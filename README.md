# JsPrettier

[![Travis CI Build Status](https://travis-ci.org/jonlabelle/SublimeJsPrettier.svg?branch=master)](https://travis-ci.org/jonlabelle/SublimeJsPrettier)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/ta7379jk57cdwu76/branch/master?svg=true)](https://ci.appveyor.com/project/jonlabelle/sublimejsprettier/branch/master)
[![SonarQube Quality Gate Status](https://sonarcloud.io/api/badges/gate?key=org.jonlabelle-github:SublimeJsPrettier)](https://sonarcloud.io/dashboard/index/org.jonlabelle-github:SublimeJsPrettier)
[![Package Control Installs](https://img.shields.io/packagecontrol/dt/JsPrettier.svg?label=installs)](https://packagecontrol.io/packages/JsPrettier)
[![Latest Release](https://img.shields.io/github/tag/jonlabelle/SublimeJsPrettier.svg?label=version)](https://github.com/jonlabelle/SublimeJsPrettier/releases)

[JsPrettier] is a Sublime Text Plug-in for [Prettier], the opinionated code
formatter.

[![](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/before_and_after.gif?raw=true)](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/demo.gif)

> [Watch a Quick Demo]

---

<details>
<summary><strong>Table of Contents</strong></summary>

- [Installation](#installation)
    - [Requirements](#requirements)
    - [Install Prettier](#install-prettier)
    - [Install JsPrettier via Package Control](#install-jsprettier-via-package-control)
    - [Install JsPrettier Manually](#install-jsprettier-manually)
    - [Install JsPrettier Using Git](#install-jsprettier-using-git)
- [Usage](#usage)
    - [Command Scope](#command-scope)
    - [Custom Key Binding](#custom-key-binding)
- [Settings](#settings)
    - [Sublime Text Settings](#sublime-text-settings)
    - [Prettier Options](#prettier-options)
    - [Project-level Settings](#project-level-settings)
- [Issues](#issues)
- [Changes](#changes)
- [Author](#author)
- [License](#license)

</details>

## Installation

[JsPrettier] is compatible with both Sublime Text 2 and 3, and all supported
Operating Systems.

### Requirements

JsPrettier requires the following programs to be installed prior to use:

- [Sublime Text] – Text editor for code
- [node.js] – JavaScript runtime
- [yarn] or [npm] – Package manager for JavaScript
- [Prettier] – Opinionated JavaScript formatter

### Install Prettier

If you installed [Prettier] globally (using the [yarn] or [npm] command below),
there is nothing else you need to do.

```bash
# using yarn:
yarn global add prettier

# using npm:
npm install -g prettier
```

### Install JsPrettier via Package Control

The easiest and recommended way to install Js​Prettier is
using [Package Control].

From the **main application menu**, navigate to:

- `Tools` -> `Command Palette...` -> `Package Control: Install Package`, type
  the word **JsPrettier**, then select it to complete the installation.

### Install JsPrettier Manually

1. Download and extract Js​Prettier [zip file] to your
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
(<kbd>super + shift + p</kbd>) and type ***JsPrettier: Format Code***.

You can also right-click anywhere in the file to bring up the **Context Menu**
and select ***JsPrettier Format Code***.

### Command Scope

`JsPrettier` will attempt to format selections of code first, otherwise the
entire file will be formatted.

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
    Whether or not to automatically format on every file save.

- **auto_format_on_save_excludes** (default: ["\*/node_modules/\*", "\*/.git/\*"])
    Ignore auto formatting when the target file, or its path resides in a
    particular location, and when `auto_format_on_save` is turned on.

    **Example:**

        [
            "*/node_modules/*",
            "*/file.js",
            "*.json"
        ]

- **allow_inline_formatting** (default: ***false***)
    Enables the ability to format *selections* of in-lined code. For example, to
    format a selection of JavaScript code within a PHP or HTML file. When
    ***true***, the JsPrettier command is available for use across all Sublime
    Text syntaxes.

- **custom_file_extensions** (default: [])
    There's built-in support already for `js`, `jsx`, `json`, `graphql/gql`,
    `ts`, `tsx`, `css`, `scss` and `less` files. Any additional file
    extensions must be specified here, without the leading dot.

- **max_file_size_limit** (default: ***-1***)
    The maximum allowed file size to format in bytes. For performance reasons,
    files with a greater file size than the specified `max_file_size_limit` will
    not be formatted. Setting the `max_file_size_limit` value to ***-1*** will
    disable file size checking (default).

- **additional_cli_args** (default: {})
    A key-value pair of additional arguments to append to the prettier command.

    **Examples:**

        {
            "--config": "path/to/my/custom/.prettierrc",
            "--no-config": "",
            "--with-node-modules": ""
            "--ignore-path": "path/to/.prettierignore"
            "--config-precedence": "file-override"
        }

    > **NOTE:** If choosing to specify additional CLI args, it is assumed that
    > each argument is supported by the [Prettier CLI]. Otherwise, the command
    > will fail to run, and errors will be dumped out to
    > the [Sublime Text Console]. You can also enable the `debug` setting to
    > inspect the generated command-line output passed to prettier; which is
    > also useful for quickly troubleshooting issues.

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
    Which parser to use. Valid options are "***flow***", "***babylon***",
    "***typescript***" and "***postcss***".

    > If CSS or TypeScript is detected in Sublime Text, the parser option will
    > *always* be internally overridden and set to "***postcss***" or
    > "***typescript***" respectively.

- **semi** (default: ***true***)
    ***true*** to add a semicolon at the end of every line, or ***false*** to
    add a semicolon only at the beginning of lines that may introduce ASI
    failures.

> For further details and examples of setting Prettier's options, please see the
> [Prettier API section] on the Prettier homepage.

#### Prettier Configuration Files

When [Prettier Configuration files] are detected, Prettier options defined in
Sublime Text settings files will be ignored, with the exception of `parser`,
`tabWidth` and `useTabs`; which are auto-detected based on file or selection.

> *The configuration file will be resolved starting from the location of the file
> being formatted, and searching up the file tree until a config file is (or
> isn't) found.*

##### Custom Prettier Config File Path

To specify a custom Prettier config path, simply add the `--config` argument
with an appropriate path to the `additional_cli_args` setting. Here's an
example.

```json
{
    "additional_cli_args": {
        "--config": "path/to/my/custom/.prettierrc"
    }
}
```

##### Disable Prettier Config File Discovery

You can also add the `--no-config` option to the `additional_cli_args` setting,
and tell Prettier not to attempt to find config files.

```json
{
    "additional_cli_args": {
        "--no-config": ""
    }
}
```

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
            "auto_format_on_save_excludes": ["*/node_modules/*", "*/.git/*"],
            "allow_inline_formatting": false,
            "custom_file_extensions": [],
            "max_file_size_limit": -1,
            "additional_cli_args": {},
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
[Prettier CLI]: https://github.com/prettier/prettier#cli
[Package Control]: https://packagecontrol.io/packages/JsPrettier
[Sublime Text]: https://www.sublimetext.com
[JsPrettier]: https://github.com/jonlabelle/SublimeJsPrettier
[node.js]: https://nodejs.org
[Project-level Settings]: http://docs.sublimetext.info/en/latest/reference/projects.html
[***tab_size***]: http://docs.sublimetext.info/en/latest/reference/settings.html#whitespace-and-indentation
[***translate_tabs_to_spaces***]: http://docs.sublimetext.info/en/latest/reference/settings.html#whitespace-and-indentation
[installed globally]: #install-prettier
[yarn]: https://yarnpkg.com/
[npm]: https://www.npmjs.com/
[nvm]: https://github.com/creationix/nvm
[zip file]: https://github.com/jonlabelle/SublimeJsPrettier/archive/master.zip
[Sublime Text Packages directory]: #default-st-paths
[manual download instructions]: #manual-download
[Sublime Text Console]: http://docs.sublimetext.info/en/latest/basic_concepts.html#sublime-text-is-programmable
[custom key binding]: http://docs.sublimetext.info/en/latest/customization/key_bindings.html
[Prettier Configuration files]: https://github.com/prettier/prettier/blob/master/README.md#configuration-file
[issue template]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/.github/ISSUE_TEMPLATE.md
[report an issue]: https://github.com/jonlabelle/SublimeJsPrettier/issues
[Changelog]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/CHANGELOG.md
[MIT License]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/LICENSE.txt
