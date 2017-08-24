#!/usr/bin/env bash

set -e

SONAR_LOGIN=$1
SONAR_SCANNER_CMD=$2

if [ $# -eq 0 ]; then
    echo "Usage: run_sonar_scan.sh <sonar login/api key> [sonar scanner command path]"
    exit 1
fi
if [ -z "$SONAR_LOGIN" ]; then
    echo "ERROR: Missing positional arg(2) for 'sonar.login' (api token)"
    exit 1
fi
if [ -z "$SONAR_SCANNER_CMD" ]; then
    SONAR_SCANNER_CMD=sonar-scanner
fi

# cd to project root and run analysis:
echo
echo '> Run sonar analysis'
echo
SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"
pushd "${SCRIPTSDIR}" && pushd ..
"${SONAR_SCANNER_CMD}" -Dsonar.login="${SONAR_LOGIN}"
echo
echo Finished.

popd && popd
