# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import with_statement

import functools
import json
import os
import platform

from re import sub

from .const import IS_PY2
from .const import PLUGIN_NAME
from .const import PRETTIER_CONFIG_FILES
from .const import PRETTIER_IGNORE_FILE

if IS_PY2:
    text_type = unicode
    string_types = (str, unicode)
else:
    text_type = str
    string_types = (str,)


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


def contains(needle, haystack):
    if not needle or not haystack:
        return False
    return needle in haystack


@memoize
def find_prettier_config(start_dir, alt_dirs=None):
    """
    Find a prettier config file by searching up the file hierarchy.

    Hat tip to SublimeLinter 3!

    :param start_dir: The search start path.
    :param alt_dirs: If alt_dirs is not empty and the file hierarchy search failed,
        those directories are also checked.
    """
    dirs = _generate_dirs(start_dir, limit=500)
    for d in dirs:
        for config_file in PRETTIER_CONFIG_FILES:
            target = os.path.join(d, config_file)
            if os.path.exists(target):
                if config_file == 'package.json' and not _prettier_opts_in_package_json(target):
                    continue
                return target

    if alt_dirs is None:
        alt_dirs = []
    if '~' not in alt_dirs:
        alt_dirs.append('~')

    for d in alt_dirs:
        d = os.path.expanduser(d)
        for config_file in PRETTIER_CONFIG_FILES:
            target = os.path.join(d, config_file)
            if os.path.exists(target):
                if config_file == 'package.json' and not _prettier_opts_in_package_json(target):
                    continue
                return target

    return None


def _generate_dirs(start_dir, limit=None):
    """
    Generate directories, starting from start_dir.

    Hat tip goes to SublimeLinter 3.

    :param start_dir: The search start path.
    :param limit: If limit is None, the search will continue up to the root directory.
        Otherwise a maximum of limit directories will be checked.
    """
    right = True

    while right and (limit is None or limit > 0):
        yield start_dir
        start_dir, right = os.path.split(start_dir)

        if limit is not None:
            limit -= 1


def _prettier_opts_in_package_json(package_json_file):
    try:
        with open(package_json_file) as package_file:
            json_data = json.load(package_file)
    except Exception:
        from .sthelper import log_warn
        log_warn("Cannot parse '{0}' file. Prettier options "
                 "defined in this file will be ignored.".format(package_json_file), True)
        return False

    try:
        if json_data['prettier']:
            return True
        return False
    except KeyError:
        return False


def is_mac_os():
    return platform.system() == 'Darwin'


def is_windows():
    return platform.system() == 'Windows' or os.name == 'nt'


def to_str(value):
    if value is None:
        return ''
    if value is True:
        return 'true'
    if value is False:
        return 'false'
    return text_type(value)


def is_bool_str(val):
    """Determine if the specified string :val is 'true' or 'false'.

    :param val: The value to check.
    :return: True if if val: is a boolean string, otherwise False.
    :rtype: bool
    """
    if val is None:
        return False
    if isinstance(val, string_types):
        val = val.lower().strip()
        if val == 'true' or val == 'false':
            return True
    return False


def trim_trailing_ws_and_lines(val):
    """Trim trailing whitespace and line-breaks at the end of a string.

    :param val: The value to trim.
    :return: The val with trailing whitespace and line-breaks removed.
    """
    if val is None:
        return val
    val = sub(r'\s+\Z', '', val)
    return val


def repeat_str(str_to_repeat, repeat_length):
    """Repeat a string to a certain length.

    :param str_to_repeat: The string to repeat. Normally a single char.
    :param repeat_length: The amount of times to repeat the string.
    :return: The repeated string.
    """
    quotient, remainder = divmod(repeat_length, len(str_to_repeat))
    return str_to_repeat * quotient + str_to_repeat[:remainder]


def list_to_str(list_to_convert):
    """Convert a list of values into string.

    Each value will be separated by a single space.

    :param list_to_convert: The list to convert to a string.
    :return: The list converted into a string.
    """
    return ' '.join(to_str(l) for l in list_to_convert)


def is_str_empty_or_whitespace_only(txt):
    if not txt or len(txt) == 0:
        return True
    # strip all whitespace/invisible chars to determine textual content:
    txt = sub(r'\s+', '', txt)
    if not txt or len(txt) == 0:
        return True
    return False


def is_str_none_or_empty(val):
    """Determine if the specified str val is None or an empty.

    :param val: The str to check.
    :return: True if if val: is None or an empty, otherwise False.
    :rtype: bool
    """
    if val is None:
        return True
    if isinstance(val, string_types):
        val = val.strip()
    if not val:
        return True
    return False


def get_file_abs_dir(filepath):
    return os.path.abspath(os.path.dirname(filepath))


