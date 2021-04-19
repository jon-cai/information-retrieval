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
**HOST**       : The host name of the cache server. <br>
**PORT**       : The port number of the cache server. <br>
**SEEDURL**    : Initial URLs placed in the frontier. These are the first URLs that the crawler starts downloading. <br>
**POLITENESS** : How often crawler executes a request. The higher the time delay, the more polite. <br>
**SAVE**       : Where the frontier is saved. If this file is deleted, the crawler will restart at the SEEDURL. <br>
**THREADCOUNT**: How many threads to use. Do not change this as the crawler is not thread safe at the moment.
<br><br>

To execute the spacetime crawler, run the ***launch.py*** program.
