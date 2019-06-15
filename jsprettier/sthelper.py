from __future__ import absolute_import
from __future__ import print_function

import os
import sublime

from .const import AUTO_FORMAT_FILE_EXTENSIONS
from .const import IS_ST3
from .const import PLUGIN_NAME
from .const import PRETTIER_OPTIONS_KEY
from .const import PROJECT_SETTINGS_KEY
from .const import SETTINGS_FILENAME

from .util import ensure_file_has_ext
from .util import is_bool_str
from .util import is_str_none_or_empty
from .util import is_windows
from .util import memoize
from .util import to_str
from .util import which


def st_status_message(msg):
    sublime.set_timeout(lambda: sublime.status_message('{0}: {1}'.format(PLUGIN_NAME, msg)), 0)


def get_setting(view, key, default_value=None):
    settings = view.settings().get(PLUGIN_NAME)
    if settings is None or settings.get(key) is None:
        settings = sublime.load_settings(SETTINGS_FILENAME)
    value = settings.get(key, default_value)
    # check for project-level overrides:
    project_value = _get_project_setting(key)
    if project_value is None:
        return value
    return project_value


def get_sub_setting(view, key=None):
    settings = view.settings().get(PLUGIN_NAME)
    if settings is None or settings.get(PRETTIER_OPTIONS_KEY).get(key) is None:
        settings = sublime.load_settings(SETTINGS_FILENAME)
    value = settings.get(PRETTIER_OPTIONS_KEY).get(key)
    # check for project-level overrides:
    project_value = _get_project_sub_setting(key)
    if project_value is None:
        return value
    return project_value


def _get_project_setting(key):
    """Get a project setting.

    JsPrettier project settings are stored in the sublime project file
    as a dictionary, e.g.:

        "settings":
        {
            "js_prettier": { "key": "value", ... }
        }

    :param key: The project setting key.
    :return: The project setting value.
    :rtype: str
    """
    project_settings = sublime.active_window().active_view().settings()
    if not project_settings:
        return None
    js_prettier_settings = project_settings.get(PROJECT_SETTINGS_KEY)
    if js_prettier_settings and key in js_prettier_settings:
        return js_prettier_settings[key]
    return None


def _get_project_sub_setting(option):
    project_settings = sublime.active_window().active_view().settings()
    js_prettier_settings = project_settings.get(PROJECT_SETTINGS_KEY, None)
    if not js_prettier_settings:
        return None
    prettier_options = js_prettier_settings.get(PRETTIER_OPTIONS_KEY, None)
    if prettier_options and option in prettier_options:
        return prettier_options.get(option, None)
    return None


def is_file_auto_formattable(view):
    filename = view.file_name()
    if not filename:
        return False
    file_ext = filename.rpartition('.')[-1]
    if file_ext == filename:
        return False
    if file_ext in AUTO_FORMAT_FILE_EXTENSIONS:
        return True
    if file_ext in set(get_setting(view, 'custom_file_extensions', [])):
        return True
    return False


def get_st_project_path():
    """Get the active Sublime Text project path.

    Original: https://gist.github.com/astronaughts/9678368

    :rtype: object
    :return: The active Sublime Text project path.
    """
    window = sublime.active_window()
    folders = window.folders()
    if len(folders) == 1:
        return folders[0]
    else:
        active_view = window.active_view()
        if active_view:
            active_file_name = active_view.file_name()
        else:
            active_file_name = None
        if not active_file_name:
            return folders[0] if len(folders) else os.path.expanduser('~')
        for folder in folders:
            if active_file_name.startswith(folder):
                return folder
        return os.path.dirname(active_file_name)


def scroll_view_to(view, row_no, col_no):
    # error positions are offset by -1
    # prettier -> sublime text
    row_no -= 1
    col_no -= 1

    textpoint = view.text_point(row_no, col_no)
    view.sel().clear()
    view.sel().add(sublime.Region(textpoint))
    view.show_at_center(textpoint)


def has_selection(view):
    for sel in view.sel():
        if not sel.empty():
            return True
    return False


