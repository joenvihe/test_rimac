#!/bin/bash

# Building packages and uploading them to a Gemfury repository

GEMFURY_URL=$GEMFURY_PUSH_URL

set -e

DIRS="$@"
BASE_DIR=$(pwd)
SETUP="setup.py"

warn() {
    echo "$@" 1>&2
}

die() {
    warn "$@"
    exit 1
}

build() {
    DIR="${1/%\//}"
    echo "Checking directory $DIR"
    cd "$BASE_DIR/$DIR"
    [ ! -e $SETUP ] && warn "No $SETUP file, skipping" && return
    PACKAGE_NAME=$(python $SETUP --fullname)
    echo "Package $PACKAGE_NAME"
    python "$SETUP" sdist bdist_wheel || die "Building package $PACKAGE_NAME failed"
    for X in $(ls dist)
    do
        # curl -F package=@"dist/$X" "$GEMFURY_URL" || die "Uploading package $PACKAGE_NAME failed on file dist/$X"
        echo "[pypi]
        username = __token__
        password = pypi-AgEIcHlwaS5vcmcCJGUyOWEyNWZlLWYwNzQtNGYxYy1iMTQ5LWUzMDA4N2I3Mjg4MgACKlszLCI1ZjUyOWZlNS01NDA4LTQ2OWEtOTUxNy1kYWFkODJmZWY0ODciXQAABiDZ0EJJbDo7m4N9PwSeruxfW3GKIHaQ8iBppSiHZHNuRw" > ~/.pypirc
        twine upload -r pypi dist/* --verbose
    done
}

if [ -n "$DIRS" ]; then
    for dir in $DIRS; do
        build $dir
    done
else
    ls -d */ | while read dir; do
        build $dir
    done
fi