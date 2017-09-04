#!/usr/bin/env bash

set -e
[ "$TRAVIS" == "true" ] && set -x

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

echo
echo '> Run tests'
echo

pushd "${SCRIPTSDIR}" && pushd ..
py.test .
flake8 .
pylint JsPrettier.py
markdownlint .
popd && popd

echo
echo 'Finished.'
echo
