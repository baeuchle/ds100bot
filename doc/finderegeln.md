Finden von Tweets
=================

Der Bot findet Tweets auf vier verschiedenen Wegen:

- Markierung durch [Magic Hashtag](magic.html)
- Explizites Erwähnen des Bots durch
  [@\_ds\_100](https://twitter.com/_ds_100) im Text
- Implizites Erwähnen des Bots durch Antworten auf einen Tweet des Bots
- Seine Timeline, das heißt, alle Tweets von Benutzer\*innen, denen der
  Bot folgt, außer Antworten auf nicht-gefolgte Benutzer\*innen.

Der Bot reagiert in den vier Fällen jeweils unterschiedlich:

<table>
 <thead>
  <tr>
   <th></th>
   <th>#FF</th>
   <th>FF</th>
   <th>Kommentiert retweetete Tweets</th>
   <th>Beantwortete Tweets</th>
   <th>#folgenbitte, #entfolgen</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <th>Tweets mit Magic Hashtag</th>
   <td>Ja</td>
   <td>Ja, wenn kein Treffer bei Hashtags</td>
   <td>Wie Timeline</td>
   <td>Wie Timeline</td>
   <td>Ignoriert</td>
  </tr>
  <tr>
   <th>Explizite Erwähnung</th>
   <td>Ja</td>
   <td>Ja, wenn kein Treffer bei Hashtags</td>
   <td>Wie Magic Hashtag (keine Rekursion)</td>
   <td>Wie Magic Hashtag (keine Rekursion)</td>
   <td>Erkannt</td>
  </tr>
  <tr>
   <th>Implizite Erwähnung</th>
   <td>Ja</td>
   <td>Nein</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
  </tr>
  <tr>
   <th>Timeline</th>
   <td>Ja</td>
   <td>Nein</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
  </tr>
  <tr>
   <th>Retweets (ohne Kommentar)</th>
   <td>Nein</td>
   <td>Nein</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
  </tr>
  <tr>
   <th>Tweets vom Bot selbst</th>
   <td>Nein</td>
   <td>Nein</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
  </tr>
 </tbody>
</table>

Interaktion
===========

Neben dem markieren von Tweets, sodass der Bot sie findet, kann der Bot
auch dazu aufgefordert werden, einer Benutzerin zu folgen, sodass deren
Tweets in des Bots Timeline auftauchen und automatisch beantwortet
werden können (siehe oben). Dafür muss ein Tweet mit \#folgenbitte an
den Bot geschickt werden (siehe ebenfalls oben).

Wenn die Nutzerin irgendwann genug davon hat, dass der Bot sich ständig
ungefragt meldet, reicht ein weiterer Tweet mit \#entfolgen, damit der
Bot nicht mehr folgt und wieder nur auf Erwähnung reagiert.

Finden von Kürzeln
==================

Ein findbares Kürzel besteht aus

- einem ‚\#‘ oder ‚$‘ (fließt in die Auswahl der Quelle ein: \# für
  Orte, $ für Strecken)
- einem Bezeichner für die Quelle: Wenn nicht vorhanden, wird entweder
  die dem aktuellen [Magic Hashtag](magic.html) entsprechende Quelle
  oder ‚BOT:‘ benutzt.
- Groß- und Kleinschreibung der jeweiligen Quelle müssen beachtet
  werden. Viele Quellen benutzen ausschließlich Großbuchstaben (und
  Ziffern), einzelne nutzen auch Kleinbuchstaben.
- dem Kürzel selbst. Hier werden aus den Originalquellen
  aufeinanderfolgende Leerzeichen durch einen Unterstrich ersetzt (aus
  ‚`AA  G`‘ wird also ‚`AA_G`‘).
- Leerzeichen (bzw. Unterstriche) sind wichtig; es gibt eine <a
  href="/leerzeichen_ds100.html">Liste mit den Betriebsstellen</a>,
  bei denen es einen Unterschied macht,
- Führende Unterstriche werden beibehalten. (Beispiel #FFM:\_HB)
- Einträge in der [Schwarzliste](blacklist.html) können durch benutzen
  der Quelle angezeigt werden.

Beispiele
---------

- \#FKW, \#DS:FKW
- $1234, $DS:1234
- $KRM, $VDE8¹
- $FFM:A, $FFM:DⅣ, $FFM:Dⅱ (bei Unicode-römischen Ziffern sind
  Groß-/Kleinschreibung egal, aber $VGF:Dii geht nicht!)
- \#FFM:BM

