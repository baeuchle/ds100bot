<p id="meta">
<title>DS-100: Finden von Toots</title>
<desc>Welche Toots betrachtet der Bot, um sie zu beantworten?</desc>
</p>

Finden von Toots
================

Der Bot durchsucht Mastodon nach

- Toots in seiner Timeline, also von Benutzenden, denen der Bot folgt
  (siehe [Interaktion](/interaktion.html)). Antworten auf nicht-Gefolgte
  werden meistens nicht gefunden.
- Toots, die den Bot erwähnen:
  - Explizite Erwähnungen (d.h., @ril100@zug.network steht im
    sichtbaren Text)
  - Implizite Erwähnungen (z.B. Antworten auf den Bot oder auf Toots,
    die den Bot erwähnen)
- [Magic Hashtags](/finde-listen.html) können **nicht** dafür benutzt
  werden, Toots zu finden.

Der Bot schließt aus:

- Pure Boosts
- Seine eigenen Toots

Wird in einem Toot **A** ein anderer Toot **B** beantwortet oder
zitiert, so wird Toot **B** ebenfalls betrachtet. Die
Ausschlusskriterien treffen auch hier zu.

Sind die Toots gefunden, wird als nächstes analysiert, [welche
Abkürzungslisten benutzt werden sollen](/finde-listen.html)
