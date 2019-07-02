Beispiele zur Interaktion mit dem Bot
=====================================

Auf dieser Seite sind ein paar Interaktionsbeispiele mit dem Bot
dargestellt. Jede Box entspricht einem Tweet, eingerückte Boxen
antworten auf den letzten weniger eingerückten Tweet. Die Tweet-Handles
(außer @\_ds\_100) werden nur genutzt, um die Rolle darzustellen und
haben nichts mit etwaigen Twitter-Accounts des gleichen Namens zu tun:
__@ungefolgter__ ist ein öffentlicher Account, der vom Bot nicht gefolgt
wird, __@gefolgter__ wird vom Bot gefolgt und __@irgendwer__ ist ein
beliebiger (öffentlicher) Account, der dem Bot folgen kann oder nicht.

Um deutlich zu machen, auf was der Bot jeweils reagiert, werden immer
\#FF (Frankfurt (Main) Hbf) (Hashtag, Großbuchstaben), \#fkw
(Kassel-Wilhelmshöhe) (Hashtag, Kleinbuchstaben) und HG (Göttingen)
(Kein Hashtag, Großbuchstaben) benutzt. Andere Kombinationen (#Ff, #fF,
hg, Hg, hG) werden immer ignoriert.

---------

Markierung mit Hashtag #DS100:

<blockquote class="tweet_irgendwer">
Hallo #FF #fkw HG #DS100
</blockquote>

<blockquote class="tweet_bot antwort">
FF: Frankfurt (Main) Hbf<br/>
FKW: Kassel-Wilhelmshöhe
</blockquote>

---------

Markierung des Bots:

<blockquote class="tweet_irgendwer">
Hallo #FF #fkw HG @_ds_100
</blockquote>

<blockquote class="tweet_bot antwort">
FF: Frankfurt (Main) Hbf<br/>
FKW: Kassel-Wilhelmshöhe<br/>
  <h3>Output</h3>
  <p>
    Mehrere gefundene Abkürzungen werden in der Reihenfolge der Erwähnung im
    Tweet erweitert; eine Erweiterung wird dabei nicht wiederholt. Wenn alle
    Erweiterungen nicht in einen Tweet passen, werden mehrere Tweets
    gesendet, die aufeinander antworten. Innerhalb einer solchen Gruppe
    von Tweets werden Erweiterungen auch nicht wiederholt.
  </p>
HG: Göttingen
</blockquote>

---------

User, denen der Bot folgt (siehe [folgen](/folgen))

<blockquote class="tweet_follower">
Hallo #FF #fkw HG
</blockquote>

<blockquote class="tweet_bot antwort">
FF: Frankfurt (Main) Hbf<br/>
</blockquote>

Antworten
---------

<blockquote class="tweet_nofollow">
Ich vergesse, den Bot zu erwähnen. #FF #fkw HG
</blockquote>

<blockquote class="tweet_irgendwer antwort">
@_ds_100
</blockquote>

<blockquote class="tweet_bot antwort">
FF: Frankfurt (Main) Hbf<br/>
FKW: Kassel-Wilhelmshöhe<br/>
HG: Göttingen
</blockquote>
(Der @\_ds\_100-Tweet antwortet auf @ungefolgter's Tweet erst getriggert
durch @irgendwer's Tweet.)

---------

<blockquote class="tweet_irgendwer">
Guck mal @_ds_100, ich retweete diesen Tweet mit Kommentar:
<blockquote class="tweet_nofollow">
Ich vergesse, den Bot zu erwähnen. #FF #fkw HG
</blockquote>
<blockquote class="tweet_bot antwort">
FF: Frankfurt (Main) Hbf<br/>
FKW: Kassel-Wilhelmshöhe<br/>
HG: Göttingen
</blockquote>
</blockquote>

(Auch dieser @\_ds\_100-Tweet antwortet erst getriggert durch den
Retweet / das Zitat.)

---------

<blockquote class="tweet_nofollow">
Ich tweete irgendetwas
</blockquote>
<blockquote class="tweet_follower antwort">
Da Antworte ich doch mal mit #FF #fkw HG!
</blockquote>

Diese Antwort wird wahrscheinlich nicht vom Bot gefunden, weil Antworten
nur dann in der Timeline auftauchen, wenn demjenigen Account, dem
geantwortet wird, auch gefolgt wird (wie für alle Twitternutzenden). Mit
Hashtag #DS100 oder Mention @\_ds\_100 funktioniert es wie ganz oben
beschrieben.

---------

In der folgenden Situation kann der Bot unabsichtlich getwittert werden:

<blockquote class="tweet_irgendwer">
Dieser Tweet triggert den Bot #FF #fkw HG #DS100
</blockquote>

<blockquote class="tweet_bot antwort">
FF: Frankfurt (Main) Hbf<br/>
FKW: Kassel-Wilhelmshöhe
</blockquote>

<blockquote class="tweet_irgendwer antwort2">
Dieser Tweet triggert den Bot auch HG
</blockquote>

<blockquote class="tweet_bot antwort3">
HG: Göttingen
</blockquote>

Hier ist im dritten Tweet eine Mention an den Bot versteckt, die dieser
nicht von der expliziten Mention mit @\_ds\_100 im Text unterscheiden
kann.
