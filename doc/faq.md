<p id="meta">
<title>DS-100: FAQ</title>
<desc>Sammlung von häufig gestellten Fragen</desc>
</p>

Häufig gestellte Fragen
=======================

(oder was ich dafür halte)

Siehe auch die [FAQ-Abkürzungsliste des Bots](/dumps/faq.html).

Mach doch mal ein einfaches Beispiel!
-------------------------------------

- So sieht der Bot einen Status, und wahrscheinlich auch Antworten
  darauf:

> @ril100@zug.network \#FF

Warum antwortet mir der Bot nicht, obwohl er mir folgt?
-------------------------------------------------------

- Mastodon braucht manchmal ein bisschen Zeit, um Toots an die richtige
  Stelle zu liefern. Das ist systemimmanent und kann nicht verbessert
  werden.
- Vielleicht ist er grade kaputt, der Rechner, auf dem er läuft
  überlastet oder was anderes läuft schief.

Warum antwortet der Bot mir, obwohl ich das nicht will?
-------------------------------------------------------

- Der Bot antwortet Benutzerinnen, denen er folgt, automatisch, aber er
  folgt nicht automatisch. Siehe unten.
- Bei Status von nicht-gefolgten Benutzerinnen reagiert er auf
  Erwähnungen und seine [Magic Hashtags](/finde-listen.html) – aber nur
  dann, wenn auch eine erweiterbare Abkürzung im Toot steckt. Wenn das
  nicht erwünscht ist, ist der Bot nicht beleidigt, wenn er geblockt
  wird. Da der Bot keine personalisierten Daten speichert, kann man ihm
  nicht anders sagen, dass man von ihm ignoriert werden will. Wem es
  egal ist, ob der Bot antwortet oder nicht, aber selbst die Antworten
  des Bots einfach nicht sehen will, kann den Bot auf Stumm schalten.
- Soll der Bot nur auf einzelne Toots nicht antworten (aber das muss
  man vorher wissen), kann dieser Toot mit #NOBOT markiert werden.
- Der Bot antwortet auch, wenn jemand anders einen Toot beantwortet und
  in dieser Antwort den Bot markiert oder einen der Magic Hashtags
  benutzt. Das kann für die Verfasserin des originalen Toots verwirrend
  sein.

Warum ist Groß-/Kleinschreibung so wichtig?
-------------------------------------------

Ein Grundprinzip bei der Entwicklung des Bots ist „Don’t Spam”. Dazu
zählt, dass es möglichst wenige „Kollateralfunde“ geben sollte – Dinge,
die gar nicht beantwortet werden sollten. Je genauer ein bestimmtes
Kürzel angegeben werden muss, desto kleiner die Wahrscheinlichkeit, dass
es gar nicht gemeint war.
