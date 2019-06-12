#!/usr/bin/env bash

set -e
set -o pipefail
[ "$TRAVIS" == "true" ] && set -x

NEW_VERSION=
CURRENT_VERSION="$(git describe --abbrev=0 --tags)"

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
    echo "Usage: $SCRIPTNAME [options] <major|minor|patch|semver>"
    echo
    echo "Positional arguments:"
    echo
    echo "  (1) patch      auto-increment to the next patch version"
    echo "  (1) minor      auto-increment to the next minor version"
    echo "  (1) major      auto-increment to the next major version"
    echo "  (1) semver     a specific version number (as semver)"
    echo
    echo "Options:"
    echo
    echo "  -h, --help     show help/usage and exit"
    echo "  -v, --version  show the current version and exit"
    echo
    echo "Examples:"
    echo
    echo "To bump the release to the next 'major' version:"
    echo "  $ $SCRIPTNAME major"
    echo
    echo "To bump the release to the next 'minor' version:"
    echo "  $ $SCRIPTNAME minor"
    echo
    echo "To bump the release to the next 'patch' version:"
    echo "  $ $SCRIPTNAME patch"
    echo
    echo "To bump the release to a specific semver version:"
    echo "  $ $SCRIPTNAME 1.2.1"
    echo
}

run_install() {
    show_info "> Run install"
    bash scripts/install.sh
}

run_tests() {
    show_info "> Run tests"
    bash scripts/run_tests.sh
}

bump_new_version() {
    local semver_part_to_bump oldIFS version_parts major minor patch

    semver_part_to_bump=$1

    oldIFS="$IFS"
    IFS='.' read -a version_parts <<< "$CURRENT_VERSION"
    IFS="$oldIFS"

    major=${version_parts[0]}
    minor=${version_parts[1]}
    patch=${version_parts[2]}

    case "$semver_part_to_bump" in
        "major")
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        "minor")
            minor=$((minor + 1))
            patch=0
            ;;
        "patch")
            patch=$((patch + 1))
            ;;
    esac

    NEW_VERSION="$major.$minor.$patch"
}

validate_version() {
    local ver
    ver=$1
    if [[ ! ${ver} =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        show_error "'${ver}' is not a valid semver/version number (ex: 1.2.1)."
        return 1
    fi
    return 0
}

ensure_git_branch_is_master() {
    local git_branch
    show_info "> Ensure current branch is 'master'"
    git_branch=$(git rev-parse --abbrev-ref HEAD)
    if [ "$git_branch" != "master" ]; then
        show_error "'$SCRIPTNAME' must be run on the 'master' branch, and the current branch is '$git_branch'."
        exit 1
    fi
}

ensure_git_branch_is_up_to_date() {
    local git_local_hash git_remote_hash
    # compare local/remote hashes: https://stackoverflow.com/a/15119807
    show_info "> Ensure 'master' branch is up-to-date with remote"
    git_local_hash="$(git rev-parse --verify origin/master)"
    git_remote_hash="$(git ls-remote origin master | cut -d$'\t' -f 1)"
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
    show_info "> Bump version in 'package.json' file, 'v$CURRENT_VERSION' -> 'v$NEW_VERSION'"
    local tmp_pkg_file="${TMPDIR:-/tmp}/package.json.$$"
    sed -E s/'"version"\: "[0-9]+\.[0-9]+\.[0-9]+"'/'"version"\: "'"$NEW_VERSION"'"'/ package.json > "$tmp_pkg_file" && mv "$tmp_pkg_file" package.json
    grep "$NEW_VERSION" -C 1 package.json
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
        read -r -p "Ready to commit, tag and release 'v$NEW_VERSION'? (y/n): " yn
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
    git commit -m "Bump to v$NEW_VERSION"
    git push origin master
    git tag -a "$NEW_VERSION" -m "Tag v$NEW_VERSION"
    git push --tags
    set +x
}

npm_publish() {
    show_info "> Publish npm package"
    npm publish
}


main() {
    cd_project_root
    ensure_git_branch_is_master
    ensure_git_branch_is_up_to_date
    ensure_git_repo_is_clean
    run_install
    run_tests
    bump_package_json_version
    ensure_only_one_file_changed
    confirm_git_commit_tag_release
    git_commit_tag_release
    npm_publish
    cd_previous_working_dir
    show_success "\nFinished.\n"
}

if [ $# -eq 0 ]; then
    show_error "a valid semver/version number for the new release is required"
    echo
    echo "Currently, the latest release is '$(show_success "${CURRENT_VERSION}")'"
    echo
    show_usage
    exit 1
else
    if [ "$1" = "patch" ] || [ "$1" = "minor" ] || [ "$1" = "major" ]; then
        bump_new_version "$1"
        main
    elif [ "$1" = "-v" ] || [ "$1" = "--version" ]; then
        echo "${CURRENT_VERSION}"
        exit 0
    elif [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_usage
        exit 0
    else
        # check if the first arg is a valid semver... if so, use it.
        validate_version $1
        if [ $? == 0 ]; then
            NEW_VERSION=$1
            main
        else
            show_error "no valid arguments supplied."
            show_usage
            exit 1
        fi
    fi
fi
