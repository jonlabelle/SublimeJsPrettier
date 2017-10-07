#!/usr/bin/env bash

set -e

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"
readonly SCRIPTNAME="$(basename "${BASH_SOURCE[0]}")"

SONAR_LOGIN=$1
SONAR_SCANNER_CMD=$2


show_info() {
    local msg="$1"
    echo -e "\\e[36m${msg}\\e[0m"
}

show_success() {
    local msg="$1"
    echo -e "\\e[32m${msg}\\e[0m"
}

show_warning() {
    local msg="$1"
    echo -e "\\e[33mwarning\\e[0m : ${msg}"
}

show_error() {
    local msg="$1"
    echo -e "\\e[31merror\\e[0m : ${msg}"
}


show_usage() {
    echo "Usage:"
    echo
    echo "    $SCRIPTNAME <SONAR_LOGIN/API_KEY> [path/to/sonar-scanner]"
}

is_readable_file() {
    local filepath=$1
    if [ -r "$filepath" ] && [ -f "$filepath" ]; then
        return 0
    fi
    return 1
}

cd_project_root() {
    show_info '> cd to project root'
    pushd "${SCRIPTSDIR}" && pushd ..
    echo
}

cd_previous_working_dir() {
    show_info '> Restore previous working directory'
    popd && popd
    echo
}

run_scan() {
    show_info '> Run sonar scan analysis'
    "${SONAR_SCANNER_CMD}" -Dsonar.login="${SONAR_LOGIN}"
    echo
}


cd_project_root

#
# if no args passed... try to suck in .env file:
if [ $# -eq 0 ]; then
    show_info "> No command args specified... looking for '.env' file in project root"
    if is_readable_file .env; then
        show_success "using '.env' file found in project root"
        source .env
        echo
    else
        show_error "no '.env' file found in project root"
        echo
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
cd_previous_working_dir
show_success 'Finished.'
