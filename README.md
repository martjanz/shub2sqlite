Scrapinghub API to SQLite
=========================

This is a simple Python script that downloads data from a Scrapinghub enabled
account to a SQLite database.

By default this script fetch data (in json format) only from finished jobs in 
active projects.
For additional options see parameters section.

### Config (config.py)

* `apikey` Scrapinghub API key
* `database` SQLite database filename

### Parameters

* `-d --deleted` download also deleted jobs