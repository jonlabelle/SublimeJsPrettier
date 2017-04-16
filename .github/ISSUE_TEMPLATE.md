## Reporting an Issue

When reporting an issue, please include the information with your post:

- [ ] Your installed **Prettier version** (`$ prettier --version`)
- [ ] The installed **JsPrettier version** (located in the `package.json` file)
- [ ] The generated **command line arguments** passed to the Prettier CLI
- [ ] **Steps to reproduce** the behavior

### Example

**Prettier version**

```
$ prettier --version
1.1.0
```

**JsPrettier version** (package.json)

```json
  "name": "sublime-js-prettier",
  "version": "1.7.2",
```

**Prettier command line arguments** (enable the `debug` setting and open the ST console)

```
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
```

***Steps to reproduce the behavior***

1. ...
2. ...
3. ...
