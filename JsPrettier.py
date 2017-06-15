# -*- coding: utf-8 -*-

import os
import platform

from re import sub
from subprocess import PIPE
from subprocess import Popen

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
    },
    {
        'option': 'semi',
        'cli': '--semi',
        'default': 'true'
    }
]
ALLOWED_FILE_EXTENSIONS = [
    'js',
    'jsx',
    'ts',
    'tsx',
    'css',
    'scss',
    'less'
]
IS_SUBLIME_TEXT_LATEST = int(sublime.version()) >= 3000


class JsPrettierCommand(sublime_plugin.TextCommand):
    _error_message = None

    @property
    def debug(self):
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
        """The prettier cli path.

        When the `prettier_cli_path` setting is empty (""),
        the path is resolved by searching locations in the following order,
        returning the first match of the prettier cli path...

        - Locally installed prettier, relative to a Sublime Text Project
          file's root directory, e.g.: `node_modules/.bin/prettier'.
        - User's $HOME/node_modules directory.
        - Look in the JsPrettier Sublime Text plug-in directory for
          `node_modules/.bin/prettier`.
        - Finally, check if prettier is installed globally,
          e.g.: `yarn global add prettier`
            or: `npm install -g prettier`

        :return: The prettier cli path.
        """
        user_prettier_path = self.get_setting('prettier_cli_path', '')
        project_path = self.get_active_project_path()

        if self.is_str_none_or_empty(user_prettier_path):
            global_prettier_path = self.which('prettier')
            project_prettier_path = os.path.join(
                project_path, 'node_modules', '.bin', 'prettier')
            plugin_prettier_path = os.path.join(
                PLUGIN_PATH, 'node_modules', '.bin', 'prettier')

            if os.path.exists(project_prettier_path):
                return project_prettier_path

            if os.path.exists(plugin_prettier_path):
                return plugin_prettier_path

            return global_prettier_path

        # handle cases when the user specifies a prettier cli path that is
        # relative to the working file or project:
        if not os.path.isabs(user_prettier_path):
            user_prettier_path = os.path.join(project_path, user_prettier_path)

        return user_prettier_path

    @property
    def node_path(self):
        return self.get_setting('node_path', None)

    @property
    def tab_size(self):
        return int(self.view.settings().get('tab_size', 2))

    @property
    def use_tabs(self):
        translate_tabs_to_spaces = self.view.settings().get(
            'translate_tabs_to_spaces', True)
        if not translate_tabs_to_spaces:
            return True
        return False

    @property
    def allow_inline_formatting(self):
        return self.get_setting('allow_inline_formatting', False)

    @property
    def additional_cli_args(self):
        return self.get_setting('additional_cli_args', {})

    @property
    def max_file_size_limit(self):
        return int(self.get_setting('max_file_size_limit', -1))

    def exceeds_max_file_size_limit(self, view):
        if self.max_file_size_limit == -1:
            return False
        if os.path.getsize(view.file_name()) > self.max_file_size_limit:
            return True
        return False

    def is_allowed_file_ext(self, view):
        filename = view.file_name()
        if not filename:
            return False
        file_ext = os.path.splitext(filename)[1][1:]
        if file_ext in ALLOWED_FILE_EXTENSIONS:
            return True
        if file_ext in set(self.get_setting('custom_file_extensions', [])):
            return True
        return False

    def run(self, edit, force_entire_file=False):
        view = self.view

        if view.file_name() is None:
            #
            # Handle file must first be saved:
            if not IS_SUBLIME_TEXT_LATEST:
                # sublime text 2x: limited dialog support, just show error:
                return sublime.error_message(
                    '{0} Error\n\n'
                    'File must first be saved.'.format(PLUGIN_NAME))
            else:
                #
                # sublime text 3+: show dialog that includes a save option:
                result = sublime.yes_no_cancel_dialog(
                    '{0}\n\n'
                    'File must first be Saved.'.format(PLUGIN_NAME),
                    'Save...', "Don't Save")
                if result == sublime.DIALOG_YES:
                    view.run_command('save')

        #
        # re-check if the file was saved here, incase user canceled or closed
        # the save dialog:
        if view.file_name() is None:
            return sublime.set_timeout(lambda: sublime.status_message(
                '{0}: File save canceled.'.format(PLUGIN_NAME)), 0)

        prettier_cli_path = self.prettier_cli_path
        if prettier_cli_path is None:
            return sublime.error_message(
                '{0} Error\n\n'
                'The path to the Prettier cli executable could '
                'not be found! Please ensure the path to prettier is '
                'set in your PATH environment variable.'.format(PLUGIN_NAME))

        if self.exceeds_max_file_size_limit(view):
            return sublime.set_timeout(lambda: sublime.status_message(
                '{0}: File ignored, max allowed file size '
                'limit reached.'.format(PLUGIN_NAME)), 0)

        prettier_args = self.parse_prettier_options(view)
        node_path = self.node_path

        # Format entire file:
        if not self.has_selection(view) or force_entire_file is True:
            region = sublime.Region(0, view.size())
            source = view.substr(region)

            if self.is_str_empty_or_whitespace_only(source):
                return sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Nothing to format in file.'.format(PLUGIN_NAME)), 0)

            transformed = self._exec_cmd(
                source, node_path, prettier_cli_path, prettier_args)
            if self.has_error:
                self.show_console_error()
                return self.show_status_bar_error()

            # sanity check to ensure textual content was returned from cmd
            # stdout, not necessarily caught in OSError try/catch
            # exception handler
            if self.is_str_empty_or_whitespace_only(transformed):
                self.error_message = 'Empty content returned to stdout'
                return self.show_status_bar_error()

            file_changed = False
            transformed = self.trim_trailing_ws_and_lines(transformed)
            if transformed:
                if transformed == self.trim_trailing_ws_and_lines(source):
                    if self.ensure_newline_at_eof(view, edit) is True:
                        # no formatting changes applied, however, a line
                        # break was needed/inserted at the end of the file:
                        file_changed = True
                else:
                    view.replace(edit, region, transformed)
                    self.ensure_newline_at_eof(view, edit)
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

        # Format each selection:
        for region in view.sel():
            if region.empty():
                continue

            source = view.substr(region)
            if self.is_str_empty_or_whitespace_only(source):
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Nothing to format in selection.'.format(
                        PLUGIN_NAME)), 0)
                continue

            transformed = self._exec_cmd(
                source, node_path, prettier_cli_path, prettier_args)
            if self.has_error:
                self.show_console_error()
                return self.show_status_bar_error()

            # sanity check to ensure textual content was returned from cmd
            # stdout, not necessarily caught in OSError try/catch
            # exception handler
            if self.is_str_empty_or_whitespace_only(transformed):
                self.error_message = 'Empty content returned to stdout'
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

    def _exec_cmd(self, source, node_path, prettier_cli_path,
                  prettier_args):
        self._error_message = None

        if self.is_str_none_or_empty(node_path):
            cmd = [prettier_cli_path] \
                + ['--stdin'] \
                + prettier_args
        else:
            cmd = [node_path] \
                + [prettier_cli_path] \
                + ['--stdin'] \
                + prettier_args

        try:
            self.show_debug_message(
                'Prettier CLI Command', self.list_to_str(cmd))

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
            return stdout.decode('utf-8')
        except OSError as ex:
            sublime.error_message('{0} - {1}'.format(PLUGIN_NAME, ex))
            raise

    def should_show_plugin(self):
        view = self.view
        if self.allow_inline_formatting is True:
            return True
        if self.is_source_js(view) is True:
            return True
        if self.is_css(view) is True:
            return True
        if self.is_allowed_file_ext(view) is True:
            return True
        return False

    def is_visible(self):
        return self.should_show_plugin()

    def is_enabled(self):
        return self.should_show_plugin()

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

    def parse_prettier_options(self, view):
        # TODO: optimize option parsing...
        prettier_cli_args = []

        is_css = self.is_css(view)
        is_typescript = self.is_typescript(view)

        for mapping in PRETTIER_OPTION_CLI_MAP:
            option_name = mapping['option']
            cli_option_name = mapping['cli']
            option_value = self.get_sub_setting(option_name)

            # internally override the 'parser' option for css
            # and set the value to 'postcss':
            if option_name == 'parser' and is_css:
                prettier_cli_args.append(cli_option_name)
                prettier_cli_args.append('postcss')
                continue

            # internally override the 'parser' for typescript
            # and set the value to 'typescript':
            if option_name == 'parser' and is_typescript:
                prettier_cli_args.append(cli_option_name)
                prettier_cli_args.append('typescript')
                continue

            if option_value is None or str(option_value) == '':
                option_value = mapping['default']
            option_value = str(option_value).strip()

            if self.is_bool_str(option_value):
                prettier_cli_args.append('{0}={1}'.format(
                    cli_option_name, option_value.lower()))
            else:
                prettier_cli_args.append(cli_option_name)
                prettier_cli_args.append(option_value)

        # set the `tabWidth` option based on the current view:
        prettier_cli_args.append('--tab-width')
        prettier_cli_args.append(str(self.tab_size))

        # set the `useTabs` option based on the current view:
        prettier_cli_args.append('{0}={1}'.format(
            '--use-tabs', str(self.use_tabs).lower()))

        # add the additional arguments from the settings file to the command:
        if self.additional_cli_args and len(self.additional_cli_args) > 0:
            for arg_key, arg_value in self.additional_cli_args.items():
                arg_key = str(arg_key).strip()
                arg_value = str(arg_value).strip()

                # handle bool options
                if arg_value != '' and self.is_bool_str(arg_value):
                    prettier_cli_args.append(
                        '{0}={1}'.format(arg_key, arg_value.lower()))
                    continue

                prettier_cli_args.append(arg_key)
                if arg_value != '':
                    prettier_cli_args.append(arg_value)

        return prettier_cli_args

    def which(self, executable, path=None):
        if not self.is_str_none_or_empty(executable):
            if os.path.isfile(executable):
                return executable

        if self.is_str_none_or_empty(path):
            path = os.environ['PATH']
            if not self.is_windows():
                usr_path = ':/usr/local/bin'
                if not self.env_path_exists(usr_path, path) \
                        and self.path_exists(usr_path):
                    path += usr_path

        paths = path.split(os.pathsep)
        if not os.path.isfile(executable):
            for directory in paths:
                exec_path = os.path.join(directory, executable)
                if os.path.isfile(exec_path):
                    return exec_path
            return None
        return executable

    def show_debug_message(self, label, message):
        if not self.debug:
            return
        header = ' {0} DEBUG - {1} '.format(PLUGIN_NAME, label)
        horizontal_rule = self.repeat_str('-', len(header))
        print('\n{0}\n{1}\n{2}\n\n''{3}'.format(
            horizontal_rule, header, horizontal_rule, message))

    def show_console_error(self):
        print('\n------------------\n {0} ERROR \n------------------\n\n'
              '{1}'.format(PLUGIN_NAME, self.error_message))

    def format_error_message(self, error_message, error_code):
        self.error_message = '## Prettier CLI Error Output:\n\n{0}\n' \
                             '## Prettier CLI Return Code:\n\n{1}'\
            .format(error_message.replace('\n', '\n    '), '    {0}'
                    .format(error_code))

    @staticmethod
    def is_source_js(view):
        return view.scope_name(0).startswith('source.js')

    @staticmethod
    def is_css(view):
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(0)
        if scopename.startswith('source.css') or filename.endswith('.css'):
            return True
        if scopename.startswith('source.scss') or filename.endswith('.scss'):
            return True
        if scopename.startswith('source.less') or filename.endswith('.less'):
            return True
        return False

    @staticmethod
    def is_typescript(view):
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(0)
        if scopename.startswith('source.ts') or filename.endswith('.ts'):
            return True
        if scopename.startswith('source.tsx') or filename.endswith('.tsx'):
            return True
        return False

    @staticmethod
    def get_active_project_path():
        """Get the active Sublime Text project path.

        Original: https://gist.github.com/astronaughts/9678368

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

    @staticmethod
    def show_status_bar_error():
        sublime.set_timeout(lambda: sublime.status_message(
            '{0}: Format failed! Open the console window to '
            'view error details.'.format(PLUGIN_NAME)), 0)

    @staticmethod
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
        if js_prettier_settings:
            if key in js_prettier_settings:
                return js_prettier_settings[key]
        return None

    @staticmethod
    def _get_project_sub_setting(option):
        project_settings = sublime.active_window().active_view().settings()
        js_prettier_settings = project_settings.get(PROJECT_SETTINGS_KEY, None)
        if not js_prettier_settings:
            return None
        prettier_options = js_prettier_settings.get(PRETTIER_OPTIONS_KEY, None)
        if prettier_options:
            if option in prettier_options:
                return prettier_options.get(option, None)
        return None

    @staticmethod
    def is_bool_str(val):
        """Determine if the specified string :val is 'true' or 'false'.

        :param val: The value to check.
        :return: True if if val: is a boolean string, otherwise False.
        :rtype: bool
        """
        if val is None:
            return False
        if type(val) == str:
            val = val.lower().strip()
            if val == 'true' or val == 'false':
                return True
        return False

    @staticmethod
    def is_str_none_or_empty(val):
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
    def is_str_empty_or_whitespace_only(txt):
        if not txt or len(txt) == 0:
            return True
        # strip all whitespace/invisible chars to determine textual content:
        txt = sub(r'\s+', '', txt)
        if not txt or len(txt) == 0:
            return True
        return False

    @staticmethod
    def list_to_str(list_to_convert):
        """Convert a list of values into string.

        Each value will be seperated by a single space.

        :param list_to_convert: The list to convert to a string.
        :return: The list converted into a string.
        """
        return ' '.join(str(l) for l in list_to_convert)

    @staticmethod
    def repeat_str(str_to_repeat, repeat_length):
        """Repeat a string to a certain length.

        :param str_to_repeat: The string to repeat. Normally a single char.
        :param repeat_length: The amount of times to repeat the string.
        :return: The repeated string.
        """
        quotient, remainder = divmod(repeat_length, len(str_to_repeat))
        return str_to_repeat * quotient + str_to_repeat[:remainder]

    @staticmethod
    def trim_trailing_ws_and_lines(val):
        """Trim trailing whitespace and line-breaks at the end of a string.

        :param val: The value to trim.
        :return: The val with trailing whitespace and line-breaks removed.
        """
        if val is None:
            return val
        val = sub(r'\s+\Z', '', val)
        return val

    @staticmethod
    def ensure_newline_at_eof(view, edit):
        new_line_inserted = False
        if view.size() > 0 and view.substr(view.size() - 1) != '\n':
            new_line_inserted = True
            view.insert(edit, view.size(), '\n')
        return new_line_inserted

    @staticmethod
    def has_selection(view):
        for sel in view.sel():
            start, end = sel
            if start != end:
                return True
        return False

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
        for path in paths:
            if path == find_path:
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
    def is_mac_os():
        return platform.system() == 'Darwin'

    @staticmethod
    def is_windows():
        return platform.system() == 'Windows' or os.name == 'nt'


class CommandOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if self.is_allowed(view) and self.is_enabled(view):
            view.run_command(PLUGIN_CMD_NAME, {'force_entire_file': True})

    def auto_format_on_save(self, view):
        return self.get_setting(view, 'auto_format_on_save', False)

    def custom_file_extensions(self, view):
        return self.get_setting(view, 'custom_file_extensions', [])

    def is_allowed(self, view):
        return self.is_allowed_file_ext(view)

    def is_enabled(self, view):
        return self.auto_format_on_save(view)

    def is_allowed_file_ext(self, view):
        filename = view.file_name()
        if not filename:
            return False
        file_ext = os.path.splitext(filename)[1][1:]
        if file_ext in ALLOWED_FILE_EXTENSIONS:
            return True
        if file_ext in set(self.custom_file_extensions(view)):
            return True
        return False

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

    @staticmethod
    def _get_project_setting(key):
        settings = sublime.active_window().active_view().settings()
        if not settings:
            return None
        jsprettier = settings.get(PROJECT_SETTINGS_KEY)
        if jsprettier:
            if key in jsprettier:
                return jsprettier[key]
        return None
