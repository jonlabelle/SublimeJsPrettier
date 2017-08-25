#!/usr/bin/env bash

set -e

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

PIP_CMD=
resolve_pip()
{
    if [ -x "$(command -v pip)" ]; then
        PIP_CMD=$(which pip)
    elif [ -x "$(command -v pip2)" ]; then
        PIP_CMD=$(which pip2)
    elif [ -x "$(command -v pip3)" ]; then
        PIP_CMD=$(which pip3)
    else
        echo "Error: Could not resolve path to pip." >&2
        exit 1
    fi
}
resolve_pip

echo
echo '> Install package dependencies'
echo

pushd "${SCRIPTSDIR}" && pushd ..
"${PIP_CMD}" install -r requirements.txt
npm install -g markdownlint-cli
popd && popd

echo
echo 'Finished.'
echo