def env_path_contains(path_to_look_for, env_path=None):
    """Check if the specified path is listed in OS environment path.

    :param path_to_look_for: The path the search for.
    :param env_path: The environment path str.
    :return: True if the find_path exists in the env_path.
    :rtype: bool
    """
    if not path_to_look_for:
        return False
    if not env_path:
        env_path = os.environ['PATH']
    path_to_look_for = str.replace(path_to_look_for, os.pathsep, '')
    paths = env_path.split(os.pathsep)
    for path in paths:
        if path == path_to_look_for:
            return True
    return False


def env_path_exists(path):
    if not path:
        return False
    if os.path.exists(str.replace(path, os.pathsep, '')):
        return True
    return False


def which(executable, path=None):
    if is_str_none_or_empty(executable):
        return None

    executable = os.path.normpath(executable)
    if os.path.isfile(executable) and os.access(executable, os.X_OK):
        return executable

    if is_str_none_or_empty(path):
        path = os.environ.get("PATH", os.defpath)
        if not path:
            return None

        if not is_windows():
            # add '/usr/local/bin' on macos/linux if not already in path.
            usr_local_bin = ':/usr/local/bin'
            if not env_path_contains(usr_local_bin, path) \
                    and env_path_exists(usr_local_bin):
                path += usr_local_bin

    search_paths = path.split(os.pathsep)

    if is_windows():
        # The current directory takes precedence on Windows.
        if os.curdir not in search_paths:
            search_paths.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path
        # extensions. This will allow us to short circuit when given
        # "python.exe". If it does match, only test that one, otherwise we
        # have to try others.
        # hat tip: https://github.com/pydanny/whichcraft/blob/master/whichcraft.py
        if any(executable.lower().endswith(ext.lower()) for ext in pathext):
            executable_files = [executable]
        else:
            executable_files = [executable + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        executable_files = [executable]

    dirs_seen = set()
    for directory in search_paths:
        dir_normalized = os.path.normcase(directory)
        if dir_normalized not in dirs_seen:
            dirs_seen.add(dir_normalized)
            for exec_file in executable_files:
                exec_file_path = os.path.normpath(os.path.join(directory, exec_file))
                if os.path.isfile(exec_file_path) and os.access(exec_file_path, os.X_OK):
                    return exec_file_path

    return None


def get_proc_env():
    env = None
    if not is_windows():
        env = os.environ.copy()
        usr_path = ':/usr/local/bin'
        if not env_path_contains(usr_path) and env_path_exists(usr_path):
            env['PATH'] += usr_path
    return env


def in_source_file_path_or_project_root(source_file_dir, st_project_path, filename):
    # check in source file dir:
    source_file_dir_ignore_path = os.path.join(source_file_dir, filename)
    if os.path.exists(source_file_dir_ignore_path):
        return source_file_dir_ignore_path

    # check in sublime text project root dir:
    sublime_text_project_dir_path = os.path.join(st_project_path, filename)
    if os.path.exists(sublime_text_project_dir_path):
        return sublime_text_project_dir_path

    return None


@memoize
def resolve_prettier_ignore_path(source_file_dir, st_project_path):
    """Look for a '.prettierignore'

    Try to resolve a '.prettieringore' file in source file dir, or ST project root (#97).

    :return: The path (str) to a '.prettierignore' file (if one exists) in the active Sublime Text Project Window.
    """

    return in_source_file_path_or_project_root(source_file_dir, st_project_path, PRETTIER_IGNORE_FILE)


def format_error_message(error_message, error_code):
    # inject a line break between the error message, and debug output (legibility purposes):
    error_message = error_message.replace('[error] stdin: ', '\n[error] stdin: ')

    return '\nPrettier reported the following output:\n\n' \
           '{0}\n' \
           '\nPrettier process finished with exit code {1}.\n' \
        .format(error_message, '{0}'.format(error_code))


def format_debug_message(label, message, debug_enabled=False):
    if not debug_enabled:
        return
    header = ' {0} DEBUG - {1} '.format(PLUGIN_NAME, label)
    horizontal_rule = repeat_str('-', len(header))
    print('\n{0}\n{1}\n{2}\n\n''{3}'.format(
        horizontal_rule, header, horizontal_rule, message))


def get_cli_arg_value(additional_cli_args, arg_key, arg_val_can_be_empty=False, default=None):
    if not additional_cli_args or not arg_key:
        return default
    if not isinstance(additional_cli_args, dict):
        return default
    result = None
    for key, val in additional_cli_args.items():
        if key == arg_key:
            if arg_val_can_be_empty:
                result = key
            else:
                result = val
        break
    if result is None:
        return default
    return result


def ensure_file_has_ext(file_name, file_ext):
    if not file_name.endswith(file_ext):
        return '{0}{1}'.format(file_name, file_ext)
    return file_name
