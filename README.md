DS-100-Bot
==========

Dies ist ein Twitter-Bot zur Expansion von Bahnabkürzungen.

Usage
-----

Execute ``ds100bot.py``. See its ``--help``-option for details.

If you're looking for the bots behaviour w/o trying to run it yourself,
visit https://ds100.frankfurtium.de. You may want to learn German first.

Prerequisites
-------------

The bot is written in Python3 and uses the non-standard packages

* tweepy
* re
* sqlite3

(all others are included in a standard Ubuntu distribution).

In order to create the documentation, ``markdown`` is required.

Before starting
---------------

* Create an sqlite database ``info.db`` from ``schema.sql``:
    ```
    cat schema.sql | sqlite3 info.db
    ```
* Import the source data:
    ```
    cat config/sourceflags.sql | sqlite3 info.db
    cat config/sources.sql | sqlite3 info.db
    ```
* Copy ``credentials.py.dist`` to ``credentials.py`` and insert your
  Twitter bot credentials.
* Import data using ``import-data.py`` or
* Create the documentation AND import data in one step using
  ``update-doc.sh``.

LICENSE
=======

The source code of this bot is licensed under Apache License, Version
2.0, see ``LICENSE``.

The file ``config/api_weights.json`` is taken from
https://github.com/twitter/twitter-text/tree/master/config/v3.json and
licensed by Twitter, Inc., also under Apache License, Version 2.0.
