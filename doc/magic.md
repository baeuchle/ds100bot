Magic Hashtags
==============

Ein Magic Hashtag ist einer, der eine bestimmte Quelle für die
Abkürzungsexpansion auswählt. Vor Version 5 gab es nur den Magic Hashtag
‚__\#DS100__‘.

__Wer nur die DS100-Abkürzungen verwendet, für die ändert sich nichts.__

Die Motivation ist aber, in einem Tweet mit vielen Abkürzungen aus einer
_anderen_ Liste eben diese Liste als Standard auszuwählen, eben durch
Inkludieren des jeweiligen Magic Hashtag.

Der Bot durchsucht Twitter nach allen aktiven Magic Hashtags, wie in
[Finden von Tweets](finderegeln.html) beschrieben.

Verhalten
---------

__Kein Magic Hashtag vorhanden__ bedeutet, dass alles beim alten bleibt
und die DS100-/STREDAX-Listen benutzt werden, um Abkürzungen zu
expandieren. Andere Listen können wie gehabt mit Quelle angegeben
werden, etwa ‚\#FFM:HB‘.

__Ist genau ein Magic Hashtag vorhanden__, so wird die dazugehörige
Quelle für Abkürzungssuchen benutzt. Die Zuordnung Hashtag ↔ Quelle
steht bei der [Übersicht der Daten](copyright.html).

__Sind mehrere Magic Hashtags vorhanden__, so gilt jeder davon bis zum
nächsten; der erste gilt schon ab Anfang.
