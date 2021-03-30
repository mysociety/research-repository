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

curl -L -s https://bootstrap.pypa.io/pip/2.7/get-pip.py | python

pip install --upgrade setuptools
pip install --requirement requirements.txt

# make sure that there is no old code (the .py files may have been git deleted)
find . -name '*.pyc' -delete

# get the database up to speed
./manage.py migrate

# gather all the static files in one place
./manage.py collectstatic --noinput

# researchsites. This feels like a bit of a hack.
researchsites_dir='../sites'
if [ ! -d "$researchsites_dir" ]; then
    mkdir $researchsites_dir
    cd $researchsites_dir
    git clone --no-checkout ssh://git.mysociety.org/data/git/private/researchsites.git . && git checkout master
else
    cd $researchsites_dir
    /data/mysociety/bin/git-safe-to-checkout . master && git pull
fi

#create zip archive if absent
zip_archive_dir='../zip_uploads'
if [ ! -d "$zip_archive_dir" ]; then
    mkdir $zip_archive_dir
fi
