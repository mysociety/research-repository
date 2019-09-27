# Research Repository


[![Installability](http://img.shields.io/badge/installability-gold-ffd700.svg)]()

mySociety and its partners do lots of research. This is a place for us to list that research in a coherent manner for easy finding and citation.

## Local development


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


## Accessing admin

Admin password is available on the wiki - can then create a user account on the django backend

https://research.mysociety.org/admin/ 

To create a token to use the remote zip upload, use `script/token <username>`

## Models and concepts

### ResearchItem

The core of the site is the ResearchItem - this holds all the information about an individual piece of research.

It has a ‘published’ boolean that is required to be ticked before appearing on any public listing  - but the page itself can be accessed through its slug at any time.

Featured items appear on the homepage and on the research page on the main mysociety site. 

New items need an image for the page (hero) and a thumbnail - the thumbnail can be automatically generated from the hero on the admin page. 

Outputs from stringprint can be uploaded as a zip into ‘archive zip’ - this will create required research outputs to link and the link to the TOC.

Less self explanatory fields:

- Table of contents url - an external json can be used to create a table of contents (mostly for use in stringprint imports)  - this will then be stored in the table of contents cache. 
- table of Contents cache - this stores the json from above - but can also be used for arbitrary markdown to create tables of contents for other kinds of documents. TOCs will appear below the abstract, but will be included in the abstract if the code `[TOC]` is used. 

ResearchItems have `Outputs`, `Tags` and `Authors`

### Output

Outputs control the links and files associated with a ResearchItem
They can either have a link or a file associated with them and count the number of times they have been accessed.
The Top_order refers to the order of items under the image at the top (left to right). -1 is do not display. The lowest value item is also the link in the image itself is clicked. 
Order - controls the outputs on the righthand bar (generally less important). 

### Tag
Tags are the way ResearchItems and their display are managed on the site. They are many-to-many, but their exact role is modified by their properties. They have a page that shows their associated items at /section/[tagslug]

- Display - unchecking allows hidden categories that are used for internal management but do not appear in sidebar of items (e.g. creating associations for embedding on other pages, or to raise the association of items for the purpose of the related items detector). 
- Top order - if the category should appear as one of the options in the top bar of the ‘research’ page. 
- Is series - adds a ‘part of [tag]’ near the top of a research item, for more tightly connected groups of ResearchItems. 
- Display with years - if unticked, will not separate items by year (looks better if a category only has a few items). 
- Featured - tags can also be featured, this displays on the featured page on the home page and embedded pages like a Researchitem (This is the one place the thumbnail or date is used). 

The default tag (where the research link on the top bar leads - is set in the one ‘Site’ object). 

### Pages App

Content on the rest of the site is also customisable via the admin. 

- The single ‘site’ object controls the title, twitter handle and site description, as well as the default tag for displaying research. 
- Page objects allow for non-research item pages of material. The html is embedded in the admin and has a customisable social image and description. A nav order above 0 will put it in the top bar. 
- Links allow links to external sites to be put in the top bar.

### Embedding in external sites

As explored on wiki page, items can be embedded in other pages - either as iframes or by reformatting the data.

This involves a very basic api for accessing data. For instance:

`/embed/featured/limit:6/format:json`

Creates a json with the 6 most recent featured items. ‘Featured’ can also be any tag slug. These can also be stacked - for instance /blog-posts/community/ shows blog posts that are also in the community tag. 

Excluding ‘format:json’ just displays a webpage, that can be used in an iframe (how the stringprint sites show related items). 

Authors - fairly self-explanatory but have a lot of different options and allow author names to be transformed into links to their site via a customisable link behaviour. Some references in here to an authors page that was never created. 


