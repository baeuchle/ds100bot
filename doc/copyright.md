Daten und Urheberrecht
======================

Output des Bots
---------------

Die Tweets des Bots besitzen keine ausreichende Schöpfungstiefe, die
die Anwendung eines Urheberrechtes rechtfertigen würden. Die vom Bot
benutzten Datensammlungen unterliegen verschiedenen Copyrights, siehe
unten.

Verwendete Daten
----------------

Der Bot greift auf verschiedene Datenquellen zurück. Die Auswahl der
Datenquelle geschieht auf Grund des ersten Teils des Suchbegriffs, etwa
bei ‚\#DS:FF‘ der Teil ‚__\#DS:__‘. Ist kein solcher Teil vorhanden
(‚FF‘) oder besteht er nur aus ‚__\#__‘ oder ‚__\$__‘ (‚\#FF‘), werden
die Quellen aus dem aktuellen __[Magic Hashtag](magic.html)__ oder
__\#BOT__ (nur bei ‚__\#__‘) benutzt.

Folgende Datenquellen werden vom Bot benutzt:

<table>
 <thead>
  <tr>
   <td></td>
   <th>Beschreibung</th>
   <th>Quelle</th>
   <th>Lizenz</th>
   <th>Anmerkungen</th>
   <th>Dump</th>
   <th>Magic Hashtag</th>
  </tr>
 </thead>
 <tbody>
  <tr><th>#DS</th>
   <td>DS100 der Deutschen Bahn</td>
   <td><a href="https://data.deutschebahn.com/dataset/data-betriebsstellen">Betriebsstellenverzeichnis der Deutschen Bahn AG</a></td>
   <td><a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</a></td>
   <td style="text-align: left;">
    <ul>
     <li>Punkte durch ONE DOT LEADER U+2024 ‚&#x2024;‘ ersetzt</li>
     <li>Mehrere Leerzeichen zusammengefasst</li>
     <li>Einzelne Einträge korrigiert</li>
    </ul>
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/ds100.html">ds100</a>
   </td>
   <td rowspan="4">
    #DS100, #_DE
   </td>
  </tr>
  <tr><th>$DS</th>
   <td>Streckennummern der Deutschen Bahn</td>
   <td><a href="https://data.deutschebahn.com/dataset/geo-strecke">Geo-Streckennetz</a></td>
   <td><a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</a></td>
   <td style="text-align: left;">
    <ul>
     <li>Punkte durch ONE DOT LEADER U+2024 ‚&#x2024;‘ ersetzt</li>
     <li>Mehrere Leerzeichen zusammengefasst</li>
     <li>Nicht-numerische Einträge in Eigenarbeit zusammengestellt (Bsp.
     ‚$DS:KRM‘)</li>
    </ul>
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/benannte_strecken.html">benannte_strecken</a>
    <a href="https://ds100.frankfurtium.de/dumps/strecken.html">strecken</a>
   </td>
  </tr>
  <tr><th>%DS</th>
   <td>Signale in der ESO</td>
   <td>Zusammenstellung von <a href="https://twitter.com/autinerd/">@autinerd</a></td>
   <td><a href="https://creativecommons.org/licenses/by-sa/4.0/">CC-BY-SA 4.0</a></td>
   <td style="text-align: left;">
    <ul>
     <li>Gibt es in DV301 (ehem. DR) und DS301 (ehem. DB) unterschiedliche
     Signale mit gleichem Namen, wird die DS301-Variante beantwortet.</li>
     <li>Signalnamen mit "/" können aus technischen Gründen nicht beantwortet
     werden. Das betrifft Vr1/2 (aus der DV301).</li>
    </ul>
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/ds301.html">ds301</a>
   </td>
  </tr>
  <tr><th>&DS</th>
   <td>Allgemeine Abkürzungen Bahn (Deutschland)</td>
   <td>Zusammenstellung von <a href="https://twitter.com/autinerd/">@autinerd</a></td>
   <td><a href="https://creativecommons.org/licenses/by-sa/4.0/">CC-BY-SA 4.0</a></td>
   <td style="text-align: left;">
    <ul>
     <li>Beinhaltet Abkürzungen aus dem Betriebsregelwerk des VDV und
     der Ril 408 der Deutschen Bahn</li>
     <li>Liste ist auf Bahn-eigene und nicht komplett offensichtliche
     Abkürzungen („Ellok“ für „Elektrolokomotive“) begrenzt</li>
     <li>Groß- und Kleinschreibung ist sehr wichtig. Beispiele: „ZS“: Zugsammelschiene, „Zs“: Zugschaffner.</li>
     <li>Signaltypen gibt es allerdings doppelt: „Asig“ und „ASig“ bzw. „Zvsig“ und „ZVsig“.</li>
    </ul>
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/brw.html">brw</a>
   </td>
  </tr>
  <tr><th>#LP</th>
   <td>Leitpunkte (Fahrkartencodes)</td>
   <td><a href="https://www.bahn.de/p/view/mdb/bahnintern/agb/entfernungswerk/mdb_305971_teil_2-3_tarifpunkte_anstobahnhfe_regionen.pdf">Tarifpunkte</a> via <a href="https://www.bahn.de/p/view/home/agb/agb.shtml">Beförderungsbedingungen der DB</a></td>
   <td>© DB</td>
   <td>Aus der Liste extrahiert</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/leitpunkte.html">leitpunkte</a>
   </td>
   <td>
    #_LP
   </td>
  </tr>
  <tr><th>#AT</th>
   <td>DB 640 der ÖBB</td>
   <td>Zusammenstellung von <a href="https://bahn.hauptsignal.at/">Christoph Schönweiler</a> (Stand 2020)</td>
   <td>© ÖBB-Infrastruktur Betrieb AG</td>
   <td>Quelle ist nicht offiziell. Groß-/Kleinschreibung muss beachtet werden, es sind auch Kleinbuchstaben erlaubt!</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/db640.html">db640</a>
   </td>
   <td>
    #DB640, #_AT
   </td>
  </tr>
  <tr><th>#CH</th>
   <td>Schweizer Bahnhöfe</td>
   <td><a href="https://opendata.swiss/de/dataset/haltestellen-des-offentlichen-verkehrs">Haltestellen des öffentlichen Verkehrs</a> via <a href="https://data.sbb.ch/explore/dataset/dienststellen-gemass-opentransportdataswiss/information/">data.sbb.ch</a></td>
   <td><a href="https://opendata.swiss/de/dataset?q=haltestelle&organization=bundesamt-fur-verkehr-bav&res_rights=NonCommercialAllowed-CommercialAllowed-ReferenceRequired">ähnlich CC-BY</a></td>
   <td>Aus der Orignalquelle sind nur diejenigen Einträge übernommen, die wirklich eine Abkürzung haben.</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/ch.html">ch</a>
   </td>
   <td>
    #_CH
   </td>
  </tr>
  <tr><th>#FR</th>
   <td>Französische Bahnhöfe</a></td>
   <td><a href="https://ressources.data.sncf.com/explore/dataset/lexique-des-acronymes-sncf/">Lexique des abréviations SNCF</a></td>
   <td><a href="https://opendatacommons.org/licenses/odbl/">ODbL</a></td>
   <td>
    Scheinbar war die Originalquelle früher all-caps und wird langsam
    umgestellt. Das ist aber nur bis C oder D gekommen, danach wird's etwas
    uneinheitlich.
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/sncf.html">sncf</a>
   </td>
   <td>
    #_FR
   </td>
  </tr>
  <tr><th>#NL</th>
   <td>Betriebsstellen in den Niederlanden</td>
   <td><a href="https://wetten.overheid.nl/BWBR0017707/2020-04-01/#Bijlage6">Anhang 6 zu Regeling spoorverkeer</a> (Stand 2020)</td>
   <td>Gemeinfrei, da Gesetz</td>
   <td></td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/nederlands.html">nederlands</a>
   </td>
   <td>
    #_NL
   </td>
  </tr>
  <tr><th>#NO</th>
   <td>Betriebsstellen des norwegischen Eisenbahnnetzes</td>
   <td><a href="https://www.banenor.no/kundeportal/ruter-og-sportilgang/grafiske-togruter1/">Grafische Fahrpläne</a> (Stand 2020)</td>
   <td>Gemeinfrei</td>
   <td>Selbst abgetippt</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/banenor.html">banenor</a>
   </td>
   <td>
    #_NO
   </td>
  </tr>
  <tr><th rowspan="2">#UK</th>
   <td rowspan="2">Haltestellen und Bahnhöfe in England/Vereinigtes Königreich</td>
   <td><a href="http://data.atoc.org/how-to">Rail Delivery Group</a> (Stand 2020)</td>
   <td><a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</a></td>
   <td>Aus Fixed-width-Text extrahiert und Namen mit Kleinbuchstaben
   versehen<br/>
   4- bis 7-stellige Kürzel</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/raildeliverygroup.html">raildeliverygroup</a>
   </td>
   <td rowspan="2">
    #_UK
   </td>
  </tr>
  <tr><td><a href="https://www.nationalrail.co.uk/stations_destinations/48541.aspx">National Rail Enquiries</a> (Stand 2018)</td>
   <td><em>unbekannt</em></td>
   <td>Dreistellige Kürzel</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/nationalrail.html">nationalrail</a>
   </td>
  </tr>
  <tr><th>#FFM</th>
   <td>Haltestellen der <a href="https://vgf-ffm.de">VGF</a></td>
   <td>Eigene Zusammenstellung, Hilfe aus privaten Nachrichten und dem
   <a
   href="https://frankfurter-nahverkehrsforum.de/forum/index.php?thread/20682-stationskürzel/">Frankfurter
   Nahverkehrsforum</a></td>
   <td>Gemeinfrei</td>
   <td>
    Alle Stadtbahn- und von der Leitstelle betreuten
    Straßenbahnhaltestellen haben ein Kürzel aus zwei Buchstaben plus
    eventuell die Tunnelebene; andere Betriebsstellen haben längere
    Kürzel. Alle Stadtbahnhaltestellen haben dreistellige Nummern,
    Straßenbahnhaltestellen haben vierstellige Nummern (diese sind
    allerdings nur lückenhaft bekannt).
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/vgfhst.html">vgfhst</a>
   </td>
   <td rowspan="3">
    #_FFM
   </td>
  </tr>
  <tr><th>$FFM</th>
   <td>Stadtbahnstrecken der <a href="https://vgf-ffm.de">VGF</a></td>
   <td>Eigene Zusammenstellung aus <a
   href="https://de.wikipedia.org/wiki/Vorlage:Krakies/Nagel">Krakies /
   Nagel</a></td>
   <td>Gemeinfrei</td>
   <td>
    Alle Bauabschnitte der Stadtbahnstrecken können mit großen
    lateinischen Buchstaben oder den Unicode-Zeichen für römische Zahlen
    geschrieben werden: ‚$FFM:DIV‘ = ‚$FFM:DⅣ‘ = ‚$FFM:Dⅳ‘.
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/vgfstrecken.html">vgfhst</a>
   </td>
  </tr>
  <tr><th>/FFM</th>
   <td>Stadtbahn- und Straßenbahnlinien aus Frankfurt am Main</td>
   <td>Eigene Zusammenstellung</td>
   <td>Gemeinfrei</td>
   <td>
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/vgflinien.html">vgflinien</a>
   </td>
  </tr>
  <tr><th>#HH</th>
   <td>Hamburger U-Bahn-Haltestellen</td>
   <td><a href="http://www.hamburger-bahnhoefe.de/">Hamburger-Bahnhöfe.de</a></td>
   <td><em>unbekannt</em></td>
   <td>Privat zusammengestellte Liste</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/hhe.html">hhe</a>
   </td>
   <td>
    #_HH
   </td>
  </tr>
  <tr><th>#W</th>
   <td>Betriebsstellen der Wiener Linien</td>
   <td><a href="https://bahn.hauptsignal.at/">Christoph Schönweilers hauptsignal.at</a> (Stand 2020)</td>
   <td></td>
   <td>Datenbanksuche auf <a href="https://bahn.hauptsignal.at/bsb.php">hauptsignal.at</a></td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/wien_vor.html">wien_vor</a>
   </td>
   <td>
    #_W
   </td>
  </tr>
  <tr><th>#BOT</th>
   <td>Informationen über den Bot</td>
   <td>Eigene Zusammenstellung</td>
   <td>Gemeinfrei</td>
   <td></td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/gimmick.html">gimmick</a>
   </td>
   <td></td>
  </tr>
 <tbody>
</table>
