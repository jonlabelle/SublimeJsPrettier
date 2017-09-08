#!/usr/bin/env bash

set -e
[ "$TRAVIS" == "true" ] && set -x

readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"


cd_project_root() {
    echo '> cd to project root'
    pushd "${SCRIPTSDIR}" && pushd ..
}

cd_previous_working_dir() {
    echo '> Restore previous working directory'
    popd && popd
    echo
}

run_pytest() {
    echo
    echo '> Run pytest'
    py.test .
}

run_flake8() {
    echo
    echo '> Run flake8'
    echo -n 'Total errors: '
    flake8 . --count
}

run_pylint() {
    echo
    echo -n '> Run pylint'
    pylint JsPrettier.py
}

run_markdownlint() {
    echo -n '> Run markdownlint'
    markdownlint .
    echo 'Markdown looks good.' && echo
}


main() {
    cd_project_root
    run_pytest
    run_flake8
    run_pylint
    run_markdownlint
    cd_previous_working_dir

    echo & echo 'Finished.'
}

main
