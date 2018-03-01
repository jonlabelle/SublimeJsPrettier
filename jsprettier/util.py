# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import with_statement

import functools
import json
import os
import platform
import sys

from re import sub

from .const import PLUGIN_NAME
from .const import PRETTIER_CONFIG_FILES
from .const import PRETTIER_IGNORE_FILE


IS_PY2 = sys.version_info[0] == 2

if IS_PY2:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
else:
    text_type = str
    string_types = (str,)
    integer_types = (int,)


def log(msg):
    print("{0}: {1}".format(PLUGIN_NAME, msg))


def log_warn(msg):
    print("{0} [WARNING]: {1}".format(PLUGIN_NAME, msg))


def log_info(msg):
    print("{0} [INFO]: {1}".format(PLUGIN_NAME, msg))


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


def find_prettier_config(start_dir, alt_dirs=None):
    if alt_dirs is None:
        alt_dirs = []
    if '~' not in alt_dirs:
        alt_dirs.append('~')
    prettier_config = None
    for config_file in PRETTIER_CONFIG_FILES:
        prettier_config = _find_file(
            start_dir=start_dir, filename=config_file, parent=False, limit=500, aux_dirs=alt_dirs)
        if prettier_config and os.path.exists(prettier_config):
            # check for prettier key defined package.json
            if os.path.basename(prettier_config) == 'package.json' and not \
                    _prettier_opts_in_package_json(prettier_config):
                # no prettier key... reset found confile to None
                prettier_config = None
                continue
            break

    return prettier_config


def _climb_dirs(start_dir, limit=None):
    """
    Generate directories, starting from start_dir.

    Hat tip goes to SublimeLinter 3.

    :param start_dir: The search start path.
    :param limit: If limit is None, stop at the root directory. Otherwise return a maximum of limit directories.
    """
    right = True

    while right and (limit is None or limit > 0):
        yield start_dir
        start_dir, right = os.path.split(start_dir)

        if limit is not None:
            limit -= 1


def _find_file(start_dir, filename, parent=False, limit=None, aux_dirs=None):
    """
    Find the given file by searching up the file hierarchy from start_dir.

    Hat tip goes to SublimeLinter 3.

    :param start_dir: The search start path.
    :param filename: The file name to search for.
    :param parent: If the file is found and parent is False, returns the path to the file.
        If parent is True the path to the file's parent directory is returned.
    :param limit: If limit is None, the search will continue up to the root directory.
        Otherwise a maximum of limit directories will be checked.
    :param aux_dirs: If aux_dirs is not empty and the file hierarchy search failed,
        those directories are also checked.
    """
    if aux_dirs is None:
        aux_dirs = []
    for d in _climb_dirs(start_dir, limit=limit):
        target = os.path.join(d, filename)

        if os.path.exists(target):
            if parent:
                return d

            return target

    for d in aux_dirs:
        d = os.path.expanduser(d)
        target = os.path.join(d, filename)

        if os.path.exists(target):
            if parent:
                return d

            return target


def _prettier_opts_in_package_json(package_json_file):
    try:
        with open(package_json_file) as package_file:
            json_data = json.load(package_file)
    except Exception:
        log_warn("Cannot parse '{0}' file. Prettier options "
                 "defined in this file will be ignored.".format(package_json_file))
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
    if not is_str_none_or_empty(executable) \
            and os.path.isfile(executable):
        return executable

    if is_str_none_or_empty(path):
        path = os.environ['PATH']
        if not is_windows():
            usr_path = ':/usr/local/bin'
            if not env_path_contains(usr_path, path) \
                    and env_path_exists(usr_path):
                path += usr_path

    paths = path.split(os.pathsep)
    if not os.path.isfile(executable):
        for directory in paths:
            exec_path = os.path.join(directory, executable)
            if os.path.isfile(exec_path):
                return exec_path
        return None
    return executable


def get_proc_env():
    env = None
    if not is_windows():
        env = os.environ.copy()
        usr_path = ':/usr/local/bin'
        if not env_path_contains(usr_path) \
                and env_path_exists(usr_path):
            env['PATH'] += usr_path
    return env


def in_source_file_path_or_project_root(source_file_dir, st_project_path, filename):
    # check for .prettierignore in source file dir:
    source_file_dir_ignore_path = os.path.join(source_file_dir, filename)
    if os.path.exists(source_file_dir_ignore_path):
        return source_file_dir_ignore_path

    # check for .prettierignore in sublime text project root:
    sublime_text_project_dir_path = os.path.join(st_project_path, filename)
    if os.path.exists(sublime_text_project_dir_path):
        return sublime_text_project_dir_path

    return None


def resolve_prettier_ignore_path(source_file_dir, st_project_path):
    """Look for a '.prettierignore'

    Try to resolve a '.prettieringore' file in source file dir, or ST project root (#97).

    :return: The path (str) to a '.prettierignore' file (if one exists) in the active Sublime Text Project Window.
    """

    return in_source_file_path_or_project_root(source_file_dir, st_project_path, PRETTIER_IGNORE_FILE)


def format_error_message(error_message, error_code):
    return 'Prettier reported the following error(s):\n\n' \
           '{0}\n' \
           'Process finished with exit code {1}\n' \
        .format(error_message, '{0}'.format(error_code))


def format_debug_message(label, message, debug_enabled=False):
    if not debug_enabled:
        return
    header = ' {0} DEBUG - {1} '.format(PLUGIN_NAME, label)
    horizontal_rule = repeat_str('-', len(header))
    print('\n{0}\n{1}\n{2}\n\n''{3}'.format(
        horizontal_rule, header, horizontal_rule, message))


def parse_additional_cli_args(additional_cli_args_setting=None):
    listofargs = []
    if additional_cli_args_setting is None:
        additional_cli_args_setting = {}
    if additional_cli_args_setting and len(additional_cli_args_setting) > 0 \
            and isinstance(additional_cli_args_setting, dict):
        for arg_key, arg_value in additional_cli_args_setting.items():
            arg_key = to_str(arg_key).strip()
            if len(arg_key) == 0:
                # arg key cannot be empty
                continue
            listofargs.append(arg_key)

            arg_value = to_str(arg_value).strip()
            if len(arg_value) == 0:
                # arg value can be empty... just don't append it
                continue
            if is_bool_str(arg_value):
                arg_value = arg_value.lower()
            listofargs.append(arg_value)
    return listofargs


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
