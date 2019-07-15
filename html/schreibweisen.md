Erkannte Schreibweisen
======================

Kürzel, die vom Bot erkannt werden sollen, müssen grundsätzlich einem
der folgenden Formate genügen:
- \#KURZ: Findet die Langform von KURZ aus der DS100.
- $1234: Findet den Verlauf der Strecke 1234 der DB Netz.
- \#kurz: Wie \#KURZ
- \#DS:KURZ: Wie \#KURZ
- \#DS:kurz: Wie \#KURZ
- $DS:1234: Wie $1234
- KURZ: Wird nur gefunden in Tweets mit expliziter Erwähnung oder \#DS100
  (siehe [Finden von Tweets](finderegeln)), und nur dann, wenn kein
  Kürzel mit \# oder $ gefunden wurde. Hier werden nur DS100-Kürzel
  gefunden.

Die Syntax mit "DS:" erlaubt es, Kürzel aus anderen Quellen zu suchen.
Bisher gibt es ein sehr kleines Subset aus den Stadtbahnstrecken in
Frankfurt (bspw. $VGF:A) und den Haltestellenkürzeln der Stadtbahn in
Frankfurt (bspw. \#VGF:BM). Ohne Quellenteil werden nur Abkürzungen aus
der DS100, der Streckenliste oder den Spezialbefehlen des Bots (auch als
\#BOT: abrufbar) gefunden.

Mischungen aus Groß- und Kleinbuchstaben werden niemals als mögliches
Kürzel betrachtet.
