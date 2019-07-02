Bedienung des Bots
==================

Der Bot reagiert auf alle Tweets, die \#DS100 enthalten oder den Bot
explizit erwähnen, also @\_ds\_100 enthalten. Auf welchen Input er wie
reagiert, ist auf der Seite [Beispiele](beispiele.html) zu sehen.

Folgen
------

Wem der Bot folgt, dessen Tweets werden automatisch nach
großgeschriebenen Hashtags (#FF) durchsucht und diese beantwortet. Um
den Bot dazu zu bringen, zu folgen, bitte eine Mention an den Bot
schicken mit dem Hashtag #folgenbitte:

<blockquote class="tweet_nofollow">
@_ds_100 #folgenbitte
</blockquote>

Wenn das zu nervig wird, kann der Bot folgendermaßen angewiesen werden,
wieder zu entfolgen:

<blockquote class="tweet_follower">
@_ds_100 #entfolgen
</blockquote>

Eine zu kurze Abfolge von #folgenbitte und #entfolgen kann eventuell
übersehen oder in der falschen Reihenfolge abgearbeitet werden. Der Bot
läuft im Normalfall alle zwei Minuten; nach dem nächsten Lauf kann ein
neuer Befehl abgesetzt werden.

Output
-----

Wenn der Bot ein bekanntes Kürzel in einem Tweet findet, so antwortet er
mit dem Kürzel und dem langen Namen; wenn mehr als ein Kürzel gefunden
wird, wird ein Kürzel pro Zeile beschrieben. Wird etwas gefunden, das so
aussieht wie ein Kürzel, dieses aber nicht in der Datenbank gefunden,
dann antwortet der Bot nicht. (Es gibt also keine Fehlermeldung.)

Mehrere gefundene Abkürzungen werden in der Reihenfolge der Erwähnung im
Tweet erweitert; eine Erweiterung wird dabei nicht wiederholt. Wenn
nicht alle Erweiterungen in einen Tweet passen, werden mehrere Tweets
gesendet, die aufeinander antworten. Innerhalb einer solchen Gruppe von
Tweets werden Erweiterungen auch nicht wiederholt.
