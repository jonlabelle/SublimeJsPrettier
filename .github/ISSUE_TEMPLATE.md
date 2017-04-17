## Reporting an Issue

When [reporting an issue](https://github.com/jonlabelle/SublimeJsPrettier/issues),
please include the following information in your post:

- [ ] Your installed **Prettier** version
- [ ] Your installed **JsPrettier** version
- [ ] The generated **command line arguments** passed to Prettier
- [ ] **Steps to reproduce** the behavior
- [ ] Is the same behavior observed when **run against Prettier directly** from the command line?

### Example

**Prettier version**

    $ prettier --version
    1.1.0

**JsPrettier version** (package.json)

    "name": "sublime-js-prettier",
    "version": "1.7.2",

**Prettier command line arguments** (enable the `debug` setting and open the ST console)

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

Is the same behavior observed when **run against Prettier directly** from the
command line? For example, to pass the contents of file `path_to_js_file.js` to
Prettier from the command line.

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

**Steps to reproduce** the behavior

    1. ...
    2. ...
    3. ...
