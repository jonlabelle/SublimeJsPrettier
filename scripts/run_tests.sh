#!/usr/bin/env bash

set -e
set -o pipefail

# shellcheck disable=SC2005,SC2155
readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

cd_project_root() { cd "${SCRIPTSDIR}" && cd ..; }

run_pytest() {
    echo
    echo '> Run pytest'
    py.test .
}

run_flake8() {
    echo
    echo '> Run flake8'
    echo -n 'Total errors: '
    flake8 . --count --show-source --statistics
}

run_pylint() {
    echo
    echo '> Run pylint'
    pylint --rcfile .pylintrc .
}

run_markdownlint() {
    echo '> Run markdownlint'
    markdownlint .
    echo 'Markdown looks good.' && echo
}


main() {
    cd_project_root
    run_pytest
    run_flake8
    run_pylint
    run_markdownlint

    echo & echo 'Finished.'
}

main
