#!/usr/bin/env bash

set -e

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

SONAR_LOGIN=$1
SONAR_SCANNER_CMD=$2

show_info() {
    local msg="$1"
    echo -e "\e[36m${1}\e[0m"
}

show_success() {
    local msg="$1"
    echo -e "\e[32m${msg}\e[0m"
}

show_warning() {
    local msg="$1"
    echo -e "\e[33mwarning\e[0m : ${1}"
}

show_error() {
    local msg="$1"
    echo -e "\e[31merror\e[0m : ${1}"
}

cd_root_dir() {
    show_info '> cd to project root'
    echo
    pushd "${SCRIPTSDIR}" && pushd ..
}

cd_previous_dir() {
    show_info '> Restore previous working directory'
    echo
    popd && popd
}

show_usage() {
    echo "Usage: bash $SCRIPT_NAME <SONAR_LOGIN/API_KEY> [path/to/sonar-scanner]"
}

run_scan() {
    echo
    show_info '> Run sonar scanner analysis'
    echo
    "${SONAR_SCANNER_CMD}" -Dsonar.login="${SONAR_LOGIN}"
    echo
}

cd_root_dir

#
# if no args passed... try to suck in .env file:
if [ $# -eq 0 ]; then
    if [ -r .env ] && [ -f .env ]; then
        source .env
    else
        show_usage
        exit 1
    fi
fi

#
# Set sonar scan params:
if [ -z "$SONAR_LOGIN" ]; then
    show_error "ERROR: Missing positional arg(1) for 'SONAR_LOGIN/API_KEY'"
    show_usage
    exit 1
fi
if [ -z "$SONAR_SCANNER_CMD" ]; then
    SONAR_SCANNER_CMD=sonar-scanner
fi

run_scan
cd_previous_dir

echo
show_success 'Finished.'
echo
