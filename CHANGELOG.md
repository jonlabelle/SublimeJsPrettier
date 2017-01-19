# Changelog

## 1.0.2

Release Date: 2017-01-19

- Remove the default value for "node_path", and internally try to sniff out the
  appropriate path.

## 1.0.1

Release Date: 2017-01-18

- Fixed package path to use "JsPrettier" instead of "SublimeJsPrettier".
  Previously caused the "Default" settings file not to open from the Main Menu.

- Add notice regarding local installations of Prettier. The `node_modules`
  directory will be deleted after every package update pushed by Package
  Control.

## 1.0.0

Release Date: 2017-01-18

- Initial release.
- Now available for installation using [Package Control].

[Package Control]: https://packagecontrol.io/packages/JsPrettier
