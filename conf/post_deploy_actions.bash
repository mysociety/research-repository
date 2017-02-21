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
virtualenv_dir='../virtualenv-repository'
virtualenv_activate="$virtualenv_dir/bin/activate"
if [ ! -f "$virtualenv_activate" ]
then
    virtualenv $virtualenv_args $virtualenv_dir
fi
source $virtualenv_activate

# Upgrade pip to a secure version
pip_version="$(pip --version)"
if [ "$(echo -e 'pip 1.4\n'"$pip_version" | sort -V | head -1)" = "$pip_version" ]; then
    curl -L -s https://bootstrap.pypa.io/get-pip.py | python
fi

pip install --requirement requirements.txt

# make sure that there is no old code (the .py files may have been git deleted)
find . -name '*.pyc' -delete

# get the database up to speed
./manage.py migrate

# gather all the static files in one place
./manage.py collectstatic --noinput

