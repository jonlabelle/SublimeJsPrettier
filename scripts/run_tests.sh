#!/usr/bin/env bash

set -e
[ "$TRAVIS" == "true" ] && set -x

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

pushd "${SCRIPTSDIR}" && pushd ..

echo
echo '> Run pytest'
py.test .

echo
echo '> Run flake8'
flake8 .

echo
echo '> Run pylint'
pylint JsPrettier.py

echo
echo '> Run markdownlint'
markdownlint .

echo
popd && popd
echo

echo 'Finished.'

