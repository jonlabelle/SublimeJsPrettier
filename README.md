# Sublime Text JavaScript Prettier

[![Build Status](https://travis-ci.org/jonlabelle/SublimeJsPrettier.svg?branch=master)](https://travis-ci.org/jonlabelle/SublimeJsPrettier)
[![Build status](https://ci.appveyor.com/api/projects/status/ta7379jk57cdwu76/branch/master?svg=true)](https://ci.appveyor.com/project/jonlabelle/sublimejsprettier/branch/master)
[![Downloads](https://packagecontrol.herokuapp.com/downloads/JsPrettier.svg?color=80d4cd)](https://packagecontrol.io/packages/JsPrettier)

[JsPrettier] is a Sublime Text Plug-in for [Prettier], the opinionated
JavaScript formatter.

[![](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/before_and_after.gif?raw=true)](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/demo.gif)

- [Watch a Quick Demo]

## Installation

Sublime Text JavaScript Prettier ([JsPrettier]) is compatible with both Sublime
Text 2 and 3, and all supported Operating Systems.

### Requirements

The Sublime Text JavaScript Prettier plug-in requires the following programs to
be installed:

- [Sublime Text] – Text editor for code
- [node.js] – JavaScript runtime
- [npm] – Package manager for JavaScript
- [Prettier] – Opinionated JavaScript formatter

### Install Prettier

If you installed [Prettier] globally (using the [npm] command below), there is
nothing else you need to do.

    npm install -g prettier

### Install JsPrettier via Package Control

The easiest and recommended way to install Sublime Text JavaScript Prettier is
using [Package Control].

From the **main application menu**, navigate to:

- `Tools` -> `Command Palette...` -> `Package Control: Install Package`, type
  the word **JsPrettier**, then select it to complete the installation.

### Install JsPrettier Manually

1. Download and extract Sublime Text JavaScript Prettier [zip file] to your
   [Sublime Text Packages directory].
2. Rename the extracted directory from `SublimeJsPrettier-master` to
   `JsPrettier`.

**Default Sublime Text Packages Paths:**
<a name="default-st-paths"></a>

- **OS X:** `~/Library/Application Support/Sublime Text [2|3]/Packages`
- **Linux:** `~/.Sublime Text [2|3]/Packages`
- **Windows:** `%APPDATA%/Sublime Text [2|3]/Packages`

> **NOTE** Replace the `[2|3]` part with the appropriate Sublime Text
> version for your installation.

### Install JsPrettier Using Git

Alternatively, if you're a Git user, you can install [JsPrettier] and keep it
up-to-date by cloning the repository directly into your [Sublime Text Packages directory].

You can locate your Sublime Text Packages directory by using the menu item
`Preferences` -> `Browse Packages...`

    git clone https://github.com/jonlabelle/SublimeJsPrettier.git "JsPrettier"

## Usage

To run the `JsPrettier` command... open the Sublime Text **Command Palette**
(<kbd>super + shift + p</kbd>) and type ***JsPrettier***.

You can also right-click anywhere in the view to bring up the **Context Menu**,
and select ***JsPrettier***.

### Command Scope

`JsPrettier` will attempt to format any selected JavaScript sections of code
first; if no selections are made, the entire file will be formatted.

> **NOTE:** When the `auto_format_on_save` setting is set to `true`, the
> **entire file** will always be formatted.

### Custom Key Binding

To add a [custom key binding] to `JsPrettier`, please reference the following
example which binds `js_prettier` to <kbd>ctrl/cmd + b</kbd>.

```json
{ "keys": ["super+b"], "command": "js_prettier" }
```

## Settings

All [Prettier] options are configurable from the `JsPrettier.sublime-settings`
file, accessible from the **Preferences** > **Package Settings** >
***JsPrettier*** menu shortcut.

### Sublime Text Settings

- **debug** (default: ***false***)  
    When enabled (*true*), additional debugging information about the command
    and configured settings will be printed to the Sublime Text Console; useful
    for troubleshooting purposes.
  
- **prettier_cli_path** (default: ***empty***)  
    It's recommended to leave this setting empty (the default). However, if
    Sublime Text has problems resolving the CLI path to the [Prettier]
    executable, you can explicitly set the appropriate path here.
  
    When the setting is left empty, the path is resolved by searching locations
    in the following order, returning the first matched path:
  
    - Locally installed Prettier, relative to the Sublime Text Project file root
      directory, e.g.: `node_modules/.bin/prettier`.
    - The user's home directory, e.g.: `$HOME/node_modules/.bin/prettier`.
    - Look in the *JsPrettier* Sublime Text plug-in directory for
      `node_modules/.bin/prettier`.
    - Finally, check if Prettier is [installed globally].
  
    > [nvm] users are required to set an appropriate absolute
    > *prettier_cli_path* (and absolute *node_path*); according to the target
    > runtime environment.
  
- **node_path** (default: ***empty***)  
    It's recommended to leave this setting empty (the default). However, if
    Sublime Text has problems resolving the absolute path to the node
    executable, you can explicitly set the appropriate path here.
  
    > [nvm] users are required to set an appropriate absolute *node_path* (and
    > absolute *prettier_cli_path*); according to the target runtime
    > environment.
  
- **auto_format_on_save** (default: ***false***)  
    Whether or not to automatically format on every file save (`.js` and `.jsx`
    files only).
  
- **allow_inline_formatting** (default: ***false***)  
    Provides the ability to format *selections* of in-lined JavaScript code,
    outside of the normal JavaScript syntax. For example, to format a selection
    of JavaScript code within a PHP or HTML file. When ***true***, the JsPrettier
    command is available for use across all Sublime Text syntaxes.

### Prettier Options

- **useTabs** (internally set by the [***translate_tabs_to_spaces***] setting)  
    Indent lines with tabs.

- **printWidth** (default: ***80***)  
    Specifies that the formatted code should fit within this line limit.
  
- **tabWidth** (internally set by the [***tab_size***] setting)  
    The number of spaces to use per tab.
  
- **singleQuote** (default: ***false***)  
    If true, code will be formatted using single-quotes, instead of double-quotes.
  
- **trailingComma** (default: "***none***")  
   Controls the printing of trailing commas wherever possible. Valid options:
    - "***none***" – No trailing commas
    - "***es5***"  – Trailing commas where valid in ES5 (objects, arrays, etc)
    - "***all***"  – Trailing commas wherever possible (function arguments)
  
- **bracketSpacing** (default: ***true***)  
    Controls the printing of spaces inside object literals.
  
- **jsxBracketSameLine** (default: ***false***)  
    When *true*, right-angle brackets ("&gt;") of multi-line jsx elements
    will be placed at the end of the last line, instead of being alone on the
    next line.
  
- **parser** (default: "***babylon***")  
    Which parser to use. Valid options are "***flow***" and "***babylon***".
  
- **semi** (default: ***true***)  
    ***true*** to add a semicolon at the end of every line, or ***false*** to
    add a semicolononly at the beginning of lines that may introduce ASI
    failures.

> *For further details and examples of setting Prettier's options, please see
> the [Prettier API section] on the Prettier homepage.*

### Project-level Settings

JsPrettier supports [Project-level settings], specified in
`<project_name>.sublime-project` files. In order for Project-level settings to
override the Defaults and User configured settings, a new `js_prettier` section
must be created under the project file's `settings` section.

#### Example Sublime Text Project File

```json
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "js_prettier": {
            "debug": false,
            "prettier_cli_path": "",
            "node_path": "",
            "auto_format_on_save": false,
            "allow_inline_formatting": false,
            "prettier_options": {
                "printWidth": 80,
                "singleQuote": false,
                "trailingComma": "none",
                "bracketSpacing": true,
                "jsxBracketSameLine": false,
                "parser": "babylon",
                "semi": true
            }
        }
    }
}
```

## Issues

To [report an issue], please follow the steps outlined in the [Issue Template].

## Changes

Please visit the [Changelog] page for a complete list of changes.

## Author

Jon LaBelle

## License

[MIT License]

[Watch a Quick Demo]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/demo.gif
[Prettier]: https://github.com/jlongster/prettier
[Prettier API section]: https://github.com/prettier/prettier#api
[Package Control]: https://packagecontrol.io/packages/JsPrettier
[Sublime Text]: https://www.sublimetext.com
[JsPrettier]: https://github.com/jonlabelle/SublimeJsPrettier
[node.js]: https://nodejs.org
[Project-level Settings]: http://docs.sublimetext.info/en/latest/reference/projects.html
[***tab_size***]: http://docs.sublimetext.info/en/latest/reference/settings.html
[***translate_tabs_to_spaces***]: http://docs.sublimetext.info/en/latest/reference/settings.html
[installed globally]: #install-prettier
[npm]: https://www.npmjs.com
[nvm]: https://github.com/creationix/nvm
[zip file]: https://github.com/jonlabelle/SublimeJsPrettier/archive/master.zip
[Sublime Text Packages directory]: #default-st-paths
[manual download instructions]: #manual-download
[custom key binding]: http://docs.sublimetext.info/en/latest/customization/key_bindings.html
[issue template]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/.github/ISSUE_TEMPLATE.md
[report an issue]: https://github.com/jonlabelle/SublimeJsPrettier/issues
[Changelog]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/CHANGELOG.md
[MIT License]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/LICENSE.txt
