Finden von Tweets
=================

Der Bot findet Tweets auf vier verschiedenen Wegen:
- Markierung durch Hashtag \#DS100
- Explizites Erwähnen des Bots durch "@\_ds\_100" im Text
- Implizites Erwähnen des Bots durch Antworten auf einen Tweet des Bots
- Seine Timeline, das heißt, alle Tweets von Benutzer\*innen, denen der
  Bot folgt, außer Antworten auf nicht-gefolgte Benutzer\*innen.

Der Bot reagiert in den vier Fällen jeweils unterschiedlich:
- Bei implizite Erwähnungen und Timeline werden nur markierte Kürzel
  (mit \# oder $) gefunden.
- Bei Hashtags und expliziten Erwähnungen werden auch, falls keine
  markierten Kürzel gefunden werden, unmarkierte Kürzel gefunden
- Wird ein Tweet zitiert („mit Kommentar retweeten“) oder beantwortet
  und wird im Text dazu (also in der Antwort oder dem „Kommentar“) der
  Bot durch Hashtag oder explizite Erwähnung aufmerksam gemacht, so wird
  der Ursprungstweet auch betrachtet. Bei Erwähnung mit Hashtag werden
  nur markierte Kürzel gefunden, bei expliziter Erwähnung werden auch
  unmarkierte Kürzel gefunden.

In einem Tweet mit expliziter Erwähnung werden außerdem die Hahstags
\#folgenbitte und \#entfolgen erkannt, die den Bot dazu bringen, dem
Autor zu folgen beziehungsweise zu entfolgen.
