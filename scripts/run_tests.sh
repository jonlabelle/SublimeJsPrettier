#!/usr/bin/env bash

set -e
set -x

#
# cd to project root and run tests
#

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo $(pwd))"
pushd "${SCRIPTSDIR}"
pushd ..

pytest .
flake8 .

popd
popd
