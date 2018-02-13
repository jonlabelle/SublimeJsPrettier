from __future__ import absolute_import
from __future__ import print_function


PLUGIN_NAME = 'JsPrettier'
PLUGIN_CMD_NAME = 'js_prettier'
PROJECT_SETTINGS_KEY = PLUGIN_CMD_NAME
SETTINGS_FILENAME = '{0}.sublime-settings'.format(PLUGIN_NAME)
PRETTIER_OPTIONS_KEY = 'prettier_options'

# https://prettier.io/docs/en/configuration.html
PRETTIER_CONFIG_FILES = [
    '.prettierrc',
    '.prettierrc.yml',
    '.prettierrc.yaml',
    '.prettierrc.json',
    '.prettierrc.js',
    'prettier.config.js',
    'package.json'
]

PRETTIER_IGNORE_FILE = '.prettierignore'

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
    }
]

AUTO_FORMAT_FILE_EXTENSIONS = [
    'js',
    'jsx',
    'json',
    'graphql',
    'gql',
    'ts',
    'tsx',
    'css',
    'scss',
    'less',
    'md',
    'vue'
]
