Magic Hashtags
==============

Ein Magic Hashtag ist einer, der eine bestimmte Quelle für die
Abkürzungsexpansion auswählt. Vor Version 5 gab es nur den Magic Hashtag
‚__\#DS100__‘.

Der Bot durchsucht Twitter nach allen aktiven Magic Hashtags, wie in
[Finden von Tweets](finderegeln.html) beschrieben.

Kein Magic Hashtag vorhanden
----------------------------

Ist in einem Tweet kein Magic Hashtag vorhanden, dann funktioniert der
Bot genau so, als wäre \#DS100 als Magic Hashtag vorhanden.

Genau ein Magic Hashtag vorhanden
---------------------------------

Ist in einem Tweet ein Magic Hashtag vorhanden, so wird die damit
assoziierte Quelle als Standard-Quelle für alle quellenlosen
Suchbegriffe benutzt.

### Beispiel:

Im Tweet:
> Text \#HB Text \#\_FFM \#SB \#DS:FFW
wird der Magic Hashtag __\#\_FFM__ erkannt, daher werden \#HB und \#SB
als \#FFM:HB (Hauptbahnhof) und \#FFM:SB (Südbahnhof) erkannt. \#DS:FFW
bleibt aber der Quelle DS zugeordnet und wird aus dieser als Frankfurt
West übersetzt.

Mehr als ein Magic Hashtag vorhanden
------------------------------------

Bei mehrern Magic Hashtags in einem Tweet ist jeder Magic Hashtag für
alles folgende bis zum nächsten Magic Hashtag gültig. Der erste Magic
Hashtag ist von Beginn an gültig.

### Beispiele:
Tweet 1:
> \#\_FFM \#HB \#DS100 \#FFS \#\_FFM \#OB \#DS100 \#FFM:WEBF \#FFLF
expandiert zu \#FFM:HB (Hauptbahnhof), \#DS:FFS (Frankfurt Süd),
\#FFM:OB (Ostbahnhof), \#FFM:WEBF (Westbahnhof) und \#DS:FFLF (Frankfurt
Flughafen Fernbahnhof).

Tweet 2:
> \#KDWE \#BO \$A \#WBC \#\_FFM \#WBD \$B \#DS100 \#FF \#FKW
expandiert zu \#FFM:KDWE (Konrad-Duden-Weg), \#FFM:BO (Bonames Mitte),
\$FFM:A (A-Strecke), \#FFM:WBC (Willy-Brandt-Platz C-Ebene), \#FFM:WBD
(Willy-Brandt-Platz D-Ebene), \$FFM:B (B-Strecke), \#DS:FF (Frankfurt
Hbf) und \#DS:FKW (Kassel-Wilhelmshöhe).
