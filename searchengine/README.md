ABOUT
----------------------
This contains two python files: **indexer.py** is used to create an inverted index of a large collection of ICS web pages, and **retrieval.py** is the search engine that uses the inverted index to return the most relevant URLs.



EXECUTION
----------------------
To index the ICS web page files, run the indexer.py command in the same directory as the ICS files.
```python3 indexer.py```

To execute the search engine, run the retrieval.py command in the same directory as the outputted files from the indexer.py command.
```python3 retrieval.py```


### USING THE SEARCH ENGINE:

After starting the retrieval.py program, the user will be prompted with:

search>>>

The search engine will print out the top 10 most relevant links in order, along with the total time taken to retrieve those links.

In order to exit the program, type "exit" into the search engine. The user will then be asked if they want to exit the program. If the user does not want to exit, the search engine will assume the user wanted to search the word "exit" and will run like normal instead.


FILES
----------------------
After running the indexer.py command to completion, there will be several txt files created. Do not edit or delete these files as the search engine will not work without them. (The partial index files can be deleted after they are merged.)


*indexindex.txt* : 

This text file contains the index of the inverted index. It contains a dictionary of the byte locations for every letter of the alphabet in the inverted index.

*partial_n_.txt*:

"_n_" can by any number from 1 - n, depend on how large the corpus is. These text files are partial indexed that were offloaded during indexing in order to free up memory. They are automatically merged together at the end of indexing.

*finalindex.txt*:

This is the final inverted index that is created from the indexer and is used by the search engine. It is created by merging the partial index files.

*url_index.txt*:

This text file contains the document id numbers for the URLs. The search engine uses this file to transform the document id into a useable URL.



