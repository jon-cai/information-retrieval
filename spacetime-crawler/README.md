# README


## About

This is a simple implementation of a spacetime web crawler
that accesses a cache server to receive requests.
<br><br>
The scraper uses a similarity hash to ignore duplicate pages 
and infinite traps. All collected data is offloaded onto 
pickle files.

## Execution

Before running the crawler, adjust the parameters in config.ini. <br><br>
**USERAGENT**  : Identifier for your crawler. (not necessary) <br>
**SEEDURL**    : Initial URLs placed in the frontier. <br>
**POLITENESS** : How often crawler executes a request. (in seconds) <br>
**SAVE**       : Where the frontier is saved. <br>
**THREADCOUNT**: How many threads to use.
<br><br>

To execute the spacetime crawler, run the launch.py program.
