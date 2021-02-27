<description><titel>Titel</titel>
<metadata>metametameta</metatada>
<card src="card.png"/>
</description>


Aufbau der Antworten des Bots
=============================

Findet der Bot in einem Tweet erweiterbare Abkürzungen, so antwortet er
auf diesen Tweet mit diesen Erweiterungen. Hierbei wird eine Zeile pro
Abkürzung geschrieben:

    FF: Frankfurt (Main) Hbf
    1733: Hannover --Kassel-- - Würzburg

Ist die Quelle für die Abkürzung nicht DS100 oder BOT, so wird die
Quelle vorangestellt:

    FFM#HB: Frankfurt Hauptbahnhof
    FFM$A3: Anschlussstrecke A3: Abzweig Nordwest - Oberursel Hohemark

Mehrere Kürzel werden in der Reihenfolge beantwortet, in der sie
auftauchen; mehrfach wiederholte gleiche Kürzel werden nur beim ersten
Mal beantwortet.

Ist die Antwort zu lange für einen Tweet, antwortet der Bot mit dem
nächsten Teil seiner Antwort auf den vorherigen Teil, sodass ein
Twitter-Thread seiner Antworten entsteht.
