# Sublime Text JavaScript Prettier

A Sublime Text Plug-in for [Prettier], the opinionated JavaScript formatter.

## Installation

Sublime Text JavaScript Prettier (JsPrettier) is compatible with both Sublime
Text 2 and 3, and all supported Operating Systems.

### Requirements

The Sublime Text JavaScript Prettier plug-in requires the following programs:

- [node.js]
- [npm]

### Package Control

The easiest and recommended way to install Sublime Text JavaScript Prettier is
using Package Control.

From the **main application menu**, navigate to:

- **Tools** -> **Command Palette...** -> **Package Control: Install Package**,
type the word ***JsPrettier*** and select it to complete installation.

### Manual Download

Download and extract Sublime Text JavaScript Prettier [zip file] to your
Sublime Text Packages directory.

**Default Sublime Text Packages Paths:**
<a name="default-st-paths"></a>

* **OS X:** `~/Library/Application Support/Sublime Text [2|3]/Packages`
* **Linux:** `~/.Sublime Text [2|3]/Packages`
* **Windows:** `%APPDATA%/Sublime Text [2|3]/Packages`

> **NOTE** Replace the `[2|3]` part with the appropriate Sublime Text
> version for your installation.

### Installing the node.js Dependencies

**cd** to the `SublimeJsPrettier` [package directory], and install
the [node.js] dependencies using [npm].

For example, on **macOS:**

	$ cd ~/Library/Application Support/Sublime Text 3/Packages/SublimeJsPrettier
	$ npm install

## Usage

To run the **JsPrettier** command... open the Sublime Text **Command Palette**
(<kbd>shift + super + p</kbd>) and type **`JsPrettier: Format JavaScript`**.

## Settings

All [Prettier] options are configurable from the `JsPrettier.sublime-settings`
file, accessible from the **Preferences** > **Package Settings** >
***JsPrettier*** menu shortcut.

## Author

Jon LaBelle

[Prettier]: https://github.com/jlongster/prettier
[Package Control]: https://packagecontrol.io
[node.js]: https://nodejs.org
[npm]: https://www.npmjs.com
[zip file]: https://github.com/jonlabelle/SublimeJsPrettier/archive/master.zip
[package directory]: #default-st-paths "Default Sublime Text Packages Paths"
[manual download instructions]: #manual-download
