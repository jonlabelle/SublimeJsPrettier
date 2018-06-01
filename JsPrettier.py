# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import fnmatch
import os
import sys

from re import match
from re import search
from subprocess import PIPE
from subprocess import Popen

import sublime
import sublime_plugin


PLUGIN_PATH = os.path.join(sublime.packages_path(), os.path.dirname(os.path.realpath(__file__)))

IS_ST3 = int(sublime.version()) >= 3000
IS_PY2 = sys.version_info[0] == 2

if IS_PY2:
    # st with python 2x
    from jsprettier.const import PLUGIN_CMD_NAME
    from jsprettier.const import PLUGIN_NAME
    from jsprettier.const import PRETTIER_OPTION_CLI_MAP
    from jsprettier.const import SETTINGS_FILENAME

    from jsprettier.sthelper import debug_enabled
    from jsprettier.sthelper import get_setting
    from jsprettier.sthelper import get_st_project_path
    from jsprettier.sthelper import get_sub_setting
    from jsprettier.sthelper import has_selection
    from jsprettier.sthelper import is_file_auto_formattable
    from jsprettier.sthelper import log_debug
    from jsprettier.sthelper import log_error
    from jsprettier.sthelper import log_warn
    from jsprettier.sthelper import resolve_prettier_cli_path
    from jsprettier.sthelper import scroll_view_to
    from jsprettier.sthelper import st_status_message

    from jsprettier.util import contains
    from jsprettier.util import find_prettier_config
    from jsprettier.util import format_debug_message
    from jsprettier.util import format_error_message
    from jsprettier.util import get_cli_arg_value
    from jsprettier.util import get_file_abs_dir
    from jsprettier.util import get_proc_env
    from jsprettier.util import in_source_file_path_or_project_root
    from jsprettier.util import is_bool_str
    from jsprettier.util import is_str_empty_or_whitespace_only
    from jsprettier.util import is_str_none_or_empty
    from jsprettier.util import is_windows
    from jsprettier.util import list_to_str
    from jsprettier.util import parse_additional_cli_args
    from jsprettier.util import resolve_prettier_ignore_path
    from jsprettier.util import trim_trailing_ws_and_lines
else:
    from .jsprettier.const import PLUGIN_CMD_NAME
    from .jsprettier.const import PLUGIN_NAME
    from .jsprettier.const import PRETTIER_OPTION_CLI_MAP
    from .jsprettier.const import SETTINGS_FILENAME

    from .jsprettier.sthelper import debug_enabled
    from .jsprettier.sthelper import get_setting
    from .jsprettier.sthelper import get_st_project_path
    from .jsprettier.sthelper import get_sub_setting
    from .jsprettier.sthelper import has_selection
    from .jsprettier.sthelper import is_file_auto_formattable
    from .jsprettier.sthelper import log_debug
    from .jsprettier.sthelper import log_error
    from .jsprettier.sthelper import log_warn
    from .jsprettier.sthelper import resolve_prettier_cli_path
    from .jsprettier.sthelper import scroll_view_to
    from .jsprettier.sthelper import st_status_message

    from .jsprettier.util import contains
    from .jsprettier.util import find_prettier_config
    from .jsprettier.util import format_debug_message
    from .jsprettier.util import format_error_message
    from .jsprettier.util import get_cli_arg_value
    from .jsprettier.util import get_file_abs_dir
    from .jsprettier.util import get_proc_env
    from .jsprettier.util import in_source_file_path_or_project_root
    from .jsprettier.util import is_bool_str
    from .jsprettier.util import is_str_empty_or_whitespace_only
    from .jsprettier.util import is_str_none_or_empty
    from .jsprettier.util import is_windows
    from .jsprettier.util import list_to_str

    from .jsprettier.util import parse_additional_cli_args
    from .jsprettier.util import resolve_prettier_ignore_path
    from .jsprettier.util import trim_trailing_ws_and_lines


