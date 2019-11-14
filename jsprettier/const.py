from __future__ import absolute_import
from __future__ import print_function

import os
import re

from sys import version_info

import sublime

IS_PY2 = version_info[0] == 2
IS_ST3 = int(sublime.version()) >= 3000

PLUGIN_NAME = 'JsPrettier'
PLUGIN_CMD_NAME = 'js_prettier'
PROJECT_SETTINGS_KEY = PLUGIN_CMD_NAME
SETTINGS_FILENAME = '{0}.sublime-settings'.format(PLUGIN_NAME)
PRETTIER_OPTIONS_KEY = 'prettier_options'

PLUGIN_PATH = os.path.join(sublime.packages_path(), os.path.dirname(os.path.realpath(__file__)))

SYNTAX_ERROR_RE = re.compile(
    r'^.+?:\s(?:(?P<error>SyntaxError)):\s(?P<message>.+) \((?P<line>\d+):(?P<col>\d+)\)',
    re.MULTILINE
)

# ref: https://prettier.io/docs/en/configuration.html
PRETTIER_CONFIG_FILES = [
    '.prettierrc',
    '.prettierrc.json',
    '.prettierrc.js',
    'prettier.config.js',
    'package.json',
    '.prettierrc.yml',
    '.prettierrc.yaml',
    '.prettierrc.toml'
]

PRETTIER_IGNORE_FILE = '.prettierignore'

PRETTIER_OPTION_CLI_MAP = [
    {
        'option': 'printWidth',
        'cli': '--print-width',
        'default': '80'
    },
    {
        'option': 'tabWidth',
        'cli': '--tab-width',
        'default': '2'
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
        'default': 'babel'
    },
    {
        'option': 'semi',
        'cli': '--semi',
        'default': 'true'
    },
    {
        'option': 'requirePragma',
        'cli': '--require-pragma',
        'default': 'false'
    },
    {
        'option': 'proseWrap',
        'cli': '--prose-wrap',
        'default': 'preserve'
    },
    {
        'option': 'arrowParens',
        'cli': '--arrow-parens',
        'default': 'avoid'
    },
    {
        'option': 'htmlWhitespaceSensitivity',
        'cli': '--html-whitespace-sensitivity',
        'default': 'css'
    },
    {
        'option': 'quoteProps',
        'cli': '--quote-props',
        'default': 'as-needed'
    },
    {
        'option': 'vueIndentScriptAndStyle',
        'cli': '--vue-indent-script-and-style',
        'default': 'false'
    }
]

AUTO_FORMAT_FILE_EXTENSIONS = [
    'js',
    'jsx',
    'json',
    'graphql',
    'gql',
    'html',
    'ts',
    'tsx',
    'css',
    'scss',
    'less',
    'md',
    'vue',
    'yml',
    'mjs',
    'mdx'
]
