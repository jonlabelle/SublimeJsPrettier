# -*- coding: utf-8 -*-

import os
import json
import platform
import sublime
import sublime_plugin

from subprocess import PIPE, Popen
from os.path import splitext

#
# monkey patch `Region` to be iterable:
sublime.Region.totuple = lambda self: (self.a, self.b)
sublime.Region.__iter__ = lambda self: self.totuple().__iter__()

PLUGIN_NAME = 'JsPrettier'
PLUGIN_PATH = os.path.join(sublime.packages_path(), os.path.dirname(os.path.realpath(__file__)))
SETTINGS_FILE = '{0}.sublime-settings'.format(PLUGIN_NAME)
JS_PRETTIER_FILE = '{0}.js'.format(PLUGIN_NAME.lower())
JS_PRETTIER_PATH = os.path.join(PLUGIN_PATH, JS_PRETTIER_FILE)

PRETTIER_OPTION_CLI_MAP = [
    {'key': 'printWidth', 'option': '--print-width'},
    {'key': 'tabWidth', 'option': '--tab-width'},
    {'key': 'useFlowParser', 'option': '--flow-parser'},
    {'key': 'singleQuote', 'option': '--single-quote'},
    {'key': 'trailingComma', 'option': '--trailing-comma'},
    {'key': 'bracketSpacing', 'option': '--bracket-spacing'},
]


class JsPrettierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.file_name() is None:
            return sublime.error_message(
                '%s Error\n\n'
                'The current View must be Saved\n'
                'before running JsPrettier.' % PLUGIN_NAME)

        config = self.get_config()
        config['tabWidth'] = self.get_tab_size()

        #
        # format entire file:
        if not self.has_selection():
            region = sublime.Region(0, self.view.size())
            source = self.view.substr(region)

            if not self.is_prettier_global_cli_installed():
                transformed = self.prettier_local(source, config)
            else:
                transformed = self.prettier_global_cli(source, config)

            if transformed and transformed == source:
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: File already formatted.'.format(PLUGIN_NAME)), 0)
            else:
                self.view.replace(edit, region, transformed)
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: File formatted.'.format(PLUGIN_NAME)), 0)
            return

        #
        # format each selection:
        for region in self.view.sel():
            if region.empty():
                continue

            source = self.view.substr(region)

            if not self.is_prettier_global_cli_installed():
                transformed = self.prettier_local(source, config)
            else:
                transformed = self.prettier_global_cli(source, config)

            if transformed and transformed == source:
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Selection(s) already formatted.'.format(PLUGIN_NAME)), 0)
            else:
                self.view.replace(edit, region, transformed)
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Selection(s) formatted.'.format(PLUGIN_NAME)), 0)

    def prettier_local(self, source, config):
        config = json.dumps(config)
        cwd = os.path.dirname(self.view.file_name())

        try:
            proc = Popen(['node', JS_PRETTIER_PATH, config, cwd],
                         stdout=PIPE, stdin=PIPE, stderr=PIPE,
                         env=self.get_env(), shell=self.is_windows())
        except OSError:
            raise Exception(
                "{0} - node.js program path not found! Please ensure "
                "the path to node.js is set in your $PATH env variable "
                "by running `node -v` from the command-line.".format(PLUGIN_NAME))

        stdout, stderr = proc.communicate(input=source.encode('utf-8'))
        if stdout:
            return stdout.decode('utf-8')
        else:
            return sublime.error_message(
                "%s Error\n\n%s" % (PLUGIN_NAME, stderr.decode('utf-8')))

    def prettier_global_cli(self, source, config):
        prettier_cli_opts = self.parse_settings_to_cli_args(config)

        cmd = [self.get_prettier_global_cli_path()] + prettier_cli_opts + ['--stdin']
        proc = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, env=self.get_env(), shell=self.is_windows())
        stdout, stderr = proc.communicate(input=source.encode('utf-8'))
        if stderr or proc.returncode != 0:
            return sublime.error_message("%s Error\n\n%s" % (PLUGIN_NAME, stderr.decode('utf-8')))
        else:
            return stdout.decode('utf-8')

    def is_js(self):
        return self.view.scope_name(0).startswith('source.js')

    def get_env(self):
        env = None
        if self.is_osx():
            env = os.environ.copy()
            env['PATH'] += self.get_node_path()
        return env

    def get_node_path(self):
        return self.get_settings().get('node_path')

    def is_prettier_global_cli_installed(self):
        if which('prettier', self.get_node_path()) is None:
            return False
        return True

    def get_prettier_global_cli_path(self):
        return which('prettier', self.get_node_path())

    def get_settings(self):
        settings = self.view.settings().get(PLUGIN_NAME)
        if settings is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        return settings

    def get_config(self):
        return self.get_settings().get('config')

    def get_tab_size(self):
        return int(self.view.settings().get('tab_size', 2))

    def has_selection(self):
        for sel in self.view.sel():
            start, end = sel
            if start != end:
                return True
        return False

    @staticmethod
    def is_osx():
        return platform.system() == 'Darwin'

    @staticmethod
    def is_windows():
        return platform.system() == 'Windows'

    @staticmethod
    def parse_settings_to_cli_args(config):
        prettier_cli_opts = []
        for mapping in PRETTIER_OPTION_CLI_MAP:
            opt = config[mapping['key']]
            if opt:
                prettier_cli_opts.append(mapping['option'])
                if not isinstance(opt, bool):
                    prettier_cli_opts.append(str(opt))
        return prettier_cli_opts


def which(executable, path=None):
    """
    Tries to find 'executable' in the directories
    listed in 'path' parameter. Similar to the
    'NIX `which` command.

    :param executable: The program to search for.
    :param path: A string listing directories separated by 'os.pathsep';defaults to os.environ['PATH'].
    :return: The complete filename, or None if not found.
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)

    if not os.path.isfile(executable):
        for p in paths:
            f = os.path.join(p, executable)
            if os.path.isfile(f):
                return f
        return None
    else:
        return executable

class CommandOnSave(sublime_plugin.EventListener):
    def get_settings(self, view):
        settings = view.settings().get(PLUGIN_NAME)
        if settings is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        return settings
    def is_enabled(self, view):
        return self.get_settings(view).get('autoformat')
    def on_pre_save(self, view):
        ext = splitext(view.file_name())[1][1:]
        if self.is_enabled(view) and ext == 'js':
            view.run_command("js_prettier")
