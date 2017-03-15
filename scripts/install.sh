#!/usr/bin/env bash

set -e
set -x

#
# cd to project root and install dev/test dependencies
#

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo $(pwd))"
pushd "${SCRIPTSDIR}"
pushd ..

pip install -r requirements.txt

popd
popd
