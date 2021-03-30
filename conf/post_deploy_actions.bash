#!/bin/bash

# abort on any errors
set -e

# check that we are in the expected directory
cd `dirname $0`/..

# create/update the virtual environment
# NOTE: some packages are difficult to install if they are not site packages,
# for example xapian. If using these you might want to add the
# '--system-site-packages' argument.
virtualenv_args=""
virtualenv_dir='../venv'
virtualenv_activate="$virtualenv_dir/bin/activate"
if [ ! -f "$virtualenv_activate" ]
then
    python3 -m venv $virtualenv_dir  --without-pip
fi
source $virtualenv_activate

# Upgrade pip to a secure version
curl -L -s https://bootstrap.pypa.io/pip/3.5/get-pip.py | python3

pip3 install --requirement requirements.txt

# make sure that there is no old code (the .py files may have been git deleted)
find . -name '*.pyc' -delete

# get the database up to speed
python3 manage.py migrate

# gather all the static files in one place
python3 manage.py collectstatic --noinput

#create zip archive if absent
zip_archive_dir='../zip_uploads'
if [ ! -d "$zip_archive_dir" ]; then
    mkdir $zip_archive_dir
fi
