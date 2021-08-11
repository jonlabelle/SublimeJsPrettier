#!/usr/bin/env bash

set -e
set -o pipefail

# shellcheck disable=SC2005,SC2155
readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

cd_project_root() { cd "${SCRIPTSDIR}" && cd ..; }

install_pip_requirements() {
    echo && echo '> Install pip requirements'
    pip3 install -r requirements.txt
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
