#!/usr/bin/env bash

set -e
set -o pipefail

[ "$TRAVIS" == "true" ] && set -x

# shellcheck disable=SC2005
readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"
readonly SCRIPTNAME="$(basename "${BASH_SOURCE[0]}")"

SONAR_LOGIN=$1
SONAR_SCANNER_CMD=$2

cd_project_root() { cd "${SCRIPTSDIR}" && cd ..; }

show_info()    { echo -e "\\e[36m${1}\\e[0m"; }
show_success() { echo -e "\\e[32m${1}\\e[0m"; }
show_warning() { echo -e "\\e[33m${1}\\e[0m"; }
show_error()   { echo -e "\\e[31mError:\\e[0m ${1}"; }

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
# Resolve sonar scanner login var:
if [ -z "$SONAR_LOGIN" ]; then
    show_error "Missing positional arg(1) for 'SONAR_LOGIN' (API Key)."
    show_usage
    exit 1
fi

#
# Resolve sonar scanner command/executable var:
if [ -z "$SONAR_SCANNER_CMD" ]; then
    if [ -x "$(command -v sonar-scanner)" ]; then
        SONAR_SCANNER_CMD=$(command -v sonar-scanner)
    else
        show_error "Missing positional arg(2) for 'SONAR_SCANNER_CMD'."
        show_usage
        exit 1
    fi
fi

run_scan
show_success 'Finished.'
