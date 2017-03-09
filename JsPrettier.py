# -*- coding: utf-8 -*-

import os
import platform
from re import sub
from os.path import splitext
from subprocess import PIPE, Popen

import sublime
import sublime_plugin

#
# Monkey patch `sublime.Region` so it can be iterable:
sublime.Region.totuple = lambda self: (self.a, self.b)
sublime.Region.__iter__ = lambda self: self.totuple().__iter__()

PLUGIN_NAME = 'JsPrettier'
PLUGIN_PATH = os.path.join(sublime.packages_path(),
                           os.path.dirname(os.path.realpath(__file__)))
PLUGIN_CMD_NAME = 'js_prettier'
PROJECT_SETTINGS_KEY = PLUGIN_CMD_NAME
SETTINGS_FILE = '{0}.sublime-settings'.format(PLUGIN_NAME)
PRETTIER_OPTIONS_KEY = 'prettier_options'
PRETTIER_OPTION_CLI_MAP = [
    {
        'option': 'printWidth',
        'cli': '--print-width',
        'default': '80'
    },
    {
        'option': 'singleQuote',
        'cli': '--single-quote',
        'default': 'false'
    },
    {
        'option': 'trailingComma',
        'cli': '--trailing-comma',
        'default': 'none'
    },
    {
        'option': 'bracketSpacing',
        'cli': '--bracket-spacing',
        'default': 'true'
    },
    {
        'option': 'jsxBracketSameLine',
        'cli': '--jsx-bracket-same-line',
        'default': 'false'
    },
    {
        'option': 'parser',
        'cli': '--parser',
        'default': 'babylon'
    }
]


