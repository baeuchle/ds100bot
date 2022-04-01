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

- So sieht der Bot diesen Tweet, aber wahrscheinlich nicht Antworten
  darauf:

> \#DS100 \#FF


- So sieht der Bot einen Tweet, und wahrscheinlich auch Antworten
  darauf:

> @\_ds\_100 \#FF

Warum antwortet mir der Bot nicht, obwohl er mir folgt?
-------------------------------------------------------

- Vielleicht ist er grade kaputt, der Rechner, auf dem er läuft
  überlastet oder was anderes läuft schief. Meistens aber:
- Wenn dir der Bot folgt, einen Tweet von dir mit richtigem Hashtag
  (sagen wir, #FF) aber nicht beantwortet, liegt es meistens daran, dass
  dieser Tweet von dir eine Antwort auf einen anderen Tweet ist. Einen
  Antwort-Thread „sieht“ der Bot nur dann, wenn er allen beteiligten
  Personen im Thread folgt (oder wenn er selbst beteiligt ist). Das
  liegt daran, wie Twitter die Timeline (für jede Benutzerin)
  zusammenstellt.  Wird ein [Magic Hashtag](/finde-listen.html)
  verwendet oder der Bot im Tweet (oder im Thread) erwähnt, sollte er
  Tweets auch mitten in Threads sehen.

Warum antwortet der Bot mir, obwohl ich das nicht will?
-------------------------------------------------------

- Der Bot antwortet Benutzerinnen, denen er folgt, automatisch, aber er
  folgt nicht automatisch. Siehe unten.
- Bei Tweets von nicht-gefolgten Benutzerinnen reagiert er auf
  Erwähnungen und seine [Magic Hashtags](/finde-listen.html) – aber nur
  dann, wenn auch eine erweiterbare Abkürzung im Tweet steckt. Wenn das
  nicht erwünscht ist, ist der Bot nicht beleidigt, wenn er geblockt
  wird. Da der Bot keine personalisierten Daten speichert, kann man ihm
  nicht anders sagen, dass man von ihm ignoriert werden will. Wem es
  egal ist, ob der Bot antwortet oder nicht, aber selbst die Antworten
  des Bots einfach nicht sehen will, kann den Bot auf Stumm schalten.
- Soll der Bot nur auf einzelne Tweets nicht antworten (aber das muss
  man vorher wissen), kann dieser Tweet mit #NOBOT markiert werden.
- Der Bot antwortet auch, wenn jemand anders einen Tweet beantwortet und
  in dieser Antwort den Bot markiert oder einen der Magic Hashtags
  benutzt. Das kann für die Verfasserin des originalen Tweets verwirrend
  sein.

Warum ist Groß-/Kleinschreibung so wichtig?
-------------------------------------------

Ein Grundprinzip bei der Entwicklung des Bots ist „Don’t Spam”. Dazu
zählt, dass es möglichst wenige „Kollateralfunde“ geben sollte – Dinge,
die gar nicht beantwortet werden sollten. Je genauer ein bestimmtes
Kürzel angegeben werden muss, desto kleiner die Wahrscheinlichkeit, dass
es gar nicht gemeint war.
