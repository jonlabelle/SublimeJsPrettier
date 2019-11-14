# JsPrettier

[![Travis CI Build Status](https://travis-ci.org/jonlabelle/SublimeJsPrettier.svg?branch=master)](https://travis-ci.org/jonlabelle/SublimeJsPrettier)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/ta7379jk57cdwu76/branch/master?svg=true)](https://ci.appveyor.com/project/jonlabelle/sublimejsprettier/branch/master)
[![SonarQube Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=org.jonlabelle-github%3ASublimeJsPrettier&metric=alert_status)](https://sonarcloud.io/dashboard/index/org.jonlabelle-github:SublimeJsPrettier)
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
- [Prettier Plug-in Support](#prettier-plug-in-support)
    - [Prettier PHP](#prettier-php)
- [Issues](#issues)
- [Changes](#changes)
- [Author](#author)
- [License](#license)

</details>

## Installation

[JsPrettier] is compatible with both Sublime Text 2 and 3, and all supported
Operating Systems.

### Requirements

- [Sublime Text] – Text editor for code
- [node.js] – JavaScript runtime
    - [yarn] or [npm] – Package manager for JavaScript
        - [Prettier] – Opinionated code formatter (v1.19 or above)

### Install Prettier

If you've already installed [Prettier] \(using one of the [yarn] or [npm]
commands below\), you're all set... otherwise:

```bash
# yarn (local):
yarn add prettier --dev

# yarn (global):
yarn global add prettier

# npm (local):
npm install --save-dev prettier

# npm (global):
npm install --global prettier
```

### Install JsPrettier via Package Control

The easiest and recommended way to install Js​Prettier is using [Package Control].

From the **application menu**, navigate to:

- `Tools` -> `Command Palette...` -> `Package Control: Install Package`, type
  the word **JsPrettier**, then select it to complete the installation.

### Install JsPrettier Manually

1. Download and extract Js​Prettier [zip file] to your [Sublime Text Packages directory].
2. Rename the extracted directory from `SublimeJsPrettier-master` to `JsPrettier`.

**Default Sublime Text Packages Paths:** <a name="default-st-paths"></a>

- **OS X:** `~/Library/Application Support/Sublime Text [2|3]/Packages`
- **Linux:** `~/.Sublime Text [2|3]/Packages`
- **Windows:** `%APPDATA%/Sublime Text [2|3]/Packages`

> **NOTE** Replace the `[2|3]` part with the appropriate Sublime Text
> version for your installation.

### Install JsPrettier Using Git

If you're a Git user, you can install [JsPrettier] and keep it up-to-date by
cloning the repository directly into your [Sublime Text Packages directory].

> **TIP:** You can locate your Sublime Text Packages directory by using the
> application menu `Preferences` -> `Browse Packages...`.

```bash
git clone https://github.com/jonlabelle/SublimeJsPrettier.git "JsPrettier"
```

## Usage

There are three available options to format code:

1. **Command Palette:** From the command palette (<kbd>ctrl/cmd + shift + p</kbd>), type **JsPrettier Format Code**.
2. **Context Menu:** Right-click anywhere in the file to bring up the context menu and select **JsPrettier Format Code**.
3. **Key Binding:** There is no default key binding to run Prettier, but here's how to [add your own].

### Command Scope

`JsPrettier` will attempt to format selections of code first, then the entire
file. When `auto_format_on_save` is `true`, the **entire file** will be formatted.

### Custom Key Binding

To add a [custom key binding], please reference the following example which
binds the `js_prettier` command to <kbd>ctrl + alt + f</kbd>:

```json
{ "keys": ["ctrl+alt+f"], "command": "js_prettier" }
```

## Settings

Plug-in settings and Prettier options can be configured by navigating the
application menu to:

- **Preferences**
    - **Package Settings**
        - **JsPrettier**
            - **Settings - Default** (to view the defaults)
            - **Settings - User** (to override the defaults)

### Sublime Text Settings

- **debug** (default: ***false***)  
    When enabled (*true*), debug info will print to the console - useful for
    troubleshooting and inspecting generated commands passed to Prettier.
    Enabling debug mode also sets Prettier's [`--loglevel`] option to `debug`
    (when not overridden by `additional_cli_args`), for printing additional
    debug information to the console.

- **prettier_cli_path** (default: ***empty***)  
    If Sublime Text has problems automatically resolving a path to [Prettier],
    you can set a custom path here.

    When the setting is empty, the plug-in will attempt to find Prettier by:

    - Searching the path relative to the current Sublime Text Project directory...
      `node_modules/.bin/prettier` and `node_modules/prettier/bin-prettier.js`.
    - The *JsPrettier* plug-in directory... `node_modules/.bin/prettier` and `node_modules/prettier/bin-prettier.js`.
    - The current user's home directory... `$HOME/node_modules/.bin/prettier`.
    - And finally a globally installed Prettier instance.
  
    **Examples:**
  
    ```
    ...
    {
        // macOS/Linux:
        "prettier_cli_path": "/usr/local/bin/prettier"
        "prettier_cli_path": "/some/absolute/path/to/node_modules/.bin/prettier"
        "prettier_cli_path": "./node_modules/.bin/prettier"
        "prettier_cli_path": "~/bin/prettier"
        "prettier_cli_path": "$HOME/bin/prettier"
        "prettier_cli_path": "${project_path}/bin/prettier"
        "prettier_cli_path": "$ENV/bin/prettier"

        // Windows:
        "prettier_cli_path": "C:/path/to/prettier.cmd"
        "prettier_cli_path": "%USERPROFILE%\\bin\\prettier.cmd"
    }
    ...
    ```

- **node_path** (default: ***empty***)  
    If Sublime Text has problems resolving the absolute path to node, you can
    set a custom path here.
  
    **Examples:**
  
    ```
    ...
    {
        // macOS/Linux:
        "node_path": "/usr/local/bin/node"
        "node_path": "/some/absolute/path/to/node"
        "node_path": "./node"
        "node_path": "~/bin/node"
        "node_path": "$HOME/bin/node"
        "node_path": "${project_path}/bin/node"
        "node_path": "$ENV/bin/node"

        // Windows:
        "node_path": "C:/path/to/node.exe"
        "node_path": "%USERPROFILE%\\bin\\node.exe"
    }
    ...
    ```

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
    There's built-in support already for `js`, `jsx`, `mjs`, `json`, `html`,
    `graphql/gql`, `ts`, `tsx`, `css`, `scss`, `less`, `md`, `mdx`, `yml`,
    `vue` and `component.html` (angular html) files.

    Put additional file extensions here, and be sure not to include the
    leading dot in the file extension.

- **max_file_size_limit** (default: ***-1***)  
    The max allowed file size to format in bytes. For performance reasons,
    files with a greater file size than the specified `max_file_size_limit` will
    not format. Setting the `max_file_size_limit` value to ***-1*** disables the
    file size checking (default).

- **disable_tab_width_auto_detection** (default: ***false***)  
    Whether or not to disable the plug-in from automatically setting Prettier's
    "[tabWidth / \--tab-width](https://prettier.io/docs/en/options.html#tab-width)"
    option, and adhere to the Prettier configured setting.

- **disable_prettier_cursor_offset** (default: ***false***)  
    There's an apparent (and nasty) defect in Prettier that seems to occur
    during Prettier's [cursor offset](https://prettier.io/docs/en/api.html#prettierformatwithcursorsource-options)
    calculation, and when attempting to format large or minimized files (but not limited to just these cases).
    The issue effectively results in the CPU spiking to a constant 100%...
    indefinitely, or until the node executable/process running Prettier is
    forcefully terminated.

    To avoid this problematic behavior, or until the defect is resolved, you can
    disable the plug-in (JsPrettier) from ever passing the cursor offset
    position to Prettier by setting the `disable_prettier_cursor_offset` value
    to `true`.

    - See related issues: [#147](https://github.com/jonlabelle/SublimeJsPrettier/issues/147), [#168](https://github.com/jonlabelle/SublimeJsPrettier/issues/168)
    - [Prettier Cursor Offset Documentation](https://prettier.io/docs/en/api.html#prettierformatwithcursorsource-options)

- **additional_cli_args** (default: {})  
    A key-value pair of arguments to append to the prettier command.

    **Examples:**

    ```json
    {
        "additional_cli_args": {
            "--config": "~/.prettierrc",
            "--config": "$HOME/.prettierrc",
            "--config": "${project_path}/.prettierrc",
            "--config": "/some/absolute/path/to/.prettierrc",

            "--config-precedence": "file-override",
            "--ignore-path": "${file_path}/.prettierignore",
            "--with-node-modules": "",
            "--plugin-search-dir": "$folder"
        }
    }
    ```

### Prettier Options

- **useTabs** (internally set by the [***translate_tabs_to_spaces***] setting)  
    Indent lines with tabs.

- **printWidth** (default: ***80***)  
    Specifies that the formatted code should fit within this line limit.

- **tabWidth**  (default: ***2***)  
    Specify the number of spaces per indentation-level.

    **IMPORTANT:** By default, "tabWidth" is automatically set using the
    SublimeText configured value for "[tab_size]". To disable this behavior, you
    must first change the `disable_tab_width_auto_detection` value from `false`,
    to `true`.

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

- **parser** (default: "***babel***")  
    The [`parser`] is automatically set by the plug-in (JsPrettier), based
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
    (*Markdown and YAML Only*) By default, Prettier will wrap Markdown and YAML
    text as-is since some services use a linebreak-sensitive renderer, e.g.
    GitHub comment and BitBucket. In some cases you may want to rely on
    SublimeText soft wrapping instead, so this option allows you to opt out with
    "never".

    Valid Options:

    - "***always***" - Wrap prose if it exceeds the print width.
    - "***never***" - Do not wrap prose.
    - "***preserve***" (default) - Wrap prose as-is. available in v1.9.0+

- **arrowParens** (default: "***avoid***")  
    Include parentheses around a sole arrow function parameter.

    Valid Options:

    - "***avoid***" (default) - Omit parentheses when possible. Example: `x => x`
    - "***always***" - Always include parentheses. Example: `(x) => x`

- **htmlWhitespaceSensitivity** (default: "***css***")  
    (*HTML Only*) Specify the global whitespace sensitivity for HTML files,
    see [whitespace-sensitive formatting] for more info.

    Valid Options:

    - "***css***" (default) - Respect the default value of CSS display property.
    - "***strict***" - Whitespaces are considered sensitive.
    - "***ignore***" - Whitespaces are considered insensitive.

- **quoteProps** (default: "***as-needed***")  
    Change when properties in objects are quoted. Requires [Prettier v1.17+].

    Valid options:

    - "***as-needed***" (default) - Only add quotes around object properties where required.
    - "***consistent***" - If at least one property in an object requires quotes, quote all properties.
    - "***preserve***" - Respect the input use of quotes in object properties.

- **vueIndentScriptAndStyle** (default: ***false***)  
    (*Vue files Only*) Whether or not to indent the code inside `<script>`
    and `<style>` tags in Vue files. Some people (like [the creator of Vue](https://github.com/prettier/prettier/issues/3888#issuecomment-459521863))
    don't indent to save an indentation level, but this might break code
    folding in Sublime Text.

    Valid Options:

    - ***false*** (default) - Do not indent script and style tags in Vue files.
    - ***true*** - Indent script and style tags in Vue files.

See the Prettier Options [doc page] for more details and examples.

### Project-level Settings

JsPrettier supports [project-level settings], specified in `<project_name>.sublime-project` files.

In order for your project-level settings to override [previous configurations](#settings),
you'll need to add a new `js_prettier` key and section under `settings`, as [seen below].

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
            "disable_tab_width_auto_detection": false,
            "disable_prettier_cursor_offset": false,
            "additional_cli_args": {},
            "prettier_options": {
                "printWidth": 80,
                "tabWidth": 2,
                "singleQuote": false,
                "trailingComma": "none",
                "bracketSpacing": true,
                "jsxBracketSameLine": false,
                "parser": "babel",
                "semi": true,
                "requirePragma": false,
                "proseWrap": "preserve",
                "arrowParens": "avoid",
                "htmlWhitespaceSensitivity": "css",
                "quoteProps": "as-needed",
                "vueIndentScriptAndStyle": false
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
        "--config": "~/some/path/from/my/home/.prettierrc",
        "--config-precedence": "prefer-file",
        "--ignore-path": "${project_path}/.prettierignore"
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

## Prettier Plug-in Support

### Prettier PHP

In most cases, [Prettier PHP] works as drop-in replacement for Prettier.
However, JsPrettier only detects if you're formatting a PHP file (or PHP selection),
and sets the `--parser` to `php` accordingly. Aside from that, it's up to you ensure your
config(s) conform to Prettier PHP [options](https://github.com/prettier/plugin-php#configuration).

To **install Prettier PHP** in your project root, and use it as a drop-in
replacement for Prettier:

```bash
cd to/project/directory
npm install @prettier/plugin-php
```

## Issues

To report a bug or a make suggestion, please [open a new issue] selecting the
appropriate Issue Template (**Bug report** or **Feature request**). Be sure to
follow the guidelines outlined in each template... otherwise your submission
will be subject to immediate closure.

## Changes

Please visit the [Changelog] page for a complete list of changes.

## Author

Jon LaBelle

## License

[MIT License]

[Watch a Quick Demo]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/demo.gif
[Prettier]: https://prettier.io
[Prettier API section]: https://github.com/prettier/prettier#api
[Prettier CLI]: https://github.com/prettier/prettier#cli
[Package Control]: https://packagecontrol.io/packages/JsPrettier
[Sublime Text]: https://www.sublimetext.com
[JsPrettier]: https://github.com/jonlabelle/SublimeJsPrettier
[node.js]: https://nodejs.org
[project-level settings]: http://docs.sublimetext.info/en/latest/reference/projects.html
[tab_size]: http://docs.sublimetext.info/en/latest/reference/settings.html#whitespace-and-indentation
[***translate_tabs_to_spaces***]: http://docs.sublimetext.info/en/latest/reference/settings.html#whitespace-and-indentation
[installed globally]: #install-prettier
[yarn]: https://yarnpkg.com
[npm]: https://www.npmjs.com
[nvm]: https://github.com/creationix/nvm
[zip file]: https://github.com/jonlabelle/SublimeJsPrettier/archive/master.zip
[Sublime Text Packages directory]: #default-st-paths
[Sublime Text Console]: http://docs.sublimetext.info/en/latest/basic_concepts.html#sublime-text-is-programmable
[custom key binding]: http://docs.sublimetext.info/en/latest/customization/key_bindings.html
[Prettier Configuration files]: https://prettier.io/docs/en/configuration.html
[issue template]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/.github/ISSUE_TEMPLATE/bug_report.md
[Changelog]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/CHANGELOG.md
[MIT License]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/LICENSE.txt
[doc page]: https://prettier.io/docs/en/options.html
[`--ignore-path`]: https://prettier.io/docs/en/cli.html#ignore-path
[whitespace-sensitive formatting]: https://prettier.io/blog/2018/11/07/1.15.0.html#whitespace-sensitive-formatting
[`parser`]: https://prettier.io/docs/en/options.html#parser
[`--loglevel`]: https://prettier.io/docs/en/cli.html#loglevel
[Prettier PHP]: https://github.com/prettier/plugin-php
[open a new issue]: https://github.com/jonlabelle/SublimeJsPrettier/issues/
[Prettier v1.17+]: https://prettier.io/blog/2019/04/12/1.17.0.html
[seen below]: #example-sublime-text-project-file "See the Sublime Text project file example"
[add your own]: #custom-key-binding "See how to add a custom key binding to run Prettier"
