#!/usr/bin/env bash

set -e

SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

# cd to project root
pushd "${SCRIPTSDIR}" && pushd ..

SONAR_LOGIN=$1
SONAR_SCANNER_CMD=$2

# if no args passed... try to suck in .env file:
if [ $# -eq 0 ]; then
    if [ -r .env ] && [ -f .env ]; then
        source .env
    else
        echo "Usage: run_sonar_scan.sh <sonar login/api key> [sonar scanner command path]"
        exit 1
    fi
fi

if [ -z "$SONAR_LOGIN" ]; then
    echo "ERROR: Missing positional arg(1) for 'SONAR_LOGIN' (api token)"
    exit 1
fi
if [ -z "$SONAR_SCANNER_CMD" ]; then
    SONAR_SCANNER_CMD=sonar-scanner
fi

echo
echo '> Run sonar scanner analysis'
echo

"${SONAR_SCANNER_CMD}" -Dsonar.login="${SONAR_LOGIN}"
popd && popd

echo
echo 'Finished.'
echo
