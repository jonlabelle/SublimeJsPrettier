#!/usr/bin/env bash

##
# Release tasks bulked into one script (user intervention required)
#
# Usage:
#
# From the 'master' branch... run:
#
#   $ release.sh <semver>
#
# ... which performs the following operations:
#
# - Bumps 'package.json' file to passed <semver> arg (1).
# - Commit and push the change (on master)
# - Create and push <semver> git tag
# - publish the npm package
#
# Example:
#
#   $ release.sh 1.2.1
##

set -e

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

#
# cd to scripts dir, then project root (assuming this script is
# stored at <root>/scripts:
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" && cd ../

VERSION=$1
if [[ ! ${VERSION} =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "$VERSION is not a valid semver (ex: 1.2.1)"
    exit 1
fi

GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$GIT_BRANCH" != "master" ]; then
    echo "$SCRIPT_NAME must be run from the 'master' branch (current branch is: '$GIT_BRANCH')."
    exit 1
fi

if ! git diff-index --quiet HEAD --; then
    echo "git repo is dirty. Commit all changes before using $SCRIPT_NAME."
    exit 1
fi

echo
echo "> Bump package.json version:"
echo
sed -E s/'"version"\: "[0-9]+\.[0-9]+\.[0-9]+"'/'"version"\: "'"$VERSION"'"'/ package.json \
    > /tmp/package.json && \
    mv /tmp/package.json package.json
grep "$VERSION" -C 1 package.json

if [[ ! $(git diff --stat) =~ "2 files changed, 2 insertions(+), 2 deletions(-)" ]]; then
    echo "WARNING! Expected exactly 2 changes in 2 files after replacing version number. Bailing! (check git status and git diff)"
    exit 1
fi

echo
while true; do
    read -r -p "> Ready to build, commit, tag and release v$VERSION? (y/n): " yn
    case ${yn} in
        [Yy]* )   break;;
        [NnQq]* ) exit;;
        * ) echo "Please answer w [Y]es or [N]o.";;
    esac
done

echo
echo "> git commit/push/tag/push --tags"
set -x
git add package.json
git commit -m "Bump to v$VERSION"
git push "$ORIGIN" "$BRANCH"
git tag -a "$VERSION"
git push --tags
set +x

echo
echo "> npm publish"
npm publish
