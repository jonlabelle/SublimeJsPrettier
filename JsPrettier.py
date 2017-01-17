# -*- coding: utf-8 -*-

import os
import json
import platform
import sublime
import sublime_plugin

from os.path import splitext
from subprocess import PIPE, Popen

#
# Monkey patch `sublime.Region` so it can be iterable:
sublime.Region.totuple = lambda self: (self.a, self.b)
sublime.Region.__iter__ = lambda self: self.totuple().__iter__()

PLUGIN_NAME = 'JsPrettier'
PLUGIN_PATH = os.path.join(sublime.packages_path(), os.path.dirname(os.path.realpath(__file__)))
SETTINGS_FILE = '{0}.sublime-settings'.format(PLUGIN_NAME)
JS_PRETTIER_FILE = '{0}.js'.format(PLUGIN_NAME.lower())
JS_PRETTIER_PATH = os.path.join(PLUGIN_PATH, JS_PRETTIER_FILE)

PRETTIER_OPTION_CLI_MAP = [
    {'option': 'printWidth', 'cli': '--print-width'},
    {'option': 'tabWidth', 'cli': '--tab-width'},
    {'option': 'useFlowParser', 'cli': '--flow-parser'},
    {'option': 'singleQuote', 'cli': '--single-quote'},
    {'option': 'trailingComma', 'cli': '--trailing-comma'},
    {'option': 'bracketSpacing', 'cli': '--bracket-spacing'},
]


class JsPrettierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.file_name() is None:
            return sublime.error_message(
                '%s Error\n\n'
                'The current View must be Saved\n'
                'before running JsPrettier.' % PLUGIN_NAME)

        prettier_options = self.get_prettier_options()
        prettier_options['tabWidth'] = self.get_tab_size()

        #
        # Format entire file:
        if not self.has_selection():
            region = sublime.Region(0, self.view.size())
            source = self.view.substr(region)

            if not self.is_global_prettier_installed():
                transformed = self.run_local_prettier(source, prettier_options)
            else:
                transformed = self.run_global_prettier(source, prettier_options)

            if transformed and transformed == source:
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: File already formatted.'.format(PLUGIN_NAME)), 0)
            else:
                self.view.replace(edit, region, transformed)
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: File formatted.'.format(PLUGIN_NAME)), 0)
            return

        #
        # Format each selection:
        for region in self.view.sel():
            if region.empty():
                continue

            source = self.view.substr(region)

            if not self.is_global_prettier_installed():
                transformed = self.run_local_prettier(source, prettier_options)
            else:
                transformed = self.run_global_prettier(source, prettier_options)

            if transformed and transformed == source:
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Selection(s) already formatted.'.format(PLUGIN_NAME)), 0)
            else:
                self.view.replace(edit, region, transformed)
                sublime.set_timeout(lambda: sublime.status_message(
                    '{0}: Selection(s) formatted.'.format(PLUGIN_NAME)), 0)

    def run_local_prettier(self, source, prettier_options):
        prettier_options = json.dumps(prettier_options)
        cwd = os.path.dirname(self.view.file_name())

        try:
            proc = Popen(['node', JS_PRETTIER_PATH, prettier_options, cwd],
                         stdout=PIPE, stdin=PIPE, stderr=PIPE,
                         env=self.get_env(), shell=self.is_windows())
        except OSError:
            raise Exception(
                "{0} - path to node.js not found! Please ensure "
                "the path to node.js is set in your $PATH env variable "
                "by running `node -v` from the command-line.".format(PLUGIN_NAME))

        stdout, stderr = proc.communicate(input=source.encode('utf-8'))
        if stdout:
            return stdout.decode('utf-8')
        else:
            return sublime.error_message("%s Error\n\n%s" % (PLUGIN_NAME, stderr.decode('utf-8')))

    def run_global_prettier(self, source, prettier_options):
        prettier_cli_opts = self.parse_prettier_option_cli_map(prettier_options)

        cmd = [self.get_global_prettier_path()] + prettier_cli_opts + ['--stdin']
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
        if self.is_mac_os():
            env = os.environ.copy()
            env['PATH'] += self.get_node_path()
        return env

    def get_node_path(self):
        return self.get_settings().get('node_path')

    def is_global_prettier_installed(self):
        if which('prettier', self.get_node_path()) is None:
            return False
        return True

    def get_global_prettier_path(self):
        return which('prettier', self.get_node_path())

    def get_settings(self):
        settings = self.view.settings().get(PLUGIN_NAME)
        if settings is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        return settings

    def get_prettier_options(self):
        return self.get_settings().get('prettier_options')

    def get_tab_size(self):
        return int(self.view.settings().get('tab_size', 2))

    def has_selection(self):
        for sel in self.view.sel():
            start, end = sel
            if start != end:
                return True
        return False

    @staticmethod
    def is_mac_os():
        return platform.system() == 'Darwin'

    @staticmethod
    def is_windows():
        return platform.system() == 'Windows'

    @staticmethod
    def parse_prettier_option_cli_map(prettier_options):
        prettier_cli_args = []
        for mapping in PRETTIER_OPTION_CLI_MAP:
            option = prettier_options[mapping['option']]
            if option:
                prettier_cli_args.append(mapping['cli'])
                if not isinstance(option, bool):
                    prettier_cli_args.append(str(option))
        return prettier_cli_args


class CommandOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        ext = splitext(view.file_name())[1][1:]
        if self.is_enabled(view) and ext == 'js':
            view.run_command("js_prettier")

    def is_enabled(self, view):
        return self.get_settings(view).get('auto_format_on_save', False)

    @staticmethod
    def get_settings(view):
        settings = view.settings().get(PLUGIN_NAME)
        if settings is None:
            settings = sublime.load_settings(SETTINGS_FILE)
        return settings


def which(executable, path=None):
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
