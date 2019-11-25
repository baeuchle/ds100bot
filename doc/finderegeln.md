Finden von Tweets
=================

Der Bot findet Tweets auf vier verschiedenen Wegen:

- Markierung durch Hashtag
  [\#DS100](https://twitter.com/search?q=%23DS100&f=tweets)
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
   <th>#ff</th>
   <th>FF</th>
   <th>Kommentiert retweetete Tweets</th>
   <th>Beantwortete Tweets</th>
   <th>#folgenbitte, #entfolgen</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <th>Tweets mit #DS100</th>
   <td>Ja</td>
   <td><strong>Nein</strong></td>
   <td>Ja, wenn kein Treffer bei Hashtags</td>
   <td>Wie Timeline</td>
   <td>Wie Timeline</td>
   <td>Ignoriert</td>
  </tr>
  <tr>
   <th>Explizite Erwähnung</th>
   <td>Ja</td>
   <td><strong>Nein</strong></td>
   <td>Ja, wenn kein Treffer bei Hashtags</td>
   <td>Wie #DS100 (keine Rekursion)</td>
   <td>Wie #DS100 (keine Rekursion)</td>
   <td>Erkannt</td>
  </tr>
  <tr>
   <th>Implizite Erwähnung</th>
   <td>Ja</td>
   <td><strong>Nein</strong></td>
   <td>Nein</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
  </tr>
  <tr>
   <th>Timeline</th>
   <td>Ja</td>
   <td><strong>Nein</strong></td>
   <td>Nein</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
   <td>Ignoriert</td>
  </tr>
  <tr>
   <th>Retweets (ohne Kommentar)</th>
   <td>Nein</td>
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
  die Quelle ‚DS:‘ oder ‚BOT:‘ benutzt. Besteht immer aus
  Großbuchstaben.
- dem Kürzel selbst. Hier werden aus den Originalquellen
  aufeinanderfolgende Leerzeichen durch einen Unterstrich ersetzt (aus
  ‚`AA  G`‘ wird also ‚`AA_G`‘). Das Kürzel kann aus
  Großbuchstaben und Zahlen bestehen. Kleinbuchstaben sind nicht (mehr)
  möglich.

Beispiele
---------

- \#FKW, <del>\#fkw,</del> \#DS:FKW<del>, \#DS:fkw</del>
- $1234, $DS:1234
- $KRM, $VDE8¹, $VDE8\_1
- $VGF:A, $VGF:DⅣ, $VGF:Dⅱ (bei Unicode-römischen Ziffern sind
  Groß-/Kleinschreibung egal, aber $VGF:Dii geht nicht!)
- \#VGF:BM<del>, \#VGF:wbd</del>

Code
====

Der Reguläre Ausdruck zum Finden der Kürzel ist (es werden überlappende
matches gesucht, damit "#FKW #FF" auch gefunden werden kann):

        (?p)                # find longest match
        (?:^|\W)            # either at the beginning of the text or after a non-alphanumeric character, but don't find this
        (?:                 # Select source
            (\$|\#)         # Special character to find something: # or $
            (?:(\p{Lu}+):)? # Optional prefix, e.g. "DS:" or "VGF:"
        )
        (                   # Payload
            [\p{Lu}\p{N}_]+ # All uppercase letters plus all kinds of numbers plus _
        )
        (?:$|\W)            # either end of string or non-\w character

