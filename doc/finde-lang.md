<p id="meta">
<title>DS-100: Finden der Abkürzungen</title>
<desc>Was hält der Bot für Abkürzungen und wie interpretiert er das?</desc>
</p>

Finden der Abkürzungen
======================

Wurde ein [Toot gefunden](/finde-toots.html) und die [aktuelle
Abkürzungsliste](/finde-listen.html) festgestellt, wird der Text nach
beantwortbaren Kürzeln durchsucht. Je nach Kontext werden
unterschiedliche Dinge gefunden / beantwortet. __In jedem Fall ist
Groß-/Kleinschreibung der Kürzel wichtig!__

Wir nehmen als Beispiel __HE__, das nach [DS100](/dumps/orte_de.html) „Emden“
bedeutet, bei den [VGF-Haltestellen](/dumps/orte_ffm.html) „Heerstraße“
und in der [Schweiz](/dumps/orte_ch.html) „Herisau“. __He__ in Quelle
[DB640](/dumps/orte_at.html) bedeutet „Hegyeshalom“.

<table>
 <thead>
  <tr>
    <th rowspan="2">↓ Toot ist/hat…</th>
    <th colspan="2">Kürzel mit #,$,%,&amp;,/, aber ohne Quelle</th>
    <th colspan="3">Kürzel mit expliziter Quelle</th>
    <th colspan="2">Kürzel ohne #,$,%,&amp;,/</th>
  </tr>
  <tr>
   <th>#HE</th>
   <th>#He</th>
   <th>#FFM:HE</th>
   <th>#DS:HE</th>
   <th>#CH:HE</th>
   <th class="note">HE<sup>(1)</sup></th>
   <th class="note">He<sup>(2)</sup></th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <th>… Magic Hashtag #DS100</th>
   <td class="yes">HE: Emden</td>
   <td class="no">(nicht beantwortet)</td>
   <td class="yes" rowspan="7">FFM#HE: Heerstraße</td>
   <td class="yes" rowspan="7">HE: Emden</td>
   <td class="yes" rowspan="7">CH#HE: Herisau</td>
   <td class="note">HE: Emden</td>
   <td class="no" rowspan="7">(nicht beantwortet)</td>
  </tr>
  <tr>
   <th>… Magic Hashtag #&#x5f;FFM</th>
   <td class="yes">FFM#HE: Heerstraße</td>
   <td class="no">(nicht beantwortet)</td>
   <td class="note">FFM#HE: Heerstraße</td>
  </tr>
  <tr>
   <th>… Magic Hashtag #&#x5f;CH</th>
   <td class="yes">CH#HE: Herisau</td>
   <td class="no">(nicht beantwortet)</td>
   <td class="note">CH#HE: Herisau</td>
  </tr>
  <tr>
   <th>… Magic Hashtag #&#x5f;AT</th>
   <td class="no">(nicht beantwortet)</td>
   <td class="yes">AT#He: Hegyeshalom</td>
   <td class="no">(nicht beantwortet)</td>
  </tr>
  <tr>
   <th>… explizite Erwähnung ohne Magic Hashtag</th>
   <td class="yes">HE: Emden</td>
   <td class="no">(nicht beantwortet)</td>
   <td class="note">HE: Emden</td>
  </tr>
  <tr>
   <th>… implizite Erwähnung ohne Magic Hashtag</th>
   <td class="yes">HE: Emden</td>
   <td class="no">(nicht beantwortet)</td>
   <td class="no">(nicht beantwortet)</td>
  </tr>
  <tr>
   <th>… in Timeline ohne Erwähnung oder Magic Hashtag</th>
   <td class="yes">HE: Emden</td>
   <td class="no">(nicht beantwortet)</td>
   <td class="no">(nicht beantwortet)</td>
  </tr>
 </tbody>
</table>

