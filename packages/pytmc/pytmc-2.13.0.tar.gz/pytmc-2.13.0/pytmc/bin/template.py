"""
"pytmc template" is a command line utility to expand a template based on a
TwinCAT3 project (or XML-format file such as .TMC).

The template file is expected to be in Jinja template format.

The following dictionaries are available in the template context::

    solutions - {solution_filename: [project_fn: {...}, ...], ...}
    projects - {project_filename: {...}, ...}
    others - {filename: {...}, ...}

If installed and available, ``git_info`` will be available on each project.

The following helpers are available in the environment::

    config_to_pragma
    data_type_to_record_info
    determine_block_type
    element_to_class_name
    enumerate_types
    get_boxes
    get_data_type_by_reference
    get_data_types
    get_library_versions
    get_links
    get_linter_results
    get_motors
    get_nc
    get_pou_call_blocks
    get_symbols
    list_types
    max
    min
    separate_by_classname

And the following filters::

    epics_prefix
    epics_suffix
    pragma
    title_fill
"""

import argparse
import functools
import logging
import os
import pathlib
import sys
from typing import Generator, List, Optional, Tuple

import jinja2

from .. import parser, pragmas
from ..record import EPICSRecord
from . import pragmalint, stcmd, summary, util
from .db import process as db_process

try:
    import git
except ImportError:
    git = None


DESCRIPTION = __doc__

logger = logging.getLogger(__name__)


def build_arg_parser(argparser=None):
    if argparser is None:
        argparser = argparse.ArgumentParser()

    argparser.description = DESCRIPTION
    argparser.formatter_class = argparse.RawTextHelpFormatter

    argparser.add_argument(
        'projects', type=str,
        help='Path to project or solution (.tsproj, .sln)',
        nargs='+',
    )

    argparser.add_argument(
        '-t', '--template',
        dest='template',
        type=argparse.FileType(mode='r'),
        help='Template filename (default: standard input)',
        default='-',
    )

    argparser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Post template generation, open an interactive Python session'
    )

    return argparser


def find_git_root(fn: pathlib.Path) -> Optional[pathlib.Path]:
    """Given a file, find the git repository root (if it exists)."""
    while fn:
        if (fn / ".git").exists():
            return fn
        fn = fn.parent


def _to_http_url(url: str) -> str:
    """Git over SSH -> GitHub https URL."""
    if url.startswith("git@github.com:"):
        _, repo_slug = url.split(':')
        return f"https://github.com/{repo_slug}"
    return url


def _to_doc_url(url: str) -> str:
    """Git over SSH -> GitHub https URL."""
    try:
        org, repo = _to_repo_slug(url).split('/')
        return f"https://{org}.github.io/{repo}"
    except Exception:
        return ""


def _to_tree_url(url: str, hash: str) -> str:
    """Get a github.com/org/repo/tree/master-style URL."""
    url = _to_http_url(url)
    if url.startswith("https://github.com"):
        return f"{url}/tree/{hash}"
    return url


def _to_repo_slug(url: str) -> str:
    """Get a org/repo from a full URL."""
    url = _to_http_url(url)
    github = "https://github.com/"
    if url.startswith(github):
        return url.split(github)[1]
    return url


def get_git_info(fn: pathlib.Path) -> str:
    """Get the git hash and other info for the repository that ``fn`` is in."""
    if git is None:
        raise RuntimeError("gitpython not installed")
    repo = git.Repo(find_git_root(fn))
    urls = [
        url
        for remote in repo.remotes
        for url in remote.urls
    ]
    repo_slugs = [_to_repo_slug(url) for url in urls]
    head_sha = repo.head.commit.hexsha
    try:
        desc = repo.git.describe("--contains", head_sha)
    except git.GitCommandError:
        desc = repo.git.describe("--always", "--tags")

    return {
        "describe": desc,
        "sha": head_sha,
        "repo_slug": repo_slugs[0] if repo_slugs else None,
        "repo_slugs": repo_slugs,
        "doc_urls": [_to_doc_url(url) for url in urls],
        "repo_urls": [_to_http_url(url) for url in urls],
        "tree_urls": [_to_tree_url(url, head_sha) for url in urls],
        "repo": repo,
    }


