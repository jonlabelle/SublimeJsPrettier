# Changelog

## 1.28.0

**Release Date:** 2019-11-14

- Added support for new Prettier [Vue files script and style tags indentation]
  option; determines whether or not to indent the code inside `<script>` and
  `<style>` tags in Vue files (requires [Prettier v1.19+]).

  | Default |              CLI Override              |            API Override           |              Sublime Text             |
  |---------|----------------------------------------|-----------------------------------|---------------------------------------|
  | `false` | `--vue-indent-script-and-style <bool>` | `vueIndentScriptAndStyle: <bool>` | [`"vueIndentScriptAndStyle": <bool>`] |

  **Valid options:**

    - `false` (default) - Do not indent script and style tags in Vue files.
    - `true` - Indent script and style tags in Vue files.

## 1.27.0

**Release Date:** 2019-04-18

- Added support for new Prettier [Quote Props] option; changes quotes around
  object properties (requires [Prettier v1.17+]).
  
    - Default: `"as-needed"`
    - CLI Override: `--quote-props <as-needed|consistent|preserve>`
    - API Override: `quoteProps:` `"<as-needed|consistent|preserve>"`
  
  **Valid options:**

    - `"as-needed"` (default) - Only add quotes around object properties where required.
    - `"consistent"` - If at least one property in an object requires quotes, quote all properties.
    - `"preserve"` - Respect the input use of quotes in object properties.

## 1.26.5

**Release Date:** 2019-04-07

- Added new setting (`disable_prettier_cursor_offset`) to disable Prettier's
  (buggy) cursor offset calculation.

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

## 1.26.0

**Release Date:** 2019-03-17

- Added support for formatting PHP files; requires the [Prettier PHP Plugin].

    ```bash
    cd to/project/directory
    npm install @prettier/plugin-php
    ```

## 1.25.0

**Release Date:** 2019-02-27

- Enabling debug mode now also sets Prettier's [`--loglevel`] option to `debug`
  (when not overridden by `additional_cli_args`), for printing additional debug
  information to the console.

## 1.24.0

**Release Date:** 2019-01-29

- Added support for auto-expanding environment and Sublime Text (v3+ only)
  variables in path-like settings. Including `prettier_cli_path`, `node_path`
  and options defined in `additional_cli_args` (e.g. `--config` `<path>`).

  Check-out the [default settings] \(comment section) for examples.
  
## 1.23.0

**Release Date:** 2019-01-25

- Renamed default `babylon` parser to `babel` (requires [Prettier v1.16+]).
  Babel's parser, babylon, was renamed to @babel/parser in Babel 7.

  See the [Prettier v1.16] release notes page for additional information on the
  parser change, including new features and bug fixes.
  
## 1.22.0

**Release Date:** 2019-01-21

- Added setting to `disable_tab_width_auto_detection` (default is `false`);
  which disables the default behavior of the plug-in automatically setting
  Prettier's "tabWidth" option (at runtime) with the SublimeText configured
  value for "tab_size".

## 1.21.0

**Release Date:** 2018-09-28

- Added YAML syntax/file formatting support. Requires [Prettier v1.14+].

## 1.20.0

**Release Date:** 2018-02-13

