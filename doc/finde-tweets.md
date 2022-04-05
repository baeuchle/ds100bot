<p id="meta">
<title>DS-100: Finden von Tweets</title>
<desc>Welche Tweets betrachtet der Bot, um sie zu beantworten?</desc>
</p>

Finden von Tweets
=================

Der Bot durchsucht <span class="only-twitter">Twitter</span> <span
class="only-mastodon">Mastodon</span> nach

- <span class="only-twitter">Tweets</span> <span
  class="only-mastodon">Toots</span> in seiner Timeline, also von
  Benutzenden, denen der Bot folgt (siehe
  [Interaktion](/interaktion.html)). Antworten auf nicht-Gefolgte werden
  meistens nicht gefunden.
- Tweets, die den Bot erwähnen:
  - Explizite Erwähnungen (d.h., <span
    class="only-twitter">@\_ds\_100</span> <span
    class="only-mastodon">@ril100@botsin.space</span> steht im
    sichtbaren Text)
  - Implizite Erwähnungen (z.B. Antworten auf den Bot oder auf Tweets,
    die den Bot erwähnen)
- <span class="only-twitter">Tweets, die einen der [Magic
  Hashtags](/finde-listen.html) im normalen Text (nicht im
  Alternativtext von Medien) enthalten.</span> <span
  class="only-mastodon">[Magic Hashtags](/finde-listen.html) können bei
  Mastodon **nicht** dafür benutzt werden, Toots zu finden.</span>

Der Bot schließt aus:

- Pure Retweets
- Seine eigenen Tweets

Wird in einem Tweet **A** ein anderer Tweet **B** beantwortet oder
zitiert (das ist dieses 'Mit Kommentar retweeten'), so wird Tweet **B**
ebenfalls betrachtet. Die Ausschlusskriterien treffen auch hier zu.

Sind die Tweets gefunden, wird als nächstes analysiert, [welche
Abkürzungslisten benutzt werden sollen](/finde-listen.html)