@memoize
def resolve_prettier_cli_path(view, plugin_path, st_project_path):
    """The prettier cli path.

    When the `prettier_cli_path` setting is empty (""),
    the path is resolved by searching locations in the following order,
    returning the first match of the prettier cli path...

    - Locally installed prettier, relative to a Sublime Text Project
      file's root directory, e.g.: `node_modules/.bin/prettier' and 'node_modules/prettier/bin-prettier.js';
    - User's $HOME/node_modules directory.
    - Look in the JsPrettier Sublime Text plug-in directory for
      `node_modules/.bin/prettier`.
    - Finally, check if prettier is installed globally,
      e.g.: `yarn global add prettier`
        or: `npm install -g prettier`

    :return: The prettier cli path.
    """
    custom_prettier_cli_path = expand_var(view.window(), get_setting(view, 'prettier_cli_path', ''))

    if is_str_none_or_empty(custom_prettier_cli_path):
        #
        # 1. check locally installed prettier
        project_prettier_path = os.path.join(st_project_path, 'node_modules', '.bin', 'prettier')
        plugin_prettier_path = os.path.join(plugin_path, 'node_modules', '.bin', 'prettier')
        if os.path.exists(project_prettier_path):
            return project_prettier_path
        if os.path.exists(plugin_prettier_path):
            return plugin_prettier_path
        #
        # 2. check locally installed '--no-bin-links' prettier (see #146)
        project_prettier_path_nbl = os.path.join(st_project_path, 'node_modules', 'prettier', 'bin-prettier.js')
        plugin_prettier_path_nbl = os.path.join(plugin_path, 'node_modules', 'prettier', 'bin-prettier.js')
        if os.path.exists(project_prettier_path_nbl):
            return project_prettier_path_nbl
        if os.path.exists(plugin_prettier_path_nbl):
            return plugin_prettier_path_nbl
        #
        # 3. check globally install prettier
        prettier_cmd = 'prettier'
        if is_windows():
            prettier_cmd = ensure_file_has_ext(prettier_cmd, ".cmd")
        return which(prettier_cmd)

    # handle cases when the user specifies a prettier cli path that is
    # relative to the working file or project:
    if not os.path.isabs(custom_prettier_cli_path):
        custom_prettier_cli_path = os.path.join(st_project_path, custom_prettier_cli_path)

    return os.path.normpath(custom_prettier_cli_path)


# noinspection PyUnusedLocal
@memoize
def resolve_node_path(source_file):
    node_cmd = 'node'
    if is_windows():
        node_cmd = ensure_file_has_ext(node_cmd, ".exe")
    return which(node_cmd)


def expand_var(window, var_to_expand):
    if not is_str_none_or_empty(var_to_expand):
        expanded = os.path.expanduser(var_to_expand)
        expanded = os.path.expandvars(expanded)
        if IS_ST3 and window:
            window_variables = window.extract_variables()
            expanded = sublime.expand_variables(expanded, window_variables)
        return expanded
    return var_to_expand


def parse_additional_cli_args(window, additional_cli_args_setting=None):
    listofargs = []
    if additional_cli_args_setting is None:
        additional_cli_args_setting = {}
    if additional_cli_args_setting and len(additional_cli_args_setting) > 0 \
            and isinstance(additional_cli_args_setting, dict):
        for arg_key, arg_value in additional_cli_args_setting.items():
            arg_key = to_str(arg_key).strip()
            if len(arg_key) == 0:
                # arg key cannot be empty
                log_warn("Empty argument detected in 'additional_cli_args'. Did you forget to add something?", True)
                continue
            listofargs.append(arg_key)

            arg_value = to_str(arg_value).strip()
            if len(arg_value) == 0:
                # arg value can be empty... just don't append it
                continue
            if is_bool_str(arg_value):
                arg_value = arg_value.lower()
            else:
                arg_value = expand_var(window, arg_value)
            listofargs.append(arg_value)
    return listofargs


def debug_enabled(view):
    return bool(get_setting(view, 'debug', False))


def _print_log(kind, msg, insert_leading_line_break=False):
    """Print a log message to the Sublime Text Console.

    :param kind: The kind of message to log. e.g.: 'DEBUG', 'INFO', 'WARN' or 'ERROR'.
    :param msg: The message to log.
    :param insert_leading_line_break: Whether or not to insert a leading line break before the log message.
    """
    leading_line_break = ''
    if insert_leading_line_break:
        leading_line_break = '\n'
    print("{0}[{1} {2}]: {3}".format(leading_line_break, PLUGIN_NAME, kind, msg))


def log_debug(view, msg, insert_leading_line_break=False):
    if debug_enabled(view):
        _print_log('DEBUG', msg, insert_leading_line_break)


def log_warn(msg, insert_leading_line_break=False):
    _print_log('WARN', msg, insert_leading_line_break)


def log_error(msg, insert_leading_line_break=False):
    _print_log('ERROR', msg, insert_leading_line_break)
