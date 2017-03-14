Research Repository
===========================

[![Installability](http://img.shields.io/badge/installability-gold-ffd700.svg)]()

mySociety and its partners do lots of research. This is a place for us to list that research in a coherent manner for easy finding and citation.

Local development
-----------------

This project includes a Vagrantfile to make local development easy.
Simply run:

    $ vagrant up

To get a fully configured vagrant development environment. The code is
installed into `/vagrant/repository` inside the VM, and you can run
the Django dev server with:

    $ source virtualenv-repository/bin/activate
    $ python manage.py runserver 0.0.0.0:8000

The website will then be running at http://localhost:8000
