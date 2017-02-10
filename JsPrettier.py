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
SETTINGS_FILE = '{0}.sublime-settings'.format(PLUGIN_NAME)

PRETTIER_OPTION_CLI_MAP = [
    {'option': 'printWidth', 'cli': '--print-width', 'default': '80'},
    {'option': 'singleQuote', 'cli': '--single-quote', 'default': 'false'},
    {'option': 'trailingComma', 'cli': '--trailing-comma', 'default': 'false'},
    {'option': 'bracketSpacing', 'cli': '--bracket-spacing', 'default': 'true'},
    {'option': 'parser', 'cli': '--parser', 'default': 'babylon'}
]


class JsPrettierCommand(sublime_plugin.TextCommand):
    _error_message = None

    def run(self, edit):
        view = self.view

        if view.file_name() is None:
            return sublime.error_message(
                '{0} Error\n\n'
                'The current View must be Saved\n'
                'before running JsPrettier.'.format(PLUGIN_NAME))

        prettier_cli_path = self.prettier_cli_path
        if prettier_cli_path is None:
            return sublime.error_message(
                '{0} Error\n\n'
                'The path to the Prettier cli executable could '
                'not be found! Please ensure the path to prettier is '
                'set in your PATH environment variable.'.format(PLUGIN_NAME))

        prettier_args = self.parse_prettier_option_cli_map()

        #
        # Format entire file:
        if not self.has_selection:
            region = sublime.Region(0, view.size())
            source = view.substr(region)

            transformed = self.run_prettier(source, prettier_cli_path,
                                            prettier_args)
            if self.has_errors:
                self.print_error_console()
                return self.show_status_bar_error()

            if transformed and transformed == source:
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: File already formatted.'.format(PLUGIN_NAME)), 0)
            else:
                view.replace(edit, region, transformed)
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: File formatted.'.format(PLUGIN_NAME)), 0)
            return

        #
        # Format each selection:
        for region in view.sel():
            if region.empty():
                continue

            source = view.substr(region)
            transformed = self.run_prettier(source, prettier_cli_path,
                                            prettier_args)
            if self.has_errors:
                self.print_error_console()
                return self.show_status_bar_error()

            if transformed and transformed == source:
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Selection(s) already formatted.'.format(
                        PLUGIN_NAME)), 0)
            else:
                # strip trailing whitespace including line-breaks from the
                # end of the string, inserted by prettier:
                transformed = sub(r'\s+\Z', '', transformed)

                view.replace(edit, region, transformed)
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Selection(s) formatted.'.format(PLUGIN_NAME)), 0)

    @property
    def has_errors(self):
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
    def is_js(self):
        return self.view.scope_name(0).startswith('source.js')

    @property
    def proc_env(self):
        env = None
        if not self.is_windows():
            env = os.environ.copy()
            usr_path = ':/usr/local/bin'
            if not self.path_exists_in_env_path(usr_path) \
                    and self.path_exists(usr_path):
                env['PATH'] += usr_path
        return env

    @property
    def prettier_cli_path(self):
        prettier_path = self.get_setting('prettier_cli_path', '')
        if self.is_none_or_empty(prettier_path):
            return self.which('prettier')
        return self.which(prettier_path)

    @property
    def tab_size(self):
        return int(self.view.settings().get('tab_size', 2))

    @property
    def has_selection(self):
        for sel in self.view.sel():
            start, end = sel
            if start != end:
                return True
        return False

    def run_prettier(self, source, prettier_cli_path, prettier_args):
        self._error_message = None
        cmd = [prettier_cli_path] + prettier_args + ['--stdin'] + \
              ['--color'] + ['false']
        try:
            proc = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE,
                         env=self.proc_env, shell=self.is_windows())
            stdout, stderr = proc.communicate(input=source.encode('utf-8'))
            if stderr or proc.returncode != 0:
                self.error_message = "Prettier Error Code: {0}\n\n{1}".format(
                    str(proc.returncode), stderr.decode('utf-8'))
                return None
            else:
                return stdout.decode('utf-8')
        except OSError:
            raise Exception(
                "{0} - path to prettier not found! Please ensure "
                "the path to prettier is set in your $PATH env "
                "variable.".format(PLUGIN_NAME))

    def parse_prettier_option_cli_map(self):
        prettier_cli_args = []
        for mapping in PRETTIER_OPTION_CLI_MAP:
            option_name = mapping['option']
            cli_name = mapping['cli']
            val = self.get_sub_setting('prettier_options', option_name)
            if val is None or str(val) == '':
                val = mapping['default']
            prettier_cli_args.append(cli_name)
            prettier_cli_args.append(str(val).lower())

        # get/set the `tabWidth` based on the current view:
        prettier_cli_args.append('--tab-width')
        prettier_cli_args.append(str(self.tab_size))

        return prettier_cli_args

    def show_status_bar_error(self):
        sublime.set_timeout(lambda: sublime.status_message(
            '{0}: Format failed! Open the console window to '
            'view error details.'.format(PLUGIN_NAME)), 0)

    def print_error_console(self):
        print("\n------------------\n {0} Error \n------------------\n\n"
              "{1}".format(PLUGIN_NAME, self.error_message))

    def get_setting(self, key, default_value=None):
        settings = self.view.settings().get(PLUGIN_NAME)
        if settings is None or settings.get(key) is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        return settings.get(key, default_value)

    def get_sub_setting(self, key, sub_key=None):
        settings = self.view.settings().get(PLUGIN_NAME)
        if settings is None or settings.get(key).get(sub_key) is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        return settings.get(key).get(sub_key)

    def which(self, executable, path=None):
        if not self.is_none_or_empty(executable):
            if os.path.isfile(executable):
                return executable

        if self.is_none_or_empty(path):
            path = os.environ['PATH']
            if not self.is_windows():
                usr_path = ':/usr/local/bin'
                if not self.path_exists_in_env_path(usr_path, path) \
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
    def path_exists_in_env_path(find_path, env_path=None):
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
    def is_none_or_empty(val):
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


class CommandOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        ext = splitext(view.file_name())[1][1:]
        if self.is_enabled(view) and ext == 'js':
            view.run_command("js_prettier")

    def is_enabled(self, view):
        return self.get_setting(view, 'auto_format_on_save', False)

    @staticmethod
    def get_setting(view, key, default_value=None):
        settings = view.settings().get(PLUGIN_NAME)
        if settings is None or settings.get(key) is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        return settings.get(key, default_value)
