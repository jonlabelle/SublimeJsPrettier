#!/usr/bin/env bash

set -e
set -o pipefail

# shellcheck disable=SC2005,SC2155
readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

cd_project_root() { cd "${SCRIPTSDIR}" && cd ..; }

activate_venv() {
    if [[ -d "venv" ]]; then
        # shellcheck disable=SC1091
        source venv/bin/activate
    fi
}

run_pytest() {
    echo
    echo '> Run pytest'
    activate_venv
    python -m pytest || {
        echo "pytest failed"
        exit 1
    }
}

run_flake8() {
    echo
    echo '> Run flake8'
    activate_venv
    echo -n 'Total errors: '
    python -m flake8 . --count --show-source --statistics || {
        echo "flake8 failed"
        exit 1
    }
}

run_pylint() {
    echo
    echo '> Run pylint'
    activate_venv
    python -m pylint . || {
        echo "pylint failed"
        exit 1
    }
}

run_markdownlint() {
    echo '> Run markdownlint'
    markdownlint-cli2 . || {
        echo "markdownlint failed"
        exit 1
    }
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
