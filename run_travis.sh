#!/usr/bin/env bash

# Exit on error
set -e
# Echo each command
set -x

pip install jinja2
python render.py
cd ..
set +x
git clone "https://${GH_TOKEN}@github.com/iwrhci/iwrhci.github.io.git" iwrhci.github.io -q
set -x
cd iwrhci.github.io
git rm -fr *
mv ../site_source/build/* .
git add .
# We assume here that a failure in commit means that there's nothing
# to commit.
git commit -m "Update website, commit ${TRAVIS_COMMIT} [skip ci]." || exit 0
PUSH_COUNTER=0
until git push -q
do
    git pull -q
    PUSH_COUNTER=$((PUSH_COUNTER + 1))
    if [ "$PUSH_COUNTER" -gt 3 ]; then
        echo "Push failed, aborting."
        exit 1
    fi
done
