# JsPrettier

[![Travis CI Build Status](https://travis-ci.org/jonlabelle/SublimeJsPrettier.svg?branch=master)](https://travis-ci.org/jonlabelle/SublimeJsPrettier)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/ta7379jk57cdwu76/branch/master?svg=true)](https://ci.appveyor.com/project/jonlabelle/sublimejsprettier/branch/master)
[![SonarQube Quality Gate Status](https://sonarcloud.io/api/badges/gate?key=org.jonlabelle-github:SublimeJsPrettier)](https://sonarcloud.io/dashboard/index/org.jonlabelle-github:SublimeJsPrettier)
[![Package Control Installs](https://img.shields.io/packagecontrol/dt/JsPrettier.svg?label=installs)](https://packagecontrol.io/packages/JsPrettier)
[![Latest Release](https://img.shields.io/github/tag/jonlabelle/SublimeJsPrettier.svg?label=version)](https://github.com/jonlabelle/SublimeJsPrettier/releases)

> [JsPrettier] is a Sublime Text Plug-in for [Prettier], the opinionated code
> formatter.

[![Before and After JsPrettier](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/before_and_after.gif?raw=true)](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/demo.gif)

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
    - [Prettier Configuration Files](#prettier-configuration-files)
- [Issues](#issues)
- [Changes](#changes)
- [Author](#author)
- [License](#license)

</details>

## Installation

[JsPrettier] is compatible with both Sublime Text 2 and 3, and all supported
Operating Systems.

### Requirements

- [Sublime Text] - Text editor for code
- [node.js] - JavaScript runtime
- [yarn] or [npm] - Package manager for JavaScript
- [Prettier] - Opinionated JavaScript formatter

### Install Prettier

If you installed [Prettier] globally (using the [yarn] or [npm] command below),
there's nothing else you need to do.

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

If you're a Git user, you can install [JsPrettier] and keep it up-to-date by
cloning the repository directly into your [Sublime Text Packages directory].

You can locate your Sublime Text Packages directory by using the menu item
`Preferences` -> `Browse Packages...`

    git clone https://github.com/jonlabelle/SublimeJsPrettier.git "JsPrettier"

## Usage

To run the `JsPrettier` command... open the Sublime Text **Command Palette**
(<kbd>super + shift + p</kbd>) and type ***JsPrettier: Format Code***.

You can also right-click anywhere in the file to bring up the **Context Menu**
and select ***JsPrettier Format Code***.

### Command Scope

`JsPrettier` will attempt to format selections of code first, then the entire
file.

> **NOTE:** When `auto_format_on_save` is `true`, the **entire file** will be
> formatted.

### Custom Key Binding

To add a [custom key binding] to `JsPrettier`, please reference the following
example which binds `js_prettier` to <kbd>ctrl/cmd + alt + f</kbd>.

```json
{ "keys": ["super+alt+f"], "command": "js_prettier" }
```

## Settings

All [Prettier] options are configurable from the `JsPrettier.sublime-settings`
file, accessible from the **Preferences** > **Package Settings** >
***JsPrettier*** menu shortcut.

### Sublime Text Settings

- **debug** (default: ***false***)  
    When enabled (*true*), debug info will print to the console - useful for
    troubleshooting and inspecting generated commands passed to Prettier.

- **prettier_cli_path** (default: ***empty***)  
    If Sublime Text has problems automatically resolving a path to [Prettier],
    you can set a custom path here.

    When the setting is empty, the plug-in will attempt to find Prettier by...

    - Searching the path relative to the current Sublime Text Project directory,
      e.g.: `node_modules/.bin/prettier`.
    - The USER home directory, e.g.: `$HOME/node_modules/.bin/prettier`.
    - The *JsPrettier* plug-in directory, and `node_modules/.bin/prettier` path.
    - Globally installed Prettier.

    > [nvm] users must set an appropriate absolute *prettier_cli_path* (and
    > absolute *node_path*), according to the runtime environment.

- **node_path** (default: ***empty***)  
    If Sublime Text has problems resolving the absolute path to node, you can
    set a custom path here.

    > [nvm] users must set an appropriate absolute *node_path* (and
    > absolute *prettier_cli_path*), according to the runtime environment.

- **auto_format_on_save** (default: ***false***)  
    Automatically format the file on save.

- **auto_format_on_save_excludes** (default: [])  
    File exclusion patterns to ignore when `auto_format_on_save` is enabled.
  
    **Example:**
  
    ```json
    {
        "auto_format_on_save_excludes": [
            "*/node_modules/*",
            "*/file.js",
            "*.json"
        ]
    }
    ```

- **auto_format_on_save_requires_prettier_config** (default: ***false***)  
    Enable auto format on save *only* when a Prettier config file is (or isn't)
    found.

    The Prettier config file is resolved by first checking if a `--config </path/to/prettier/config>`
    is specified in the `additional_cli_args` setting, then by searching the
    location of the file being formatted, and finally navigating up the file tree
    until a config file is (or isn't) found.

- **allow_inline_formatting** (default: ***false***)  
    Enables the ability to format *selections* of in-lined code. For example, to
    format a selection of JavaScript code within a PHP or HTML file. When
    ***true***, the JsPrettier command is available for use across all Sublime
    Text syntaxes.

- **custom_file_extensions** (default: [])  
    There's built-in support already for `js`, `jsx`, `json`, `graphql/gql`,
    `ts`, `tsx`, `css`, `scss`, `less`, `md` and `vue` files. Put additional
    file extensions here, but be sure not to include the leading dot in the
    file extension.

- **max_file_size_limit** (default: ***-1***)  
    The max allowed file size to format in bytes. For performance reasons,
    files with a greater file size than the specified `max_file_size_limit` will
    not format. Setting the `max_file_size_limit` value to ***-1*** disables the
    file size checking (default).

- **additional_cli_args** (default: {})  
    A key-value pair of arguments to append to the prettier command.

    **Examples:**

    ```json
    {
        "additional_cli_args": {
            "--config": "path/to/my/custom/.prettierrc",
            "--config-precedence": "prefer-file",
            "--ignore-path": "path/to/.prettierignore",
            "--with-node-modules": ""
        }
    }
    ```

### Prettier Options

- **useTabs** (internally set by the [***translate_tabs_to_spaces***] setting)  
    Indent lines with tabs.

- **printWidth** (default: ***80***)  
    Specifies that the formatted code should fit within this line limit.

- **tabWidth** (internally set by the [***tab_size***] setting)  
    The number of spaces to use per tab.

- **singleQuote** (default: ***false***)  
    Format code using single or double-quotes.

- **trailingComma** (default: "***none***")  
   Controls the printing of trailing commas wherever possible. Valid options:
    - "***none***" - No trailing commas
    - "***es5***" - Trailing commas where valid in ES5 (objects, arrays, etc)
    - "***all***" - Trailing commas wherever possible (function arguments)

- **bracketSpacing** (default: ***true***)  
    Controls the printing of spaces inside object literals.

- **jsxBracketSameLine** (default: ***false***)  
    When *true*, multi-line jsx elements with right-angle brackets ("&gt;") are
    placed at the end of the last line, instead of alone on the next line.

- **parser** (default: "***babylon***")  
    Which parser to use. Valid options are "***flow***", "***babylon***",
    "***typescript***", "***css***", "***json***", "***graphql***"
    and "***markdown***".
  
    The `parser` option is automatically set by the plug-in (JsPrettier), based
    on the contents of current file or selection.
  
- **semi** (default: ***true***)  
    ***true*** to add a semicolon at the end of every line, or ***false*** to
    add a semicolon at the beginning of lines that may introduce ASI failures.

- **requirePragma** (default: ***false***)  
    Prettier can ignore formatting files that contain a special comment, called
    a *pragma* at the top of the file. This is useful when gradually
    transitioning large, unformatted codebases to prettier.

    For example, a file with its first comment specified below, and the
    `--require-pragma` option:

    ```js
    /**
     * @prettier
     */
    ```

    or

    ```js
    /**
     * @format
     */
    ```

- **proseWrap** (default: "***preserve***")  
    (*Markdown Only*) By default, Prettier will wrap markdown text as-is since
    some services use a linebreak-sensitive renderer, e.g. GitHub comment and
    BitBucket. In some cases you may want to rely on SublimeText soft wrapping
    instead, so this option allows you to opt out with "never".

    Valid Options:

    - "***always***" - Wrap prose if it exceeds the print width.
    - "***never***" - Do not wrap prose.
    - "***preserve***" (default) - Wrap prose as-is. available in v1.9.0+

- **arrowParens** (default: "***avoid***")  
    Include parentheses around a sole arrow function parameter.

    Valid Options:

    - "***avoid***" (default) - Omit parentheses when possible. Example: `x => x`
    - "***always***" - Always include parentheses. Example: `(x) => x`

See the Prettier Options [doc page] for more details and examples.

### Project-level Settings

JsPrettier supports [Project-level settings] set within `<project_name>.sublime-project` files.
In order for Project-level settings to override the default and customized
preferences, create a `js_prettier` section under the project file's `settings`
section.

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
            "auto_format_on_save_excludes": [],
            "auto_format_on_save_requires_prettier_config": false,
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
                "semi": true,
                "requirePragma": false,
                "proseWrap": "preserve",
                "arrowParens": "avoid"
            }
        }
    }
}
```

### Prettier Configuration Files

When [Prettier configuration files] are detected, options defined in *Sublime
Text* are ignored, with the exception of `parser`, `tabWidth` and `useTabs`.
These options are automatically set based on syntax settings of the current file
or selection(s) defined in Sublime Text.

#### Custom Prettier Config File Path

To specify a custom Prettier config path, simply add a `--config <path>`
key-value item to `additional_cli_args`. Here's an example:

```json
{
    "additional_cli_args":
    {
        "--config": "path/to/my/custom/.prettierrc",
        "--config-precedence": "prefer-file"
    }
}
```

#### Disable Prettier Config File Discovery

You can also add the `--no-config` option to the `additional_cli_args` setting,
and tell Prettier not to attempt to find config files.

```json
{
    "additional_cli_args": {
        "--no-config": ""
    }
}
```

#### Prettier Ignore Config File Discovery (`.prettierignore`)

When the [`--ignore-path`] option is NOT specified in `additional_cli_args`, the
plug-in will attempt to discover and set `--ignore-path <file>` when a
`.prettierignore` config exists in the same directory of the source file
(first), or the active Sublime Text project root directory (second).

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
[yarn]: https://yarnpkg.com
[npm]: https://www.npmjs.com
[nvm]: https://github.com/creationix/nvm
[zip file]: https://github.com/jonlabelle/SublimeJsPrettier/archive/master.zip
[Sublime Text Packages directory]: #default-st-paths
[manual download instructions]: #manual-download
[Sublime Text Console]: http://docs.sublimetext.info/en/latest/basic_concepts.html#sublime-text-is-programmable
[custom key binding]: http://docs.sublimetext.info/en/latest/customization/key_bindings.html
[Prettier Configuration files]: https://prettier.io/docs/en/configuration.html
[issue template]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/.github/ISSUE_TEMPLATE.md
[report an issue]: https://github.com/jonlabelle/SublimeJsPrettier/issues
[Changelog]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/CHANGELOG.md
[MIT License]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/LICENSE.txt
[doc page]: https://prettier.io/docs/en/options.html
[`--ignore-path`]: https://prettier.io/docs/en/cli.html#ignore-path
