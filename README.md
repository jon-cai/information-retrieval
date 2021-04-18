# information-retrieval
Project worked on regarding information retrieval.


**ABOUT**
-----------------------------------

Two information retrieval projects that I worked on. 


The spacetime crawler crawls a cached server and stores the information in various pickle files. It uses a similarity hash to 
avoid duplicate web pages.


The search engine project has an indexer that parses thousands of downloaded web page documents (can be modified to be a typical 
web crawler that scrapes information from websites) and indexes it for use with the search engine. The indexer also uses a
similarity hash to ignore duplicates and stores indexes on regular txt files. 

The search engine uses the indexed txt files to return relevant web pages in under 300ms.
