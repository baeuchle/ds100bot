<p id="meta">
<title>DS-100: Finden von Tweets</title>
<desc>Welche Tweets betrachtet der Bot, um sie zu beantworten?</desc>
</p>

Finden von Tweets
=================

Der Bot durchsucht Twitter nach

- Tweets in seiner Timeline, also von Benutzenden, denen der Bot folgt
  (siehe [Interaktion](/interaktion.html)). Antworten auf nicht-Gefolgte
  werden meistens nicht gefunden.
- Tweets, die den Bot erwähnen:
  - Explizite Erwähnungen (d.h., @\_ds\_100 steht im sichtbaren Text)
  - Implizite Erwähnungen (z.B. Antworten auf den Bot oder auf Tweets,
    die den Bot erwähnen)
- Tweets, die einen der [Magic Hashtags](/finde-listen.html) im normalen
  Text (nicht im Alternativtext von Medien) enthalten.

Der Bot schließt aus:
- Pure Retweets
- Seine eigenen Tweets

Wird in einem Tweet **A** ein anderer Tweet **B** beantwortet oder
zitiert (das ist dieses 'Mit Kommentar retweeten'), so wird Tweet **B**
ebenfalls betrachtet. Die Ausschlusskriterien treffen auch hier zu.

Sind die Tweets gefunden, wird als nächstes analysiert, [welche
Abkürzungslisten benutzt werden sollen](/finde-listen.html)
