# PhenVar
PhenVar is designed to take one or more rsids and generate a list of PubMed IDs to query and generate novel associations between publications. It utilizes a local sqlite database in a configurable location to keep a local copy of relevant srids, pmids, and the abstract blobs for the pmids, which enables faster fetching of results.
The website portion of phenvar is powered by Flask.
## Installation Notes
Dependencies:
* Python 3.3+
* uwsgi + Nginx (for web)
* Sqlite 3
To install, clone the repository (ideally in /opt) and edit the settings.py file, replacing EMAIL with the email address you intend to use when querying NCBI.
To initialize and load the database and json cache, run:
`./manage_db initialize`
`./manage_db load`
`./manage_db build_json`
Note that the above will take quite some time (approximately ~1 day) due to the limitations of pubmed's API.

## Application Structure

### settings.py
settings.py is a file containing various configuration options used by the application.
* EMAIL is the email address to use when querying NCBI, ideally this should be your email address
* WORDCLOUD_STORAGE is the path you wish to store your wordclouds in. The default is static/wc, which is recommended.
* MAPPING_FILE is a json file that is used to store nouns associated with preprocessed pmid's
* FILTER_LIST is a list of lowercase words to ignore when generating wordclouds

### ncbiutils.py
#### PubmedArticle
This object stores information about an article parsed from a PubmedArticle xml tree. It has the properties:
* pmid
* abstract
* authors
* date_created
* date_revised
And the method rsids(), which queries pubmed for a list of rsids cited in the article.
#### Author
Similar to PubmedArticle, this class is initiated with an Author xml tree from a pubmed article, and has the properties:
* last_name
* first_name
* initials
Or, if it is a collective author:
* collectiv_name
Both types of author have the *affiliations* property, which is a list of author affiliations parsed from the xml.
#### RSID
The RSID class takes an rsid number as input, and optionally gathers data about that RSID from SNP. It also has a method to return all associated PubmedArticles from pubmed.
#### get_pubmed_articles
Returns a full list of pubmed articles via the pubmed_snp_cited search term. Alternatively, only returns articles revised since the since_date variable (a python datetime.date object)
#### get_all_rsids
Returns full list of cited rsids from snp, as RSID objects

### database.py
Contains the database schema definitions, using the Sqlalchemy ORM.
This also contains functions to perform language processing on abstracts in the database in order to create the cached json file, which contains lists of nouns in each article, linked by their pmid.

### visualization.py
Contains methods to create wordclouds from a list of rsids.
