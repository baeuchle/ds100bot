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

Namensgebung der Magic Hashtags
===============================

Magic Hashtags beginnen mit einem Unterstrich \_, um von anderen Tags
unterschieden werden zu können.

Ausnahmen dafür sind \#DS100 und \#DB640, die eindeutig genug die
jeweiligen Dokumente bezeichnen, aus denen die (Haupt-)Listen hinter
diesen Quellen stammen.

Bei nationalen Listen besteht der Magic Hashtag dann aus dem Unterstrich
und dem 2-Buchstaben-Code für das Land (vgl. Internet-Domains), also
\_DE, \_AT, \_FR, \_UK etc.

Bei lokalen Listen (gegenwärtig Frankfurt, Hamburg, Wien) wird ein
möglichst sinnvolles Kürzel für die Stadt gewählt: \_FFM, \_HH, \_W.

Beispiel für die Benutzung von Magic Hashtags
=============================================

> ### Tweet 1
> Variante 1: Quelle direkt im Suchbegriff: \#FFM:HWC<br/>
> Variante 2: Magic Hashtag benutzen, dann gilt die dazugehörige
> Quelle für alle Suchbegriffe ohne explizite Quelle nach Variante 1:
> \#OSL \#\_NO \#BRG<br/>
> Variante 2b: Der Magic Hashtag aus 2 gilt bis zum nächsten: \#TND
> \#\_AT \#Lz
>
>> #### Antwort
>> FFM#HWC: Hauptwache (C-Ebene)<br/>
>> NO#OSL: Oslo S<br/>
>> NO#BRG: Bergen<br/>
>> NO#TND: Trondheim S<br/>
>> AT#Lz: Linz Hbf (in Lz)<br/>

und
> ### Tweet 2
> Lemma: Ohne Magic Hashtag ist so, als wäre DS100 der MHT; der erste
> MHT gilt vom Tweetbeginn an (siehe \#OSL \#\_NO im Beispiel-Tweet 1
> und hier).
>
>> #### Antwort
>> NO#OSL: Oslo S
