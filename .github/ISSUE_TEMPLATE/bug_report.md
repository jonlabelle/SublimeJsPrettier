---
name: Bug report
about: Create a bug report to help us improve
title: ''
labels: 'investigating'
assignees: jonlabelle

---

---

> [!WARNING]  
> Failure to provide adequate details of your problem, as demonstrated in this document, will result in automatic closure of your issue. Please don't waste our time, or yours.

---

When [reporting an issue](https://github.com/jonlabelle/SublimeJsPrettier/issues), please include the following information in your post:

- [ ] **Explain the Issue and Expected Behavior**
- [ ] **Prettier version**
- [ ] **JsPrettier Plug-in Version**
- [ ] **Platform Details**
- [ ] **Generated Prettier command line arguments**
- [ ] **Is the same behavior observed when run against Prettier directly?**
- [ ] **The contents of your** `User/JsPrettier.sublime-settings` **file**
- [ ] **The contents of your** `<project_name>.sublime-project` **file (if applicable)**
- [ ] **Steps to reproduce the behavior**

---

## Explain the Issue and Expected Behavior

Provide a story of the issue with as much detail as possible, including the expected behavior.

## Prettier version

To show the currently installed prettier version, run the following command:

```console
prettier --version
```

## JsPrettier Plug-in Version

The JsPrettier Sublime Text Plug-in version is located in the `package.json` file.

```json
"name": "sublime-js-prettier",
"version": "<JS_PRETTIER_PLUGIN_VERSION>",
```

## Platform Details

Provide your Sublime Text version and Platform details.

**Example**

```
- Sublime Text Version: <SUBLIME_TEXT_VERSION>
- Sublime Text Build: <SUBLIME_TEXT_BUILD>
- Sublime Text Architecture: <SUBLIME_TEXT_ARCHITECTURE>
- Operating System Name: <OS_NAME>
- Operating System Version: <OS_VERSION>
- Operating System Architecture: <OS_ARCHITECTURE>
```

## Generated Prettier command line arguments

To view the generated prettier command line arguments you need to enable JsPrettier's [debug setting] and open the Sublime Text Console after a file/section formatting attempt.

**Example**

```console
-----------------------------------------
 JsPrettier DEBUG - Prettier CLI Command
-----------------------------------------

/usr/local/bin/prettier                 \
    --no-config                         \
    --print-width 80                    \
    --tab-width 2                       \
    --single-quote false                \
    --trailing-comma all                \
    --bracket-spacing true              \
    --bracket-same-line false           \
    --jsx-single-quote false            \
    --parser babel                      \
    --semi true                         \
    --require-pragma false              \
    --prose-wrap preserve               \
    --arrow-parens always               \
    --html-whitespace-sensitivity css   \
    --quote-props as-needed             \
    --vue-indent-script-and-style false \
    --embedded-language-formatting auto \
    --use-tabs false                    \
    --editorconfig true                 \
    --single-attribute-per-line false   \
    --stdin-filepath messy.js           \
    --log-level debug

Prettier produced the following output:

[debug] normalized argv: {"_":[],"bracket-spacing":true,"color":true",...}
[debug] '--no-config' option found, skip loading config file.
[debug] applied config-precedence (cli-override): {"filepath":"messy.js",...}
```

> **NOTE:** The back-slashes (`\`) in the example above will not be printed to the Console... and only provided here for legibility purposes. The full prettier command will be output to the Console with no line-breaks.

## Is the same behavior observed when run against Prettier directly?

For example, the following command passes the contents of `messy.js` to Prettier and prints the formatted to stdout:

```console
/usr/local/bin/prettier                 \
    --no-config                         \
    --print-width 80                    \
    --tab-width 2                       \
    --single-quote false                \
    --trailing-comma all                \
    --bracket-spacing true              \
    --bracket-same-line false           \
    --jsx-single-quote false            \
    --parser babel                      \
    --semi true                         \
    --require-pragma false              \
    --prose-wrap preserve               \
    --arrow-parens always               \
    --html-whitespace-sensitivity css   \
    --quote-props as-needed             \
    --vue-indent-script-and-style false \
    --embedded-language-formatting auto \
    --use-tabs false                    \
    --editorconfig true                 \
    --single-attribute-per-line false   \
    --stdin-filepath messy.js           \
    --log-level debug                   \
    < messy.js
```

## The contents of your `User/JsPrettier.sublime-settings` file

The entire contents of your **_User_** overridden JsPrettier Settings, excluding the comments.

**Example JsPrettier.sublime-settings**

```json
{
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
    "trailingComma": "all",
    "bracketSpacing": true,
    "bracketSameLine": false,
    "jsxSingleQuote": false,
    "parser": "babel",
    "semi": true,
    "requirePragma": false,
    "proseWrap": "preserve",
    "arrowParens": "always",
    "htmlWhitespaceSensitivity": "css",
    "quoteProps": "as-needed",
    "vueIndentScriptAndStyle": false,
    "embeddedLanguageFormatting": "auto",
    "editorconfig": true,
    "singleAttributePerLine": false
  }
}
```

## The contents of your `<project_name>.sublime-project` file (if applicable)

The entire contents of your **_User_** overridden JsPretter Project-level Settings, excluding the comments.

**Example**

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
        "trailingComma": "all",
        "bracketSpacing": true,
        "bracketSameLine": false,
        "jsxSingleQuote": false,
        "parser": "babel",
        "semi": true,
        "requirePragma": false,
        "proseWrap": "preserve",
        "arrowParens": "always",
        "htmlWhitespaceSensitivity": "css",
        "quoteProps": "as-needed",
        "vueIndentScriptAndStyle": false,
        "embeddedLanguageFormatting": "auto",
        "editorconfig": true,
        "singleAttributePerLine": false
      }
    }
  }
}
```

## Steps to reproduce

The steps one would take to reproduce the behavior and observe the problem.

1. This is the first step
2. This is the second step
3. Further steps, etc.

> Any other information you want to share that is relevant to the issue being
> reported. This might include the lines of code that you have identified as
> causing the bug, and potential solutions (and your opinions on their merits).

## Attach minimal project

Attach a minimal project required to reproduce the issue.

> [!IMPORTANT]
> Please attach it in **zip format** and DO NOT include your `node_modules` directory.

[debug setting]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/JsPrettier.sublime-settings#L14