- Added new `auto_format_on_save_requires_prettier_config` setting that will
  enable/disable auto format on save *only* if a Prettier config file is (or isn't) found.
  
  The Prettier config file is resolved by first checking if a `--config </path/to/prettier/config>`  
  is specified in the `additional_cli_args` setting, then by searching the
  location of the file being formatted, and finally navigating up the file tree
  until a config file is (or isn't) found.

## 1.19.0

**Release Date:** 2018-01-12

- Support for Vue Single File Components. Requires [Prettier v1.10+].

## 1.18.0

**Release Date:** 2017-12-09

- Added support for [`arrowParens`] option. Configure formatting to include
  parentheses around a sole arrow function parameter. Requires [Prettier v1.9+].

## 1.17.0

**Release Date:** 2017-11-10

- Added support for formatting Markdown files (requires [Prettier v1.8+]).

## 1.16.0

**Release Date:** 2017-09-23

- Added new setting for [requirePragma] option.
- Allow formatting to take place when Prettier reports non-fatal errors. For
  example, when Prettier reports warnings (to stderr) about *unknown options*
  ([#63], [#64], [#67], [#68], [#72]).

## 1.15.0

**Release Date:** 2017-09-05

- Added support for setting a custom Prettier config path
  (via`additional_cli_args` setting), or disabling Prettier config discovery all
  together; using the `additional_cli_args` setting.

  See the [docs](https://github.com/jonlabelle/SublimeJsPrettier#prettier-configuration-files)
  for more details and config examples.

## 1.14.0

**Release Date:** 2017-09-02

- Prettier configuration files are now automatically resolved via the
  `prettier --find-config-path <target_file_to_format>` command.
  Requires [prettier v1.6+].

## 1.13.0

**Release Date:** 2017-09-01

- Add support for reading configuration options from Prettier configuration
  files (e.g.: `.prettierrc` files). Requires [prettier v1.6+].

## 1.12.0

**Release Date:** 2017-07-02

- Added new `auto_format_on_save_excludes` setting to ignore auto formatting
  when the target file, or its path resides in a particular location, and when
  `auto_format_on_save` is turned on.

## 1.11.0

**Release Date:** 2017-06-29

- Added support for JSON formatting (requires [Prettier v1.5+]).
- Added support for GraphQL formatting (requires [Prettier v1.5+]).

## 1.10.0

**Release Date:** 2017-06-07

- Added the new setting `max_file_size_limit` to restrict Prettier formatting
  based on file size.

## 1.9.0

**Release Date:** 2017-06-05

- Added new setting `additional_cli_args` for appending additional arguments to
  the prettier cli command.

## 1.8.0

**Release Date:** 2017-06-04

- Added new setting to allow formatting custom file extensions.
- Support for CSS formatting (requires [Prettier v1.4+]).
- Built-in support for TypeScript.

## 1.7.0

**Release Date:** 2017-04-13

- Added support for new `--semi` and `--use-tabs` options.

## 1.6.0

**Release Date:** 2017-03-08

- Introduced new `debug` (bool) setting. When enabled (true), additional
  debugging information about the command and configured settings will be
  printed to the Sublime Text Console; useful for troubleshooting purposes.

## 1.5.0

**Release Date:** 2017-02-24

- Added the ability to specify a custom node path, via the `node_path` setting.

## 1.4.0

**Release Date:** 2017-02-20

- Added support for [Project-level settings].

## 1.3.1

**Release Date:** 2017-02-19

- Added support for the modified `trailingComma` option. The `trailingComma`
  option controls the printing of trailing commas wherever possible.

    Valid options are:

    - `"none"` -- No trailing commas
    - `"es5"`  -- Trailing commas where valid in ES5 (objects, arrays, etc)
    - `"all"`  -- Trailing commas wherever possible (function arguments)

## 1.3.0

**Release Date:** 2017-02-18

- Added the new setting `allow_inline_formatting` (defaults to *false*) which
  provides the ability to format *selections* of in-lined JavaScript code,
  outside of the normal JavaScript syntax. For example, to format a selection of
  JavaScript code within a PHP or HTML file. When `true`, the JsPrettier command
  is available for use across all Sublime Text syntaxes.

## 1.2.5

**Release Date:** 2017-02-16

- Added format on save support for .jsx files.

## 1.2.4

**Release Date:** 2017-02-16

- Added support for the new `jsxBracketSameLine` option. When
  `jsxBracketSameLine` is *true* (the default is *false*), right-angle brackets
  `>` of multi-line jsx elements will be placed at the end of the last line,
  instead of being alone on the next line. You may be required to update to the
  latest version of the [Prettier] to leverage the `jsxBracketSameLine` option
  (available since v0.17.0).

## 1.2.0

**Release Date:** 2017-02-10

- Now when the `auto_format_on_save` setting is set to `true`, the entire file
  will always be formatted.
- Removed extra line-breaks injected by the `prettier` cli command at the end of
  selected regions and entire file.
- Added Context Menu shortcut.

## 1.1.2

**Release Date:** 2017-01-28

- Added support for merging selective `prettier_options` in the *User*
  `JsPrettier.sublime-settings` file.

## 1.1.1

**Release Date:** 2017-01-22

- Introduced less aggressive error reporting ([#4]). Errors generated by the
  `prettier` cli are written to Sublime Text's console output window, instead of
  an alert dialog.

## 1.1.0

**Release Date:** 2017-01-21

- Removed the `node_path` option from settings.
- Added new `prettier_cli_path` setting for those wanting to explicitly set the
  path to the prettier executable/command.
- Removed support for local prettier installations stored in the Sublime Text
  Package directory.
- Improved detection of environment prettier path.

## 1.0.3

**Release Date:** 2017-01-19

- Incorporated new prettier option to specify which parser to use. Valid options
  for `parser` are `flow` and `babel`. The `useFlowParser` option has been
  deprecated, in favor of the new `parser` option.

## 1.0.2

**Release Date:** 2017-01-19

- Removed the default value for "node_path", and internally try to sniff out the
  appropriate path.

## 1.0.1

**Release Date:** 2017-01-18

- Fixed package path to use "JsPrettier" instead of "SublimeJsPrettier".
  Previously caused the "Default" settings file not to open from the Main Menu.

- Added notice regarding local installations of Prettier. The `node_modules`
  directory will be deleted after every package update pushed by Package
  Control.

## 1.0.0

**Release Date:** 2017-01-18

- JsPrettier now available on [Package Control].

[Package Control]: https://packagecontrol.io/packages/JsPrettier
[Prettier]: https://github.com/jlongster/prettier
[Project-level settings]: https://github.com/jonlabelle/SublimeJsPrettier#project-level-settings
[Prettier v1.4+]: https://github.com/prettier/prettier/releases/tag/1.4.0
[Prettier v1.5+]: https://github.com/prettier/prettier/releases/tag/1.5.0
[Prettier v1.6+]: https://github.com/prettier/prettier/releases/tag/1.6.0
[Prettier v1.8+]: https://github.com/prettier/prettier/releases/tag/1.8.0
[requirePragma]: https://github.com/prettier/prettier#require-pragma
[#4]: https://github.com/jonlabelle/SublimeJsPrettier/issues/4
[#63]: https://github.com/jonlabelle/SublimeJsPrettier/issues/63
[#64]: https://github.com/jonlabelle/SublimeJsPrettier/issues/64
[#67]: https://github.com/jonlabelle/SublimeJsPrettier/issues/67
[#68]: https://github.com/jonlabelle/SublimeJsPrettier/issues/68
[#72]: https://github.com/jonlabelle/SublimeJsPrettier/issues/72
[`arrowParens`]: https://prettier.io/docs/en/options.html#arrow-function-parentheses
[Prettier v1.9+]: https://github.com/prettier/prettier/releases/tag/1.9.0
[Prettier v1.10+]: https://prettier.io/blog/2018/01/10/1.10.0.html
[Prettier v1.14+]: https://prettier.io/blog/2018/07/29/1.14.0.html#yaml
[Prettier v1.16+]: https://prettier.io/blog/2019/01/20/1.16.0.html#rename-babylon-parser-to-babel-5647-by-wuweiweiwu
[Prettier v1.16]: https://prettier.io/blog/2019/01/20/1.16.0.html
[default settings]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/JsPrettier.sublime-settings
[`--loglevel`]: https://prettier.io/docs/en/cli.html#loglevel
[Prettier PHP Plugin]: https://github.com/prettier/plugin-php
[Prettier v1.17+]: https://prettier.io/blog/2019/04/12/1.17.0.html
[Quote Props]: https://prettier.io/docs/en/options.html#quote-props
[Vue files script and style tags indentation]: https://prettier.io/docs/en/options.html#vue-files-script-and-style-tags-indentation
[Prettier v1.19+]: https://prettier.io/blog/2019/11/09/1.19.0.html
[`"vueIndentScriptAndStyle": <bool>`]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/JsPrettier.sublime-settings#L502
