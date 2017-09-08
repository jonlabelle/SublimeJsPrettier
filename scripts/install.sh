#!/usr/bin/env bash

set -e
[ "$TRAVIS" == "true" ] && set -x

PIP_CMD=

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

cd_project_root() {
    echo '> cd to project root'
    pushd "${SCRIPTSDIR}" && pushd ..
}

cd_previous_working_dir() {
    echo '> Restore previous working directory'
    popd && popd
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

resolve_pip_cmd()
{
    echo '> Resolve pip command'

    local py_major_ver="$1"
    local pip_cmd_ver="pip${py_major_ver}"

    if [ -x "$(command -v pip)" ]; then
        PIP_CMD=$(which pip)
    elif [ -x "$(command -v "$pip_cmd_ver")" ]; then
        PIP_CMD=$(which "$pip_cmd_ver")
    else
        echo "Error: Could not resolve path to pip." >&2
        exit 1
    fi

    echo "$PIP_CMD"
}

install_pip_requirements() {
    echo '> Install pip requirements'
    "${PIP_CMD}" install -r requirements.txt
}

install_npm_packages() {
    echo '> Install npm packages'
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