def project_to_dict(path: str) -> dict:
    """
    Create a user/template-facing dictionary of project information.

    In the case of a tsproj or solution, returns keys solutions and projects.
    All other formats (such as .tmc) fall under the "others" key, leaving it up
    to the template to classify.
    """
    path = pathlib.Path(path)
    suffix = path.suffix.lower()

    if suffix in {'.tsproj', '.sln'}:
        if suffix == '.sln':
            project_files = parser.projects_from_solution(path)
            solution = path
        else:
            project_files = [path]
            solution = None

        projects = {
            fn: parser.parse(fn)
            for fn in project_files
        }

        for fn, project in projects.items():
            try:
                project.git_info = get_git_info(fn)
            except Exception:
                project.git_info = {
                    "describe": "unknown",
                    "sha": "unknown",
                    "urls": [],
                    "links": [],
                    "repo_slug": "unknown",
                    "repo_slugs": [],
                    "doc_urls": [],
                    "repo_urls": [],
                    "tree_urls": [],
                    "repo": None,
                }

        solutions = {solution: projects} if solution is not None else {}

        return {
            'solutions': solutions,
            'projects': projects,
        }

    return {
        'others': {path: parser.parse(path)},
    }


def projects_to_dict(*paths) -> dict:
    """
    Create a user/template-facing dictionary of project information.

    Returns
    -------
    dict
        Information dictionary with keys::
            solutions - {solution_filename: [project_fn: {...}, ...], ...}
            projects - {project_filename: {...}, ...}
            others - {filename: {...}, ...}
    """
    result = {
        'solutions': {},
        'projects': {},
        'others': {},
    }
    for path in paths:
        for key, value in project_to_dict(path).items():
            result[key].update(value)
    return result


def get_jinja_filters(**user_config):
    """All jinja filters."""

    if 'delim' not in user_config:
        user_config['delim'] = ':'

    if 'prefix' not in user_config:
        user_config['prefix'] = 'PREFIX'

    def epics_prefix(obj):
        return stcmd.get_name(obj, user_config)[0]

    def epics_suffix(obj):
        return stcmd.get_name(obj, user_config)[1]

    def pragma(obj, key, default=''):
        item_and_config = pragmas.expand_configurations_from_chain([obj])
        if item_and_config:
            item_to_config = dict(item_and_config[0])
            config = pragmas.squash_configs(*item_to_config.values())
            return config.get(key, default)
        return default

    def title_fill(text, fill_char):
        return fill_char * len(text)

    return {
        key: value for key, value in locals().items()
        if not key.startswith('_')
    }


def get_symbols(plc) -> Generator[parser.Symbol, None, None]:
    """Get symbols for the PLC."""
    for symbol in plc.find(parser.Symbol):
        symbol.top_level_group = (
            symbol.name.split('.')[0] if symbol.name else 'Unknown')
        yield symbol


@functools.lru_cache()
def get_motors(plc) -> list:
    """Get motor symbols for the PLC (non-pointer DUT_MotionStage)."""
    symbols = get_symbols(plc)
    return [
        mot for mot in symbols['Symbol_DUT_MotionStage']
        if not mot.is_pointer
    ]


@functools.lru_cache()
def get_plc_records(plc: parser.Plc,
                    dbd: Optional[str] = None,
                    ) -> Tuple[List[EPICSRecord], List[Exception]]:
    """
    Get EPICS records generated from a specific PLC.

    Returns
    -------
    records : list of EPICSRecord
        Records generated.

    exceptions : list of Exception
        Any exceptions raised during the generation process.
    """
    if plc.tmc is None:
        return None, None

    try:
        packages, exceptions = db_process(
            plc.tmc, dbd_file=dbd, allow_errors=True,
            show_error_context=True,
        )
    except Exception:
        logger.exception(
            'Failed to create EPICS records'
        )
        return None, None

    records = [
        record
        for package in packages
        for record in package.records
    ]

    return records, exceptions


@functools.lru_cache()
def get_nc(project: parser.TopLevelProject) -> parser.NC:
    """Get the top-level NC settings for the project."""
    try:
        nc, = list(project.find(parser.NC, recurse=False))
        return nc
    except Exception:
        return None


@functools.lru_cache()
def get_data_types(project) -> List[dict]:
    """Get the data types container for the project."""
    data_types = getattr(project, 'DataTypes', [None])[0]
    if data_types is not None:
        return list(summary.enumerate_types(data_types))
    return []


@functools.lru_cache()
def get_boxes(project) -> list:
    """Get boxes contained in the project."""
    return list(
        sorted(project.find(parser.Box),
               key=lambda box: int(box.attributes['Id']))
    )


def _clean_link(link):
    """Clean None from links for easier displaying."""
    link.a = tuple(value or '' for value in link.a)
    link.b = tuple(value or '' for value in link.b)
    return link


@functools.lru_cache()
def get_links(project) -> list:
    """Get links contained in the project or PLC."""
    return list(_clean_link(link) for link in project.find(parser.Link))


@functools.lru_cache()
def get_linter_results(plc: parser.Plc) -> dict:
    """
    Lint the provided PLC code pragmas.

    Returns
    -------
    dict
        Includes "pragma_count", "pragma_errors", and "linter_results" keys.
    """
    pragma_count = 0
    linter_errors = 0
    results = []

    for fn, source in plc.source.items():
        for info in pragmalint.lint_source(fn, source):
            pragma_count += 1
            if info.exception is not None:
                linter_errors += 1
                results.append(info)

    return {
        'pragma_count': pragma_count,
        'pragma_errors': linter_errors,
        'linter_results': results,
    }


