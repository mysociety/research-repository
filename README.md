Research Repository
===========================

[![Installability](http://img.shields.io/badge/installability-gold-ffd700.svg)]()

mySociety and its partners do lots of research. This is a place for us to list that research in a coherent manner for easy finding and citation.

Local development
-----------------

**Danger Will Robinson!** You must make sure that this repository is cloned into a folder called `repository`. We recommend:

    $ git clone https://github.com/mysociety/research-repository.git research-repository/repository

Once cloned create conf/general.yml and conf/httpd.conf from the example files.

In general.yml specify a django secret key and if testing locally, add '127.0.0.1' to the allowed_hosts.
    
This project includes a Vagrantfile to make local development easy.
Simply run:

    $ vagrant up

In Windows run the command prompt as administrator. 
    
To get a fully configured vagrant development environment. The code is
installed into `/vagrant/repository` inside the VM, and you can run
the Django dev server with:

    $ source ../virtualenv-repository/bin/activate
    $ python manage.py runserver 0.0.0.0:8000

The website will then be running at http://localhost:8000
