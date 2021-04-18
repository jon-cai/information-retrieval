# README


## About
--------------
This is a simple implementation of a spacetime web crawler <br>
that accesses a cache server to receive requests.
<br><br>
The scraper uses a similarity hash to ignore duplicate pages <br>
and infinite traps. All collected data is offloaded onto <br>
pickle files.

## Execution
--------------
Before running the crawler, adjust the parameters in config.ini.
USERAGENT : Identifier for your crawler. (not necessary)
SEEDURL : Initial URLs placed in the frontier.
POLITENESS : How often crawler executes a request. (in seconds)
SAVE: Where the frontier is saved.
THREADCOUNT: How many threads to use.
<br><br>

To execute the spacetime crawler, run the launch.py program.
