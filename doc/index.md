<p id="meta">
<title>DS100-Bot Startseite</title>
<desc>Erklärungen und Dokumentation zum Eisenbahnabkürzungsbot für
Twitter und Mastodon</desc>
</p>

DS100/Ril100-Bot
================

Diese Seite beschreibt den Eisenbahnabkürzungsbot für
[Twitter (@\_ds\_100)](https://twitter.com/_ds_100) und Mastodon (<a rel="me"
href="https://botsin.space/@ril100">@ril100@botsin.space</a>, <a
rel="me" href="https://bahn.social/@ril100">@ril100@bahn.social</a> und
<a rel="me" href="https://zug.network/@ril100">@ril100@zug.network</a>).

Zweck des Bots
--------------

Der Bot soll helfen, Betriebsstellen Deutschen Bahn nach Ril 100
(Betriebsstellenverzeichnis, ehemals DS 100) abzukürzen und trotzdem
sicherzustellen, dass auch Dritte den Inhalt des Tweets verstehen
können.

Der Bot entspringt aus einem privaten Wochenendprojekt und wird _pro
bono_ betrieben; es stehen keine wirtschaftlichen Interessen und keine
Umsatz- oder Gewinnabsicht hinter Erstellung und / oder Betreiben des Bots.

Twitter vs. Mastodon
--------------------

Dieser Bot wurde ursprünglich für Twitter geschrieben und später so erweitert,
dass er auch bei Mastodon eingesetzt werden kann. Aus diesen historischen
Gründen benutzt die Dokumentation das _generische Twittertum_ und bezeichnet
alles als 'Tweets', auch die 'Toots'.

<span class="only-twitter">Dinge, die nur in Twitter relevant sind,
sehen so aus</span>

<span class="only-mastodon">Dinge, die nur in Mastodon relevant sind,
sehen so aus</span>

Instanz-spezifische Mastodon-Accounts
=====================================

<span class="only-mastodon">Die Accounts <a
rel="me" href="https://bahn.social/@ril100">@ril100@bahn.social</a> und
<a rel="me" href="https://zug.network/@ril100">@ril100@zug.network</a>
beantworten Tweets in der lokalen Timeline der jeweiligen Bahn-zentrierten Mastodon-Instanzen.</span>

Kurze Funktionsübersicht: Vier Schritte
---------------------------------------

Der Bot funktioniert in vier Schritten:

1. [Suche nach Tweets](/finde-tweets.html), die eventuell beantwortet
   werden könnten
2. [Herausfinden](/finde-listen.html), welche
   [Abkürzungslisten](/copyright.html) benutzt werden sollen
3. Suche nach [Abkürzungen](/finde-lang.html) in <span
   class="only-mastodon">Spoilertext,</span> Tweet-Text und
   Bild-Alternativtexten
4. [Antwort auf die Tweets](/aufbau-antworten.html) erstellen, in dem
   die Abkürzungen ausgeschrieben werden.

Mit dem Bot kann auch [interagiert](/interaktion.html) werden.
