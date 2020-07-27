Datenlisten
===========

Dieses Verzeichnis enthält die Datenlisten, die für den Bot importiert
werden. Diese Datenlisten werden in den Konfigurationen in data/
referenziert.

Die Listen sind im CSV-Format; die erste Zeile enthält die Spaltennamen,
die in der Konfiguration (siehe Verzeichnis data/) den Datenbank-Spalten
zugeordnet werden.

Jeder einzelne Datensatz sollte als Antwort in einen Tweet passen, das
heißt für eine Datenquelle mit Default-Quellenangabe 'XS' gilt für einen
Datensatz mit Abkürzung ABK, dass der Langname 272 Zeichen lang sein
darf, weil ``XS#ABK: `` eben 8 Zeichen lang ist:
``XS#ABK: _HIER_PASSEN_NOCH_272_ZEICHEN_REIN_``.

Vorsicht jedoch: Twitter zählt manche Zeichen doppelt. Das betrifft
allerdings 'nur' sehr ausgefallene Satzzeichen und nicht-europäische
Alphabete.  [Siehe hier für
Details](https://developer.twitter.com/en/docs/basics/counting-characters).
