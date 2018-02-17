## Reporting an Issue

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

### Explain the Issue and Expected Behavior

Provide a story of the issue with as much detail as possible, including the expected behavior.

### Prettier version

To show the currently installed prettier version, run the following command:

    $ prettier --version
    <PRETTIER_VERSION>

### JsPrettier Plug-in Version

The JsPrettier Sublime Text Plug-in version is located in the `package.json` file.

    ...
    "name": "sublime-js-prettier",
    "version": "<JS_PRETTIER_PLUGIN_VERSION>",
    ...

### Platform Details

Provide your Sublime Text version and Platform details.

**Example**

    - Sublime Text Version: <SUBLIME_TEXT_VERSION>
    - Sublime Text Build: <SUBLIME_TEXT_BUILD>
    - Sublime Text Architecture: <SUBLIME_TEXT_ARCHITECTURE>
    - Operating System Name: <OS_NAME>
    - Operating System Version: <OS_VERSION>
    - Operating System Architecture: <OS_ARCHITECTURE>

### Generated Prettier command line arguments

To view the generated prettier command line arguments you need to enable JsPrettier's [debug setting] and open the Sublime Text Console after a file/section formatting attempt.

**Example**

    -----------------------------------------
     JsPrettier DEBUG - Prettier CLI Command 
    -----------------------------------------

    /usr/local/bin/prettier           \
        --stdin                       \
        --color=false                 \
        --print-width 80              \
        --single-quote=true           \
        --trailing-comma none         \
        --bracket-spacing=true        \
        --jsx-bracket-same-line=false \
        --parser babylon              \
        --semi=true                   \
        --tab-width 4                 \
        --use-tabs=true
        
> **NOTE:** The back-slashes (`\`) in the example above will not be printed to the Console... and only provided here for legibility purposes. The full prettier command will be output to the Console with no line-breaks.

### Is the same behavior observed when run against Prettier directly?

For example, the following command passes the contents of `messy_formatted_file.js` to Prettier as stdin (`--stdin`) and prints the formatted code back to stdout.

    /usr/local/bin/prettier           \
        --stdin                       \
        --color=false                 \
        --print-width 80              \
        --single-quote=true           \
        --trailing-comma none         \
        --bracket-spacing=true        \
        --jsx-bracket-same-line=false \
        --parser babylon              \
        --semi=true                   \
        --tab-width 4                 \
        --use-tabs=true               \
        < messy_formatted_file.js

### The contents of your `User/JsPrettier.sublime-settings` file

The entire contents of your ***User*** overridden JsPrettier Settings, excluding the comments.

**Example JsPrettier.sublime-settings**

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
    
### The contents of your `<project_name>.sublime-project` file (if applicable)

The entire contents of your ***User*** overridden JsPretter Project-level Settings, excluding the comments.

**Example**

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

### Steps to reproduce the behavior

The steps one would take to reproduce and observe the problem.

    1. This is the first step
    2. This is the second step
    3. Further steps, etc.

    Any other information you want to share that is relevant to the issue being
    reported. This might include the lines of code that you have identified as
    causing the bug, and potential solutions (and your opinions on their
    merits).

[debug setting]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/JsPrettier.sublime-settings#L14
