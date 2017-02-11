# Sublime Text JavaScript Prettier

[![Build Status](https://travis-ci.org/jonlabelle/SublimeJsPrettier.svg?branch=master)](https://travis-ci.org/jonlabelle/SublimeJsPrettier) [![Downloads](https://packagecontrol.herokuapp.com/downloads/JsPrettier.svg?color=80d4cd)](https://packagecontrol.io/packages/JsPrettier)

A Sublime Text Plug-in for [Prettier], the opinionated JavaScript formatter.

[![](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/before_and_after.gif?raw=true)](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/demo.gif)

- [Watch a Quick Demo]

## Installation

Sublime Text JavaScript Prettier ([JsPrettier]) is compatible with both Sublime
Text 2 and 3, and all supported Operating Systems.

**Requirements**

The Sublime Text JavaScript Prettier plug-in requires the following programs to
be installed:

- [node.js] - JavaScript runtime
- [npm] - Package manager for JavaScript
- [Prettier] - Opinionated JavaScript formatter

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

* **OS X:** `~/Library/Application Support/Sublime Text [2|3]/Packages`
* **Linux:** `~/.Sublime Text [2|3]/Packages`
* **Windows:** `%APPDATA%/Sublime Text [2|3]/Packages`

> **NOTE** Replace the `[2|3]` part with the appropriate Sublime Text
> version for your installation.

### Install JsPrettier Using Git

Alternatively, if you're a git user, you can install [JsPrettier] and keep it up
to date by cloning the repository directly into your [Sublime Text Packages directory].

You can locate your Sublime Text Packages directory by using the menu item
`Preferences` -> `Browse Packages...`

    git clone https://github.com/jonlabelle/SublimeJsPrettier.git "JsPrettier"

## Usage

To run the `JsPrettier` command... open the Sublime Text **Command Palette**
(<kbd>super + shift + p</kbd>) and type ***JsPrettier***.

You can also right-click anywhere in the file (JavaScript Syntax only) to bring
up the **Context Menu**, then select ***JsPrettier*** to execute the command.

### Command Scope

The `JsPrettier` command will attempt to format any selected JavaScript sections
of code first; if no selections are made, the entire file will be formatted.

> **NOTE:** When the `auto_format_on_save` is setting is set to `true`, the
> **entire file** will always be formatted.

### Custom Key Binding

To add a [custom key binding] to execute the `JsPrettier` command at will,
please reference the following example, which binds to <kbd>ctrl/cmd + b</kbd>.

```json
{ "keys": ["super+b"], "command": "js_prettier" }
```

## Settings

All [Prettier] options are configurable from the `JsPrettier.sublime-settings`
file, accessible from the **Preferences** > **Package Settings** >
***JsPrettier*** menu shortcut.

### Sublime Text Settings

- `prettier_cli_path` (default: *empty*)  
   It's strongly recommended leaving the `prettier_cli_path` value empty (the
   default), however if Sublime Text has problems resolving the path to the
   `prettier` cli executable, you can explicitly specify the full path here.
   
- `auto_format_on_save` (default: *false*)  
   Whether or not to run the `js_prettier` command automatically on every file
   save.

### Prettier Options

- `printWidth` (default: *80*)  
   Specifies that the formatted code should fit within this line limit.

- `tabWidth` (inherits Sublime Text's *tab_size*)  
   The number of spaces to use per tab.

- `singleQuote` (default: *false*)  
   If true, code will be formatted using single-quotes, instead of double-quotes.

- `trailingComma` (default: *false*)  
   Controls the printing of trailing commas wherever possible.

- `bracketSpacing` (default: *true*)  
   Controls the printing of spaces inside object literals.

- `parser` (default: *babylon*)  
   Which parser to use. Valid options are `'flow'` and `'babylon'`.
   
> *For further details and examples of Prettier's options, please reference the
> [Prettier repository].*

## Changes

Please visit the [Changelog] page for a complete list of changes.

## Author

Jon LaBelle

## License

[MIT License]

[Watch a Quick Demo]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/demo.gif
[Prettier]: https://github.com/jlongster/prettier
[Prettier repository]: https://github.com/jlongster/prettier
[Package Control]: https://packagecontrol.io/packages/JsPrettier
[JsPrettier]: https://github.com/jonlabelle/SublimeJsPrettier
[node.js]: https://nodejs.org
[npm]: https://www.npmjs.com
[zip file]: https://github.com/jonlabelle/SublimeJsPrettier/archive/master.zip
[Sublime Text Packages directory]: #default-st-paths "Navigate to Default Sublime Text Packages Paths"
[manual download instructions]: #manual-download
[custom key binding]: http://docs.sublimetext.info/en/latest/customization/key_bindings.html
[Changelog]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/CHANGELOG.md
[MIT License]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/LICENSE.md
