Festlegen der verwendeten Abkürzungslisten
==========================================

Standardmäßig werden gefundene Kürzel mithilfe der
[DS100-](/dumps/orte_de.html)/[STREDAX-](/dumps/strecken_de.html)Listen erweitert.
Für jede Abkürzung kann eine Quelle explizit angefordert werden (siehe
[die Regeln für Abkürzungen](/finde-lang.html)); man kann aber auch die
„Standard-Liste“ für den Tweet verändern, in dem man einen Magic Hashtag
benutzt:

- __Kein Magic Hashtag vorhanden__ bedeutet, dass alles beim alten
  bleibt, siehe oben.
- __Ist genau ein Magic Hashtag vorhanden__, so wird die dazugehörige
  Quelle für Abkürzungssuchen benutzt. Die Zuordnung Hashtag ↔ Quelle
  steht bei der [Übersicht der Daten](/copyright.html).
- __Sind mehrere Magic Hashtags vorhanden__, so gilt jeder davon bis zum
  nächsten; der erste gilt schon ab Anfang.
- __Alternativtexte zu Bildern__ werden so behandelt, als führten sie
  den Tweet fort. Magic Hashtags im Alt-Text werden bei der Auswahl der
  Quelle beachtet. Allerdings werden Tweets nicht auf Grund von Magic
  Hashtags im Alt-Text gefunden.
- __Die Quelle [BOT](/dumps/gimmick.html) wird immer beachtet.__

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