(1): Kürzel ohne \#, $, &amp;, % oder / werden nur gefunden, wenn sonst
keine Kandidaten im Toot vorhanden sind.<br/>
(2): Nur Kürzel ohne Kleinbuchstaben werden bei der Suche ohne \#, $,
&amp;, % oder / gefunden.

<table>
 <thead>
  <tr>
   <th>↓ Toot A ist/hat… ↓/ → A … →</th>
   <th>… boostet Toot B mit Kommentar<br/>
       ODER<br/>
       … beantwortet Toot B:<br/>
       B wird…</th>
   <th>… enthält #folgenbitte oder #entfolgen</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <th>… hat ersten Magic Hashtag: #&#x5f;A</th>
   <td class="yes">…beantwortet, als hätte er Magic Hashtag #&#x5f;A</td>
   <td class="no">Wird ignoriert</td>
  </tr>
  <tr>
   <th>… explizite Erwähnung und Magic Hashtag #&#x5f;A</th>
   <td class="yes">…beantwortet, als hätte er Magic Hashtag #&#x5f;A</td>
   <td class="yes" rowspan="2">Wird ausgeführt</td>
  </tr>
  <tr>
   <th>… explizite Erwähnung ohne Magic Hashtag</th>
   <td class="yes">…beantwortet, als hätte er Magic Hashtag #DS100</td>
  </tr>
  <tr>
   <th>… implizite Erwähnung ohne Magic Hashtag</th>
   <td class="note">…ignoriert<sup>(3)</sup></td>
   <td class="no" rowspan="2">Wird ignoriert</td>
  </tr>
  <tr>
   <th>… in Timeline ohne Erwähnung oder Magic Hashtag</th>
   <td class="no">…ignoriert</td>
  </tr>
 </tbody>
</table>

(3): Beinhaltet A eine implizite Erwähnung des Bots und ein Zitat von B,
so wird B wahrscheinlich auch schon eine Erwähnung des Bots beinhalten,
sodass B bereits vom Bot gesehen worden sein sollte.

Aufbau der Kürzel
-----------------

- Abkürzungen bestehen aus (allen Arten von) Großbuchstaben,
  Kleinbuchstaben, Ziffern und Unterstrichen.
- Beinhaltet ein Kürzel in der Originalquelle ein Leerzeichen, so wird
  dies in einen Unterstrich umgewandelt.
- Mehrere aufeinanderfolgende Leerzeichen in der Originalquelle werden
  zu einem Unterstrich zusammengefasst (z.B. wird aus
  „AA&#x2420;&#x2420;G“ „AA\_G“).
- Leerzeichen dürfen nicht weggelassen werden. Siehe diese [Liste mit
  Betriebsstellen der DS100](/leerzeichen_ds100.html), bei denen es
  einen Unterschied macht.

Den eigentlichen Abkürzungen wird vorangestellt:

- Ein Sonderzeichen, dass die Art der Quelle anzeigt. Wird dies
  weggelassen (siehe Tabelle oben), ist es wie \#. Mögliche Zeichen:
  - __\#__ für Orte
  - __$__ für Strecken
  - __%__ für Signale
  - __&amp;__ für allgemeine Abkürzungen
  - __/__ für Linien
- Ein Bezeichner für die Quelle, siehe ebenfalls die Tabellen oben.
  Diese Bezeichner bestehen nur aus Großbuchstaben und werden von einem
  Doppelpunkt beendet.
- Ist kein solcher Bezeichner vorhanden, wird das Kürzel in der Quelle
  laut aktuellem Magic Hashtag oder der Quelle ‚BOT:‘ gesucht.

Einträge in der [Schwarzliste](/blacklist.html) können durch benutzen
der Quelle angezeigt werden.

### Beispiele

- \#FKW, \#DS:FKW
- $1234, $DS:1234
- $KRM, $VDE8¹
- $FFM:A, $FFM:DⅣ, $FFM:Dⅱ (bei Unicode-römischen Ziffern sind
  Groß-/Kleinschreibung egal, aber $VGF:Dii geht nicht!)
- \#FFM:BM
- \#AT:He