def config_to_pragma(config: dict,
                     skip_desc: bool = True,
                     skip_pv: bool = True) -> Tuple[str, str]:
    """
    Convert a configuration dictionary into a single pragma string.

    Yields
    ------
    key: str
        Pragma key.

    value: str
        Pragma value.
    """
    if not config:
        return

    for key, value in config.items():
        if key == 'archive':
            seconds = value.get('seconds', 'unknown')
            method = value.get('method', 'unknown')
            fields = value.get('fields', {'VAL'})
            if seconds != 1 or method != 'scan':
                yield ('archive', f'{seconds}s {method}')
            if fields != {'VAL'}:
                yield ('archive_fields', ' '.join(fields))
        elif key == 'update':
            frequency = value.get('frequency', 1)
            method = value.get('method', 'unknown')
            if frequency != 1 or method != 'poll':
                yield (key, f'{frequency}hz {method}')
        elif key == 'field':
            for field, value in value.items():
                if field != 'DESC' or not skip_desc:
                    yield ('field', f'{field} {value}')
        elif key == 'pv':
            if not skip_pv:
                yield (key, ':'.join(value))
        else:
            yield (key, value)


@functools.lru_cache()
def get_library_versions(plc: parser.Plc) -> List[dict]:
    """Get library version information for the given PLC."""
    def find_by_name(cls_name):
        try:
            cls = parser.TWINCAT_TYPES[cls_name]
        except KeyError:
            return []
        else:
            return list(plc.find(cls, recurse=False))

    versions = {}

    for category in ('PlaceholderReference', 'PlaceholderResolution',
                     'LibraryReference'):
        for obj in find_by_name(category):
            info = obj.get_resolution_info()
            info['category'] = category
            if info['name'] not in versions:
                versions[info['name']] = {}

            versions[info['name']][category] = info

    return dict(versions)


def render_template(template: str, context: dict,
                    trim_blocks=True, lstrip_blocks=True,
                    **env_kwargs):
    """
    One-time-use jinja environment + template rendering helper.
    """
    env = jinja2.Environment(
        loader=jinja2.DictLoader({'template': template}),
        trim_blocks=trim_blocks,
        lstrip_blocks=lstrip_blocks,
        **env_kwargs,
    )

    env.filters.update(get_jinja_filters())
    return env.get_template('template').render(context)


helpers = [
    config_to_pragma,
    get_symbols,
    get_motors,
    get_nc,
    get_data_types,
    get_boxes,
    get_links,
    get_linter_results,
    get_library_versions,
    parser.get_data_type_by_reference,
    parser.get_pou_call_blocks,
    parser.separate_by_classname,
    parser.element_to_class_name,
    parser.determine_block_type,
    summary.data_type_to_record_info,
    summary.enumerate_types,
    summary.list_types,
    min,
    max,
]


def get_render_context() -> dict:
    """Jinja template context dictionary - helper functions."""
    context = {func.__name__: func for func in helpers}
    context['types'] = parser.TWINCAT_TYPES
    return context


def main(projects, template=sys.stdin, debug: bool = False) -> Optional[str]:
    """
    Render a template based on a TwinCAT3 project, or XML-format file such as
    TMC.

    Parameters
    ----------
    projects : list
        List of projects or TwinCAT project files (.sln, .tsproj, .tmc, etc.)

    template : file-like object, optional
        Read the template from the provided file or standard input (default).

    debug : bool, optional
        Open a debug session after rendering with IPython.
    """

    if template is sys.stdin:
        # Check if it's an interactive user to warn them what we're doing:
        is_tty = os.isatty(sys.stdin.fileno())
        if is_tty:
            logger.warning('Reading template from standard input...')
            logger.warning('Press ^D on a blank line when done.')

        template_text = sys.stdin.read()
        if is_tty:
            logger.warning('Read template from standard input (len=%d)',
                           len(template_text))
    else:
        template_text = template.read()

    stashed_exception = None
    try:
        template_args = get_render_context()
        template_args.update(projects_to_dict(*projects))

        rendered = render_template(template_text, template_args)
    except Exception as ex:
        stashed_exception = ex
        rendered = None

    if not debug:
        if stashed_exception is not None:
            raise stashed_exception
        print(rendered)
    else:
        message = [
            'Variables: projects, template_text, rendered, template_args. '
        ]
        if stashed_exception is not None:
            message.append(f'Exception: {type(stashed_exception)} '
                           f'{stashed_exception}')

        util.python_debug_session(
            namespace=locals(),
            message='\n'.join(message)
        )
    return rendered