class JsPrettierCommand(sublime_plugin.TextCommand):
    _error_message = None

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
    def node_path(self):
        return get_setting(self.view, 'node_path')

    @property
    def tab_size(self):
        return int(self.view.settings().get('tab_size', 2))

    @property
    def use_tabs(self):
        translate_tabs_to_spaces = self.view.settings().get('translate_tabs_to_spaces', True)
        return not translate_tabs_to_spaces

    @property
    def allow_inline_formatting(self):
        return get_setting(self.view, 'allow_inline_formatting', False)

    @property
    def additional_cli_args(self):
        return get_setting(self.view, 'additional_cli_args', {})

    @property
    def max_file_size_limit(self):
        return int(get_setting(self.view, 'max_file_size_limit', -1))

    def exceeds_max_file_size_limit(self, source_file):
        if self.max_file_size_limit == -1:
            return False
        if os.path.getsize(source_file) > self.max_file_size_limit:
            return True
        return False

    def try_find_prettier_config(self, view):
        source_file_dir = get_file_abs_dir(view.file_name())
        st_project_path = get_st_project_path()

        #
        # 1. Attempt to use prettier config defined in the 'additional_cli_args' (if exist - ensure it's abs path)

        # check if '--config <filename>' is defined in 'additional_cli_args'
        # parsed_additional_cli_args = parse_additional_cli_args(self.get_additional_cli_args(view))
        additional_cli_arg_config = get_cli_arg_value(self.additional_cli_args, '--config')
        if not is_str_none_or_empty(additional_cli_arg_config):
            additional_cli_arg_config = os.path.normpath(additional_cli_arg_config)
            if not os.path.isabs(additional_cli_arg_config):
                additional_cli_arg_config = in_source_file_path_or_project_root(
                    source_file_dir, st_project_path, additional_cli_arg_config)
                if additional_cli_arg_config and os.path.exists(additional_cli_arg_config):
                    log_debug(view, "Using Prettier config file defined in 'additional_cli_args' config -> {0}'"
                                    "".format(additional_cli_arg_config), True)
                    return additional_cli_arg_config

                log_warn("Cannot find Prettier config file defined "
                         "in 'additional_cli_args' -> '--config <path>'.", True)

                return None

        #
        # 2. Attempt to resolve a prettier config path:
        resolved_prettier_config = find_prettier_config(source_file_dir)
        if resolved_prettier_config and os.path.exists(resolved_prettier_config):
            log_debug(view, "Prettier config file discovered at '{0}'".format(resolved_prettier_config))
            return resolved_prettier_config

        log_debug(view, "Prettier config file not found. "
                        "Will use Prettier options defined in Sublime Text '{0}' file."
                  .format(SETTINGS_FILENAME), True)

        return None

    def run(self, edit, save_file=False, auto_format_prettier_config_path=None):
        view = self.view
        source_file_path = view.file_name()

        if source_file_path is None:
            #
            # Handle file must first be saved:
            if IS_ST3:
                # sublime text 3+: show dialog that includes a save option:
                result = sublime.yes_no_cancel_dialog(
                    '{0}\n\n'
                    'File must first be Saved.'.format(PLUGIN_NAME),
                    'Save...', "Don't Save")
                if result == sublime.DIALOG_YES:
                    view.run_command('save')
            else:
                # sublime text 2x: limited dialog support, just show error:
                return sublime.error_message(
                    '{0} Error\n\n'
                    'File must first be saved.'.format(PLUGIN_NAME))

        #
        # set paths
        if source_file_path is None:
            # Re-check if file was saved, in case user canceled or closed the save dialog:
            return st_status_message('Save canceled.')

        #
        # Max file size check
        if self.exceeds_max_file_size_limit(source_file_path):
            return st_status_message('Maximum file size reached.')

        source_file_dir = get_file_abs_dir(source_file_path)
        st_project_path = str(get_st_project_path())

        #
        # cd to the active sublime text project dir:
        os.chdir(st_project_path)

        #
        # if a `--config <path>` option is set in 'additional_cli_args',
        # no action is necessary. otherwise, try to sniff the config
        # file path:
        parsed_additional_cli_args = parse_additional_cli_args(self.additional_cli_args)
        has_custom_config_defined = parsed_additional_cli_args.count('--config') > 0
        has_no_config_defined = parsed_additional_cli_args.count('--no-config') > 0
        has_config_precedence_defined = parsed_additional_cli_args.count('--config-precedence') > 0

        prettier_config_path = None
        if not has_no_config_defined:
            if save_file and auto_format_prettier_config_path and os.path.exists(auto_format_prettier_config_path):
                prettier_config_path = auto_format_prettier_config_path
            if not prettier_config_path:
                resolved_prettier_config = self.try_find_prettier_config(view)
                if resolved_prettier_config and os.path.exists(resolved_prettier_config):
                    prettier_config_path = resolved_prettier_config
        if not prettier_config_path or not os.path.exists(prettier_config_path):
            prettier_config_path = ''
            has_custom_config_defined = False

        #
        # Get node and prettier command paths:
        node_path = self.node_path
        prettier_cli_path = resolve_prettier_cli_path(view, PLUGIN_PATH, st_project_path)
        if not prettier_cli_path:
            log_error(
                "Ensure 'prettier' is installed in your environment PATH, "
                "or manually specify an absolute path in your '{0}' file "
                "and the 'prettier_cli_path' setting.".format(SETTINGS_FILENAME))
            return st_status_message('Prettier not found. Open console for more details.')

        # try to find a '.prettierignore' file path in the project root
        # if the '--ignore-path' option isn't specified in 'additional_cli_args':
        prettier_ignore_filepath = None
        if not parsed_additional_cli_args.count('--ignore-path') > 0:
            prettier_ignore_filepath = resolve_prettier_ignore_path(source_file_dir, st_project_path)

        #
        # Parse prettier options:
        prettier_options = self.parse_prettier_options(
            view, parsed_additional_cli_args, prettier_config_path,
            has_custom_config_defined, has_no_config_defined,
            has_config_precedence_defined, prettier_ignore_filepath,
            source_file_path)

        #
        # Format entire file:
        if not has_selection(view) or save_file is True:
            region = sublime.Region(0, view.size())
            source = view.substr(region)
            if is_str_empty_or_whitespace_only(source):
                return st_status_message('Nothing to format in file.')

            transformed = self.format_code(source, node_path, prettier_cli_path, prettier_options, view)
            if self.has_error:
                self.format_console_error()
                return self.show_status_bar_error()

            # sanity check to ensure textual content was returned from cmd
            # stdout, not necessarily caught in OSError try/catch
            # exception handler
            if is_str_empty_or_whitespace_only(transformed):
                self.error_message = 'Empty content returned to stdout'
                return self.show_status_bar_error()

            source_modified = False
            transformed = trim_trailing_ws_and_lines(transformed)
            if transformed:
                if transformed == trim_trailing_ws_and_lines(source):
                    if self.ensure_newline_at_eof(view, edit) is True:
                        # no formatting changes applied, however, a line
                        # break was needed/inserted at the end of the file:
                        source_modified = True
                else:
                    view.replace(edit, region, transformed)
                    self.ensure_newline_at_eof(view, edit)
                    source_modified = True
            else:
                view.replace(edit, region, transformed)
                self.ensure_newline_at_eof(view, edit)
                source_modified = True

            if source_modified:
                st_status_message('File formatted.')
            else:
                st_status_message('File already formatted.')
            return

        #
        # Format each selection:
        for region in view.sel():
            if region.empty():
                continue

            source = view.substr(region)
            if is_str_empty_or_whitespace_only(source):
                st_status_message('Nothing to format in selection.')
                continue

            transformed = self.format_code(source, node_path, prettier_cli_path, prettier_options, view)
            if self.has_error:
                self.format_console_error()
                return self.show_status_bar_error()

            # sanity check to ensure textual content was returned from cmd
            # stdout, not necessarily caught in OSError try/catch
            # exception handler
            if is_str_empty_or_whitespace_only(transformed):
                self.error_message = 'Empty content returned to stdout'
                return self.show_status_bar_error()

            transformed = trim_trailing_ws_and_lines(transformed)
            if transformed and transformed == trim_trailing_ws_and_lines(source):
                st_status_message('Selection(s) already formatted.')
            else:
                view.replace(edit, region, transformed)
                st_status_message('Selection(s) formatted.')

    def format_code(self, source, node_path, prettier_cli_path, prettier_options, view):
        self._error_message = None

        if is_str_none_or_empty(node_path):
            cmd = [prettier_cli_path] \
                + ['--stdin'] \
                + prettier_options
        else:
            cmd = [node_path] \
                + [prettier_cli_path] \
                + ['--stdin'] \
                + prettier_options

        try:
            format_debug_message('Prettier CLI Command', list_to_str(cmd), debug_enabled(view))

            proc = Popen(
                cmd, stdin=PIPE,
                stderr=PIPE,
                stdout=PIPE,
                env=get_proc_env(),
                shell=is_windows())

            stdout, stderr = proc.communicate(input=source.encode('utf-8'))
            if proc.returncode != 0:
                error_output = stderr.decode('utf-8')
                self.error_message = format_error_message(error_output, str(proc.returncode))

                # detect and scroll to 'Syntax Errors':
                _, _, error_line, error_col = self.has_syntax_error(error_output)
                if error_line != -1 and error_col != -1:
                    scroll_view_to(view, error_line, error_col)

                return None
            if stderr:
                # allow warnings to pass-through
                print(format_error_message(stderr.decode('utf-8'), str(proc.returncode)))
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
        if is_file_auto_formattable(view) is True:
            return True
        return False

    def is_visible(self):
        return self.should_show_plugin()

    def is_enabled(self):
        return self.should_show_plugin()

    def parse_prettier_options(self, view, parsed_additional_cli_args,
                               prettier_config_path, has_custom_config_defined,
                               has_no_config_defined, has_config_precedence_defined,
                               prettier_ignore_filepath, file_name):
        prettier_options = []

        #
        # Check for prettier config file:
        prettier_config_exists = not is_str_none_or_empty(prettier_config_path)
        if prettier_config_exists:
            if not has_custom_config_defined:
                # only add the '--config <path>' option if it's not
                # already specified as an additional cli arg:
                prettier_options.append('--config')
                prettier_options.append(prettier_config_path)

                # set config-precedence to 'prefer-file' if
                # the key wasn't defined in additional_cli_args:
                if not has_config_precedence_defined:
                    prettier_options.append('--config-precedence')
                    prettier_options.append('cli-override')
        else:
            if not has_no_config_defined and not has_custom_config_defined:
                # only add the '--no-config' option if it's not
                # already specified as an additional cli arg:
                prettier_options.append('--no-config')

        #
        # Iterate over option map:
        for mapping in PRETTIER_OPTION_CLI_MAP:
            option_name = mapping['option']
            cli_option_name = mapping['cli']
            option_value = get_sub_setting(self.view, option_name)

            if option_name == 'parser':
                if self.is_css(view):
                    prettier_options.append(cli_option_name)
                    prettier_options.append('css')
                    continue

                if self.is_typescript(view):
                    prettier_options.append(cli_option_name)
                    prettier_options.append('typescript')
                    continue

                if self.is_json(view):
                    prettier_options.append(cli_option_name)
                    prettier_options.append('json')
                    continue

                if self.is_graphql(view):
                    prettier_options.append(cli_option_name)
                    prettier_options.append('graphql')
                    continue

                if self.is_markdown(view):
                    prettier_options.append(cli_option_name)
                    prettier_options.append('markdown')
                    continue

                if self.is_vue(view):
                    prettier_options.append(cli_option_name)
                    prettier_options.append('vue')
                    continue

            if not prettier_config_exists and not has_custom_config_defined:
                # add the cli args or the respective defaults:
                if option_value is None or str(option_value) == '':
                    option_value = mapping['default']
                option_value = str(option_value).strip()
                if is_bool_str(option_value):
                    option_value = option_value.lower()
                prettier_options.append(cli_option_name)
                prettier_options.append(option_value)

        # set the `tabWidth` option based on the current view:
        prettier_options.append('--tab-width')
        prettier_options.append(str(self.tab_size))

        # set the `useTabs` option based on the current view:
        prettier_options.append('--use-tabs')
        prettier_options.append(str(self.use_tabs).lower())

        # add the current file name to `--stdin-filepath`, only when
        # the current file being edited is NOT html, and in order
        # detect and format css/js selection(s) within html files:
        if not self.is_html(view):
            prettier_options.append('--stdin-filepath')
            prettier_options.append(file_name)

        if prettier_ignore_filepath is not None:
            prettier_options.append('--ignore-path')
            prettier_options.append(prettier_ignore_filepath)

        # Append any additional specified arguments:
        prettier_options.extend(parsed_additional_cli_args)

        return prettier_options

    def format_console_error(self):
        print('\n------------------\n {0} ERROR \n------------------\n\n'
              '{1}'.format(PLUGIN_NAME, self.error_message))

    @staticmethod
    def has_syntax_error(error_output):
        error = None
        message = ''
        line = -1
        col = -1
        match_groups = search(
            r'^.+?:\s(?:(?P<error>SyntaxError)):\s(?P<message>.+) \((?P<line>\d+):(?P<col>\d+)\)', error_output)
        if match_groups:
            error = match_groups.group('error')
            message = match_groups.group('message')
            line = int(match_groups.group('line'))
            col = int(match_groups.group('col'))
        return error, message, line, col

    @staticmethod
    def is_source_js(view):
        scopename = view.scope_name(view.sel()[0].b)
        if scopename.startswith('source.js') or contains('source.js.embedded.html', scopename):
            return True
        return False

    @staticmethod
    def is_css(view):
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(view.sel()[0].b)
        if scopename.startswith('source.css') or filename.endswith('.css') or contains('meta.selector.css', scopename):
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
    def is_json(view):
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(0)
        if scopename.startswith('source.json') or filename.endswith('.json'):
            return True
        return False

    @staticmethod
    def is_graphql(view):
        filename = view.file_name()
        if not filename:
            return False
        if filename.endswith('.graphql') or filename.endswith('.gql'):
            return True
        return False

    @staticmethod
    def is_html(view):
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(0)
        if scopename.startswith('text.html.markdown') or scopename.startswith('text.html.vue'):
            return False
        if scopename.startswith('text.html') or filename.endswith('.html') or filename.endswith('.htm'):
            return True
        return False

    @staticmethod
    def is_markdown(view):
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(0)
        if scopename.startswith('text.html.markdown') or filename.endswith('.md'):
            return True
        return False

    @staticmethod
    def is_vue(view):
        filename = view.file_name()
        if not filename:
            return False
        scopename = view.scope_name(0)
        if scopename.startswith('text.html.vue') or filename.endswith('.vue'):
            return True
        return False

    @staticmethod
    def show_status_bar_error():
        st_status_message('Format failed! Open the console window to inspect errors.')

    @staticmethod
    def ensure_newline_at_eof(view, edit):
        new_line_inserted = False
        if view.size() > 0 and view.substr(view.size() - 1) != '\n':
            new_line_inserted = True
            view.insert(edit, view.size(), '\n')
        return new_line_inserted


class CommandOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if self.is_allowed(view) and self.is_enabled(view) and self.is_excluded(view):
            if self.get_auto_format_on_save_requires_prettier_config(view) is True:
                resolved_prettier_config = self.try_find_prettier_config(view)
                if not resolved_prettier_config:
                    return
                view.run_command(PLUGIN_CMD_NAME, {
                    'save_file': True,
                    'auto_format_prettier_config_path': resolved_prettier_config
                })
                return
            else:
                view.run_command(PLUGIN_CMD_NAME, {
                    'save_file': True,
                    'auto_format_prettier_config_path': None
                })

    def try_find_prettier_config(self, view):
        source_file_dir = get_file_abs_dir(view.file_name())
        st_project_path = get_st_project_path()

        #
        # 1. Attempt to use prettier config defined in the 'additional_cli_args' (if exist - ensure it's abs path)
        additional_cli_arg_config = get_cli_arg_value(self.get_additional_cli_args(view), '--config')
        if not is_str_none_or_empty(additional_cli_arg_config):
            additional_cli_arg_config = os.path.normpath(additional_cli_arg_config)
            if not os.path.isabs(additional_cli_arg_config):
                additional_cli_arg_config = in_source_file_path_or_project_root(
                    source_file_dir, st_project_path, additional_cli_arg_config)
                if additional_cli_arg_config and os.path.exists(additional_cli_arg_config):
                    return additional_cli_arg_config
                return None

        #
        # 2. Attempt to resolve a prettier config path:
        resolved_prettier_config = find_prettier_config(source_file_dir)
        if resolved_prettier_config and os.path.exists(resolved_prettier_config):
            return resolved_prettier_config

        return None

    @staticmethod
    def get_auto_format_on_save(view):
        return bool(get_setting(view, 'auto_format_on_save', False))

    @staticmethod
    def get_auto_format_on_save_excludes(view):
        return get_setting(view, 'auto_format_on_save_excludes', [])

    @staticmethod
    def get_custom_file_extensions(view):
        return get_setting(view, 'custom_file_extensions', [])

    @staticmethod
    def get_auto_format_on_save_requires_prettier_config(view):
        return bool(get_setting(view, 'auto_format_on_save_requires_prettier_config', False))

    @staticmethod
    def is_allowed(view):
        return is_file_auto_formattable(view)

    @staticmethod
    def get_additional_cli_args(view):
        return dict(get_setting(view, 'additional_cli_args', {}))

    def is_enabled(self, view):
        return self.get_auto_format_on_save(view)

    def is_excluded(self, view):
        filename = view.file_name()
        if not filename:
            return False
        excludes = self.get_auto_format_on_save_excludes(view)
        regmatch_ef = [fnmatch.translate(os.path.normpath(pattern)) for pattern in excludes]
        for regmatch in regmatch_ef:
            if match(regmatch, filename):
                return False
        return True
