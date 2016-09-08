#!/usr/bin/env bash

# Exit on error
set -e
# Echo each command
set -x

# Install jinja2.
pip install jinja2

# Render the website.
python render.py

# Setup git infor.
git config --global push.default simple
git config --global user.name "Travis CI"
git config --global user.email "bluescarni@gmail.com"

# Now we will clone the website's repo, update it and push the new version.
cd ..
# Don't echo commands on the git clone, in order to avoid printing out sensitive info.
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
git push -q
