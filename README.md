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
    
	Once in the vagrant, to populate the database with test data (and create an 'admin'/'admin' superuser) - run:
	$ script/populate
	
	Then to run the server:
	
	$ script/server

The website will then be running at http://localhost:8000
