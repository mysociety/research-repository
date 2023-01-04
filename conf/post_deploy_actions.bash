#!/bin/bash

# abort on any errors
set -e

# check that we are in the expected directory
cd "$(dirname $BASH_SOURCE)"/..

source .venv/bin/activate

# get the database up to speed
python manage.py migrate

# repopulate search index
python manage.py rebuild_index