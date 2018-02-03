#!/usr/bin/env bash

##
# Release tasks bulked into one script w/ user intervention/confirmation
# required.
#
# - Bumps 'package.json' version field to the passed <semver> arg (1).
# - Commit and push the change (to master).
# - Create and push passed <semver> arg (1) git tag.
# - Run npm publish.
#
# Usage:
#
#   $ release.sh [options] [version]
#
# Examples:
#
#   To bump and tag to the specified version (1.2.1):
#       $ release.sh 1.2.1
#
#   To bump and tag automatically incrementing to the next patch version:
#       $ release.sh --next
##

set -e

VERSION=$1
PREVIOUS_VERSION="$(git describe --abbrev=0 --tags)"
NEXT_VERSION="${PREVIOUS_VERSION%.*}.$((${PREVIOUS_VERSION##*.}+1))"

readonly PREVIOUSWRKDIR="$(pwd)"
readonly SCRIPTSDIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"
readonly SCRIPTNAME="$(basename "${BASH_SOURCE[0]}")"


cd_project_root() {
    cd "${SCRIPTSDIR}" && cd ..
}

cd_previous_working_dir() {
    [ -d "${PREVIOUSWRKDIR}" ] && cd "${PREVIOUSWRKDIR}"
}

show_info() {
    echo -e "\\e[36m${1}\\e[0m"
}

show_success() {
    echo -e "\\e[32m${1}\\e[0m"
}

show_warning() {
    echo -e "\\e[33m${1}\\e[0m"
}

show_error() {
    echo -e "\\e[31mError:\\e[0m ${1}"
}

show_usage() {
    echo
    echo "Usage: $SCRIPTNAME [options] [version]"
    echo
    echo "Release tasks bulked into one script."
    echo
    echo "OPTIONS"
    echo "    -n, --next    auto-increment to the next patch version"
    echo "    -h, --help    show usage"
    echo
}

validate_version() {
    if [[ ! ${VERSION} =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        show_error "'$VERSION' is not a valid semver/version number (ex: 1.2.1)."
        exit 1
    fi
}

ensure_git_branch_is_master() {
    show_info "> Ensure current branch is 'master'"
    local git_branch=$(git rev-parse --abbrev-ref HEAD)
    if [ "$git_branch" != "master" ]; then
        show_error "'$SCRIPTNAME' must be run on the 'master' branch, and the current branch is '$git_branch'."
        exit 1
    fi
}

ensure_git_branch_is_up_to_date() {
    # compare local/remote hashes: https://stackoverflow.com/a/15119807
    show_info "> Ensure 'master' branch is up-to-date with remote"
    local git_local_hash="$(git rev-parse --verify origin/master)"
    local git_remote_hash="$(git ls-remote origin master | cut -d$'\t' -f 1)"
    if [ "$git_local_hash" != "$git_remote_hash" ]; then
        show_error "git remote history differs. please pull remote changes first."
        exit 1
    fi
}

ensure_git_repo_is_clean() {
    show_info "> Ensure repo is clean"
    if ! git diff-index --quiet HEAD --; then
        show_error "git repo is dirty. commit all changes before using '$SCRIPTNAME'."
        exit 1
    fi
}

bump_package_json_version() {
    show_info "> Bump version in 'package.json' file, 'v$PREVIOUS_VERSION' -> 'v$VERSION'"
    local tmp_pkg_file="${TMPDIR:-/tmp}/package.json.$$"
    sed -E s/'"version"\: "[0-9]+\.[0-9]+\.[0-9]+"'/'"version"\: "'"$VERSION"'"'/ package.json > "$tmp_pkg_file" && mv "$tmp_pkg_file" package.json
    grep "$VERSION" -C 1 package.json
}

ensure_only_one_file_changed() {
    show_info "> Ensure only one file changed (package.json and version field)"
    if [[ ! $(git diff --stat) =~ "1 file changed, 1 insertion(+), 1 deletion(-)" ]]; then
        show_error "expected '1 file changed, 1 insertion(+), 1 deletion(-)'. check git status and git diff."
        exit 1
    fi
}

confirm_git_commit_tag_release() {
    show_info "> Acquire confirmation"
    while true; do
        read -r -p "Ready to commit, tag and release 'v$VERSION'? (y/n): " yn
        case ${yn} in
            [Yy]* )   break;;
            [NnQq]* ) exit;;
            * ) show_warning "Please answer [Y]es or [N]o.";;
        esac
    done
}

git_commit_tag_release() {
    show_info "> git commit/push/tag/push --tags"
    set -x
    git add package.json
    git commit -m "Bump to v$VERSION"
    git push origin master
    git tag -a "$VERSION" -m "Tag v$VERSION"
    git push --tags
    set +x
}

npm_publish() {
    show_info "> Publish npm package"
    npm publish
}


main() {
    validate_version
    cd_project_root
    ensure_git_branch_is_master
    ensure_git_branch_is_up_to_date
    ensure_git_repo_is_clean
    bump_package_json_version
    ensure_only_one_file_changed
    confirm_git_commit_tag_release
    git_commit_tag_release
    npm_publish
    cd_previous_working_dir

    echo && show_success "Finished." && echo
}

if [ $# -eq 0 ]; then
    show_error "a valid semver number for the new release is required"
    echo "Currently, the latest release is '$(show_success "${PREVIOUS_VERSION}")'"
    show_usage
    exit 1
else
    if [ "$1" = "-n" ] || [ "$1" = "--next" ]; then
        VERSION=${NEXT_VERSION}
    fi
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_usage
        exit 0
    fi
    main
fi