class JsPrettierCommand(sublime_plugin.TextCommand):
    _error_message = None

    def is_visible(self):
        if self.allow_inline_formatting:
            return True
        return self.is_source_js

    def is_enabled(self):
        if self.allow_inline_formatting:
            return True
        return self.is_source_js

    def run(self, edit, force_entire_file=False):
        view = self.view

        if view.file_name() is None:
            return sublime.error_message(
                '{0} Error\n\n'
                'The current View must be Saved '
                'before running JsPrettier.'.format(PLUGIN_NAME))

        prettier_cli_path = self.prettier_cli_path
        if prettier_cli_path is None:
            return sublime.error_message(
                '{0} Error\n\n'
                'The path to the Prettier cli executable could '
                'not be found! Please ensure the path to prettier is '
                'set in your PATH environment variable.'.format(PLUGIN_NAME))

        prettier_args = self.parse_prettier_options()
        node_path = self.node_path

        #
        # Format entire file:
        if not self.has_selection or force_entire_file is True:
            file_changed = False

            region = sublime.Region(0, view.size())
            source = view.substr(region)
            transformed = self.run_prettier(
                source, node_path, prettier_cli_path, prettier_args)
            if self.has_error:
                self.show_console_error()
                return self.show_status_bar_error()

            transformed = self.trim_trailing_ws_and_lines(transformed)
            if transformed and transformed == self.trim_trailing_ws_and_lines(
                    source):
                if self.ensure_newline_at_eof(view, edit) is True:
                    # no formatting changes applied, however, a line break was
                    # needed/inserted at eof:
                    file_changed = True
            else:
                view.replace(edit, region, transformed)
                self.ensure_newline_at_eof(view, edit)
                file_changed = True

            if file_changed is True:
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: File formatted.'.format(PLUGIN_NAME)), 0)
            else:
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: File already formatted.'.format(PLUGIN_NAME)), 0)
            return

        #
        # Format each selection:
        for region in view.sel():
            if region.empty():
                continue

            source = view.substr(region)
            transformed = self.run_prettier(
                source, node_path, prettier_cli_path, prettier_args)
            if self.has_error:
                self.show_console_error()
                return self.show_status_bar_error()

            transformed = self.trim_trailing_ws_and_lines(transformed)
            if transformed \
                    and transformed == self.trim_trailing_ws_and_lines(source):
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Selection(s) already formatted.'.format(
                        PLUGIN_NAME)), 0)
            else:
                view.replace(edit, region, transformed)
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Selection(s) formatted.'.format(PLUGIN_NAME)), 0)

    @property
    def is_debug_enabled(self):
        return self.get_setting('debug', False)

    @property
    def has_error(self):
        if not self._error_message:
            return False
        return True

    @property
    def error_message(self):
        return self._error_message

    @error_message.setter
    def error_message(self, message=None):
        self._error_message = message

    @property
    def is_source_js(self):
        return self.view.scope_name(0).startswith('source.js')

    @property
    def proc_env(self):
        env = None
        if not self.is_windows():
            env = os.environ.copy()
            usr_path = ':/usr/local/bin'
            if not self.env_path_exists(usr_path) \
                    and self.path_exists(usr_path):
                env['PATH'] += usr_path
        return env

    @property
    def prettier_cli_path(self):
        prettier_path = self.get_setting('prettier_cli_path', '')
        if self.is_none_or_empty_str(prettier_path):
            return self.which('prettier')
        return self.which(prettier_path)

    @property
    def node_path(self):
        return self.get_setting('node_path', None)

    @property
    def tab_size(self):
        return int(self.view.settings().get('tab_size', 2))

    @property
    def allow_inline_formatting(self):
        return self.get_setting('allow_inline_formatting', False)

    @property
    def has_selection(self):
        for sel in self.view.sel():
            start, end = sel
            if start != end:
                return True
        return False

    def run_prettier(self, source, node_path, prettier_cli_path,
                     prettier_args):
        self._error_message = None

        if self.is_none_or_empty_str(node_path):
            cmd = [prettier_cli_path] \
                + prettier_args \
                + ['--stdin'] \
                + ['--color=false']
        else:
            cmd = [node_path] \
                + [prettier_cli_path] \
                + prettier_args \
                + ['--stdin'] \
                + ['--color=false']
        try:
            if self.is_debug_enabled:
                self.show_debug_message(
                    'Prettier CLI Command', ' '.join(str(c) for c in cmd))

            proc = Popen(
                cmd, stdin=PIPE,
                stderr=PIPE,
                stdout=PIPE,
                env=self.proc_env,
                shell=self.is_windows())
            stdout, stderr = proc.communicate(input=source.encode('utf-8'))
            if stderr or proc.returncode != 0:
                self.format_error_message(
                    stderr.decode('utf-8'), str(proc.returncode))
                return None
            else:
                return stdout.decode('utf-8')
        except OSError as ex:
            sublime.error_message('{0} - {1}'.format(PLUGIN_NAME, ex))
            raise

    def format_error_message(self, error_message, error_code):
        self.error_message = '## Prettier CLI Error Output:\n\n{0}\n' \
                             '## Prettier CLI Return Code:\n\n{1}'\
            .format(error_message.replace('\n', '\n    '), '    {0}'
                    .format(error_code))

    def ensure_newline_at_eof(self, view, edit):
        new_line_inserted = False
        if view.size() > 0 and view.substr(view.size() - 1) != '\n':
            new_line_inserted = True
            view.insert(edit, view.size(), "\n")
        return new_line_inserted

    def trim_trailing_ws_and_lines(self, val):
        """Trim trailing whitespace and line-breaks at the end of a string.

        :param val: The value to trim.
        :return: The val with trailing whitespace and line-breaks removed.
        """
        if val is None:
            return val
        val = sub(r'\s+\Z', '', val)
        return val

    def is_bool_str(self, val):
        if val is None:
            return False
        if type(val) == str:
            val = val.lower().strip()
            if val == 'true' or val == 'false':
                return True
        return False

    def parse_prettier_options(self):
        prettier_cli_args = []

        for mapping in PRETTIER_OPTION_CLI_MAP:
            option_name = mapping['option']
            cli_option_name = mapping['cli']

            option_value = self.get_sub_setting(option_name)
            if self.is_none_or_empty_str(option_value):
                option_value = mapping['default']

            option_value = str(option_value).lower().strip()

            if self.is_bool_str(option_value):
                prettier_cli_args.append('{0}={1}'.format(
                    cli_option_name, option_value))
            else:
                prettier_cli_args.append(cli_option_name)
                prettier_cli_args.append(option_value)

        # get/set the `tabWidth` based on the current view:
        prettier_cli_args.append('--tab-width')
        prettier_cli_args.append(str(self.tab_size))

        return prettier_cli_args

    def show_status_bar_error(self):
        sublime.set_timeout(lambda: sublime.status_message(
            '{0}: Format failed! Open the console window to '
            'view error details.'.format(PLUGIN_NAME)), 0)

    def show_console_error(self):
        print('\n------------\n {0} \n------------\n\n'
              '{1}'.format(PLUGIN_NAME, self.error_message))

    def show_debug_message(self, label, message):
        header = ' {0} DEBUG - {1} '.format(PLUGIN_NAME, label)
        horizontal_rule = self.repeat_str('-', len(header))
        print('\n{0}\n{1}\n{2}\n\n''{3}'.format(
            horizontal_rule, header, horizontal_rule, message))

    def _get_project_setting(self, key):
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
        if js_prettier_settings:
            if key in js_prettier_settings:
                return js_prettier_settings[key]
        return None

    def _get_project_sub_setting(self, option):
        project_settings = sublime.active_window().active_view().settings()
        js_prettier_settings = project_settings.get(PROJECT_SETTINGS_KEY, None)
        if not js_prettier_settings:
            return None
        prettier_options = js_prettier_settings.get(PRETTIER_OPTIONS_KEY, None)
        if prettier_options:
            if option in prettier_options:
                return prettier_options.get(option, None)
        return None

    def get_setting(self, key, default_value=None):
        settings = self.view.settings().get(PLUGIN_NAME)
        if settings is None or settings.get(key) is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        value = settings.get(key, default_value)
        # check for project-level overrides:
        project_value = self._get_project_setting(key)
        if project_value is None:
            return value
        return project_value

    def get_sub_setting(self, key=None):
        settings = self.view.settings().get(PLUGIN_NAME)
        if settings is None or settings.get(PRETTIER_OPTIONS_KEY).get(
                key) is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        value = settings.get(PRETTIER_OPTIONS_KEY).get(key)
        # check for project-level overrides:
        project_value = self._get_project_sub_setting(key)
        if project_value is None:
            return value
        return project_value

    def which(self, executable, path=None):
        if not self.is_none_or_empty_str(executable):
            if os.path.isfile(executable):
                return executable

        if self.is_none_or_empty_str(path):
            path = os.environ['PATH']
            if not self.is_windows():
                usr_path = ':/usr/local/bin'
                if not self.env_path_exists(usr_path, path) \
                        and self.path_exists(usr_path):
                    path += usr_path

        paths = path.split(os.pathsep)
        if not os.path.isfile(executable):
            for p in paths:
                f = os.path.join(p, executable)
                if os.path.isfile(f):
                    return f
            return None
        else:
            return executable

    @staticmethod
    def env_path_exists(find_path, env_path=None):
        """Check if the specified path is listed in OS enviornment path.

        :param find_path: The path the search for.
        :param env_path: The environment path str.
        :return: True if the find_path exists in the env_path.
        :rtype: bool
        """
        if not find_path:
            return False
        if not env_path:
            env_path = os.environ['PATH']
        find_path = str.replace(find_path, os.pathsep, '')
        paths = env_path.split(os.pathsep)
        for p in paths:
            if p == find_path:
                return True
        return False

    @staticmethod
    def path_exists(path):
        if not path:
            return False
        if os.path.exists(str.replace(path, os.pathsep, '')):
            return True
        return False

    @staticmethod
    def is_none_or_empty_str(val):
        """Determine if the specified str val is None or an empty.

        :param val: The str to check.
        :return: True if if val: is None or an empty, otherwise False.
        :rtype: bool
        """
        if val is None:
            return True
        if type(val) == str:
            val = val.strip()
        if not val:
            return True
        return False

    @staticmethod
    def is_mac_os():
        return platform.system() == 'Darwin'

    @staticmethod
    def is_windows():
        return platform.system() == 'Windows' or os.name == 'nt'

    @staticmethod
    def repeat_str(str_to_repeat, repeat_length):
        """Repeat a string to a certain length.

        :param str_to_repeat: The string to repeat. Normally a single char.
        :param repeat_length: The amount of times to repeat the string.
        :return: The repeated string.
        """
        a, b = divmod(repeat_length, len(str_to_repeat))
        return str_to_repeat * a + str_to_repeat[:b]


class CommandOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if self.is_allowed(view) is True and self.is_enabled(view):
            view.run_command(PLUGIN_CMD_NAME, {'force_entire_file': True})

    def is_enabled(self, view):
        return self.allow_inline_formatting(view)

    def is_allowed(self, view):
        return self.is_js_file(view)

    def is_js_file(self, view):
        ext = splitext(view.file_name())[1][1:]
        if ext == 'js' or ext == 'jsx':
            return True
        return False

    def allow_inline_formatting(self, view):
        return self.get_setting(view, 'auto_format_on_save', False)

    def _get_project_setting(self, key):
        settings = sublime.active_window().active_view().settings()
        if not settings:
            return None
        jsprettier = settings.get(PROJECT_SETTINGS_KEY)
        if jsprettier:
            if key in jsprettier:
                return jsprettier[key]
        return None

    def get_setting(self, view, key, default_value=None):
        settings = view.settings().get(PLUGIN_NAME)
        if settings is None or settings.get(key) is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        value = settings.get(key, default_value)
        # check for project-level overrides:
        project_value = self._get_project_setting(key)
        if project_value is None:
            return value
        return project_value
