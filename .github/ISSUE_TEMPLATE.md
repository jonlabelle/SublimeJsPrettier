## Reporting an Issue

When [reporting an issue](https://github.com/jonlabelle/SublimeJsPrettier/issues),
please include the following information in your post:

- [ ] **Explain the issue**
- [ ] **Prettier version**
- [ ] **JsPrettier version**
- [ ] **Platform details**
- [ ] **The generated Prettier command line arguments**
- [ ] **Steps to reproduce the behavior**
- [ ] **Is the same behavior observed when run against Prettier directly?**

### Example

**Explain the issue**

*Explain the issue with as much detail as possible...*

**Prettier version** (command line)

    $ prettier --version
    <PRETTIER_VERSION>

**JsPrettier version** (package.json)

    ...
    "name": "sublime-js-prettier",
    "version": "<JS_PRETTIER_PLUGIN_VERSION>",
    ...

**Platform details**

    - Sublime Text Version: <SUBLIME_TEXT_VERSION>
    - Sublime Text Build: <SUBLIME_TEXT_BUILD>
    - Sublime Text Architecture: <SUBLIME_TEXT_ARCHITECTURE>
    - Operating System Name: <OS_NAME>
    - Operating System Version: <OS_VERSION>
    - Operating System Architecture: <OS_ARCHITECTURE>

**Prettier command line arguments** (enable the [debug setting] and open the Sublime
Text console to view the cli args passed to Prettier)

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

**Is the same behavior observed when run against Prettier directly?** For
example, to pass the contents of file `path_to_js_file.js` to Prettier from the
command line.

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

**Steps to reproduce the behavior**

    1. ...
    2. ...
    3. ...

[debug setting]: https://github.com/jonlabelle/SublimeJsPrettier/blob/master/JsPrettier.sublime-settings#L9
