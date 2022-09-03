<p id="meta">
<title>DS-100: Finden der Listen</title>
<desc>Wie wählt der Bot aus, welche Abkürzungsliste er benutzt?</desc>
</p>

Festlegen der verwendeten Abkürzungslisten
==========================================

Standardmäßig werden gefundene Kürzel mithilfe der
[DS100-](/dumps/orte_de.html)/[STREDAX-](/dumps/strecken_de.html)Listen erweitert.
Für jede Abkürzung kann eine Quelle explizit angefordert werden (siehe
[die Regeln für Abkürzungen](/finde-lang.html)); man kann aber auch die
„Standard-Liste“ für den Tweet verändern, in dem man einen Magic Hashtag
oder ein Magic Emoji benutzt. __Durch Einstellungen im Benutzerprofil
können Benutzende auch den standardmäßig benutzten Magic Hashtag
beeinflussen__, siehe unten. Magic Emojis funktionieren dabei komplett
gleichberechtigt wie Magic Hashtags<span class="only-twitter">, nur
werden sie nicht zur Suche nach Tweets benutzt</span>. Im Detail:

- __Kein Magic Hashtag vorhanden__ bedeutet, dass alles beim alten
  bleibt, siehe oben.
- __Ist genau ein Magic Hashtag vorhanden__, so wird die dazugehörige
  Quelle für Abkürzungssuchen benutzt. Die Zuordnung Hashtag ↔ Quelle
  steht bei der [Übersicht der Daten](/copyright.html).
- __Sind mehrere Magic Hashtags vorhanden__, so gilt jeder davon bis zum
  nächsten; der erste gilt schon ab Anfang.
- __Alternativtexte zu Bildern__ werden so behandelt, als führten sie
  den Tweet fort. Magic Hashtags im Alt-Text werden bei der Auswahl der
  Quelle beachtet. <span class="only-twitter">Allerdings werden Tweets
  nicht auf Grund von Magic Hashtags im Alt-Text gefunden.</span> <span
  class="only-mastodon">__Spoilertexte__ werden so behandelt, als
  stünden sie dem Text voran; die Quellenauswahlregeln werden hier
  ebenfalls angewendet.</span>
- __Die Quelle [BOT](/dumps/gimmick.html) wird immer beachtet.__

Namensgebung der Magic Hashtags
-------------------------------

Magic Hashtags beginnen mit einem Unterstrich \_, um von anderen Tags
unterschieden werden zu können.

Ausnahmen dafür sind \#DS100 und \#DB640, die eindeutig genug die
jeweiligen Dokumente bezeichnen, aus denen die (Haupt-)Listen hinter
diesen Quellen stammen.

Bei nationalen Listen besteht der Magic Hashtag dann aus dem Unterstrich
und dem 2-Buchstaben-Code für das Land (vgl. Internet-Domains), also
\_DE, \_AT, \_FR, \_UK etc.

Bei lokalen Listen wird ein möglichst sinnvolles Kürzel für die Stadt
gewählt: \_FFM, \_HH, \_W.

Beispiel für die Benutzung von Magic Hashtags
---------------------------------------------

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

Magic Emojis
------------

Anstelle von Magic Hashtags können auch Magic Emojis genutzt werden, um
zwischen den Quellen zu wechseln. Diese sind meistens die jeweiligen
Landesflaggen, also etwa 🇩🇪 oder 🇳🇴. <span
class="only-twitter">Tweets werden jedoch nicht anhand eines Magic
Emojis gefunden!</span>

Magic Hashtags und Magic Emojis können auch gemischt werden.

Default Magic Hashtag aus dem Profil
------------------------------------

Ein Nutzer\*innenbezogener Magic Hashtag kann aus dem Profil gelesen
werden. Dabei wird im dem Profiltext ein Text nach der Form "mht:
\#DS100" gesucht, also das Wort mht, gefolgt von einem Doppelpunkt,
Leerzeichen und dann den gewünschten Hashtag inklusive des '#'. <span
class="only-mastodon">In den „Tabellenfeldern“, die Mastodon für
strukturierte Informationen bereitstellt, werden nacheinander die
Schlüssel „magic hashtag“, „magichashtag“ und „mht“ (ohne Beachtung der
Groß-/Kleinschreibung) gesucht; der Wert im ersten darunter gefundenen
wird genutzt. Erst wenn hier nichts gefunden wird, wird der Profiltext
durchsucht.</span> Wird kein Profil-MHT gefunden, wird weiterhin \#DS100
verwendet.
