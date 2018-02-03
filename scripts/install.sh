#!/usr/bin/env bash

set -e
[ "$TRAVIS" == "true" ] && set -x

readonly PREVIOUSWRKDIR="$(pwd)"
readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

PIPCMD=


cd_project_root() {
    cd "${SCRIPTSDIR}" && cd ..
}

cd_previous_working_dir() {
    [ -d "${PREVIOUSWRKDIR}" ] && cd "${PREVIOUSWRKDIR}"
}

python_major_version() {
    echo -n "> Parse Python major version " >&2

    local py_ver=
    local py_major_ver=

    py_ver="$(python --version 2>&1)"
    echo "($py_ver)" >&2
    py_major_ver="$(echo "$py_ver" | cut -d' ' -f 2 | cut -d'.' -f 1)"
    echo "major version is '$py_major_ver'" >&2
    echo "$py_major_ver"
}

resolve_pip_cmd() {
    echo && echo '> Resolve pip command'

    local py_major_ver="$1"
    local pip_cmd_ver="pip${py_major_ver}"

    if [ -x "$(command -v pip)" ]; then
        PIPCMD=$(which pip)
    elif [ -x "$(command -v "$pip_cmd_ver")" ]; then
        PIPCMD=$(which "$pip_cmd_ver")
    else
        echo "Error: Could not resolve path to pip." >&2
        exit 1
    fi

    echo "$PIPCMD"
}

install_pip_requirements() {
    echo && echo '> Install pip requirements'
    "${PIPCMD}" install -r requirements.txt
}

install_npm_packages() {
    echo && echo '> Install npm packages'
    npm install -g markdownlint-cli
}


main() {
    cd_project_root
    resolve_pip_cmd "$(python_major_version)"
    install_pip_requirements
    install_npm_packages
    cd_previous_working_dir

    echo && echo 'Finished.'
}

main
