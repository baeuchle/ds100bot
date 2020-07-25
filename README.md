DS-100-Bot
==========

Dies ist ein Twitter-Bot zur Expansion von Bahnabkürzungen.

Vorbereitungen
--------------

Die Datei config/schema.sql enthält die Struktur der Datenbank. Die
Datenbank ``info.db`` kann damit erstelt werden:

```
    cat schema.sql | sqlite3 info.db
```

Um den Twitter-Bot nutzen zu können, muss die geneigte Benutzerin
[Twitter-Developress](https://developer.twitter.com/) werden. Dann
erhält sie auch Authentifizierungsdaten.

Die Datei credentials.py.dist muss in credentials.py umbenannt werden
und die Twitter-Authentifizierungsdaten eingetragen werden.

Daten werden eingelesen und die Dokumentation erzeugt mit

```
    tools/setup
```

Vorbedinungen
-------------

Der Bot ist in python3 geschrieben und benutzt SQLite3 als Datenbank.
Alle verwendeten Python-Packages sind als Ubuntu-Packages verfügbar und
wahrscheinlich auch mit pip installierbar.

Ausführen
---------

Es gibt vier Hauptprogramme. Für Informationen zur Bedienung dieser
Programme kann die Option ``--help`` verwendet werden.

* ``ds100bot``: Der eigentliche Bot. Kann beliebig oft im Abstand weniger
  Minuten ausgeführt werden.
* ``statistics``: Gibt Statistiken über die Benutzung des Bots aus. Sollte
  z.B. einmal monatlich ausgeführt werden.
* ``test``: Führt Testfälle aus und überprüft, ob die Testtweets korrekt
  beantwortet werden.
* ``get_tweet``: Lädt echte Tweets herunter. Damit können problematische
  Tweets genauer analysiert werden.

LIZENZ
======

Der Quellcode dieses Bots ist unter der Apache Lizenz, Version 2.0,
lizensiert. Siehe Datei LICENSE.

Die Datei ``config/api_weights.json`` ist von
https://github.com/twitter/twitter-text/tree/master/config/v3.json
genommen und von Twitter, Inc. ebenfalls unter Apache Lizenz, Version
2.0, lizensiert.

Die Datentabellen in ``sources`` stehen unter verschiedenen Lizenzen.
Diese sind in ``data`` aufgeführt.
