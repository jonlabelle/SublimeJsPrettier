#!/usr/bin/env bash

set -e
set -o pipefail

# shellcheck disable=SC2005,SC2155
readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

cd_project_root() { cd "${SCRIPTSDIR}" && cd ..; }

install_pip_requirements() {
    echo && echo '> Initializing python virtual environment'
    python3 -m venv venv

    echo
    pyversion="$(python --version)"
    echo "$pyversion virtual environment initialized"

    echo && echo "> Activate $pyversion virtual environment (venv)"
    # shellcheck disable=SC1091
    source venv/bin/activate

    echo && echo '> Ensure pip upgrade'
    python -m ensurepip --upgrade

    echo && echo '> Install pip requirements'
    python -m pip install -r requirements.txt
}

install_npm_packages() {
    echo && echo '> Install npm packages'
    npm install -g markdownlint-cli
}

main() {
    cd_project_root
    install_pip_requirements
    install_npm_packages
    echo && echo 'Finished.'
}

main
