## Reporting an Issue

When [reporting an issue](https://github.com/jonlabelle/SublimeJsPrettier/issues), please include the following information in your post:

- [ ] **Explain the issue**
- [ ] **Prettier version**
- [ ] **JsPrettier Plug-in Version**
- [ ] **Platform Details**
- [ ] **Generated Prettier command line arguments**
- [ ] **Is the same behavior observed when run against Prettier directly?**
- [ ] **The contents of your** `User/JsPrettier.sublime-settings` **file**
- [ ] **The contents of your** `<project_name>.sublime-project` **file (if applicable)**
- [ ] **Steps to reproduce the behavior**

---

**Explain the issue**

*A story of the issue with as much detail as possible...*

**Prettier version** (command line)

    $ prettier --version
    <PRETTIER_VERSION>

**JsPrettier Plug-in Version** (package.json)

*Example*

    ...
    "name": "sublime-js-prettier",
    "version": "<JS_PRETTIER_PLUGIN_VERSION>",
    ...

**Platform Details**

*Example*

    - Sublime Text Version: <SUBLIME_TEXT_VERSION>
    - Sublime Text Build: <SUBLIME_TEXT_BUILD>
    - Sublime Text Architecture: <SUBLIME_TEXT_ARCHITECTURE>
    - Operating System Name: <OS_NAME>
    - Operating System Version: <OS_VERSION>
    - Operating System Architecture: <OS_ARCHITECTURE>

**Generated Prettier command line arguments**

To view the generated prettier command line arguments you need to enable JsPrettier's [debug setting] and open the Sublime Text Console after a file/section formatting attempt.

*Example*

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

**Is the same behavior observed when run against Prettier directly?**  

For example, to pass the contents of file `path_to_js_file.js` to Prettier from the command line.

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
        < path_to_js_file.js

**The contents of your** `User/JsPrettier.sublime-settings` **file (without the comments)**

    {
        "debug": false,
        "prettier_cli_path": "",
        "node_path": "",
        "auto_format_on_save": false,
        "allow_inline_formatting": false,
        "custom_file_extensions": [],
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
    
**The contents of your** `<project_name>.sublime-project` **file (if applicable)**

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
                "custom_file_extensions": [],
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

**Steps to reproduce the behavior**

    1. ...
    2. ...
    3. ...

[debug setting]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/JsPrettier.sublime-settings#L9
