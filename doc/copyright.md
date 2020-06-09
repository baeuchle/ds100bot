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
  <tr>
   <th>#DS</th>
   <td>DS100 der Deutschen Bahn</td>
   <td><a href="https://data.deutschebahn.com/dataset/data-betriebsstellen">Betriebsstellenverzeichnis der Deutschen Bahn AG</a></td>
   <td><a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</a></td>
   <td>
    <ul>
     <li>Punkte durch ONE DOT LEADER U+2024 ‚&#x2024;‘ ersetzt</li>
     <li>Mehrere Leerzeichen zusammengefasst</li>
    </ul>
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/ds100.html">ds100</a>
   </td>
   <td>
    #DS100
   </td>
  </tr>
  <tr>
   <th>$DS</th>
   <td>Streckennummern der Deutschen Bahn</td>
   <td><a href="https://data.deutschebahn.com/dataset/geo-strecke">Geo-Streckennetz</a></td>
   <td><a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</a></td>
   <td>
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
   <td>
    #DS100
   </td>
  </tr>
  <tr>
   <th>#VGF</th>
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
   <td>
    #_FFM
   </td>
  </tr>
  <tr>
   <th>$VGF</th>
   <td>Stadtbahnstrecken der <a href="https://vgf-ffm.de">VGF</a></td>
   <td>Eigene Zusammenstellung aus <a
   href="https://de.wikipedia.org/wiki/Vorlage:Krakies/Nagel">Krakies /
   Nagel</a></td>
   <td>Gemeinfrei</td>
   <td>
    Alle Bauabschnitte der Stadtbahnstrecken können mit großen
    lateinischen Buchstaben oder den Unicode-Zeichen für römische Zahlen
    geschrieben werden: ‚$VGF:DIV‘ = ‚$VGF:DⅣ‘ = ‚$VGF:Dⅳ‘.
   </td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/vgfstrecken.html">vgfhst</a>
   </td>
   <td>
    #_FFM
   </td>
  </tr>
  <tr>
   <th>#ÖBB</th>
   <td>DB 640 der ÖBB</td>
   <td><a href="http://www.bahnnews-austria.at/downloads/sonstiges/DB640.pdf">Bahnnews-Austria</a></td>
   <td>© ÖBB-Infrastruktur Betrieb AG</td>
   <td>Quelle ist nicht offiziell und scheint veraltet (von 2007)</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/db640.html">db640</a>
   </td>
   <td>
    #DB640
   </td>
  </tr>
  <tr>
   <th>#NOR</th>
   <td>Betriebsstellen des norwegischen Eisenbahnnetzes</td>
   <td><a href="https://www.banenor.no/kundeportal/ruter-og-sportilgang/grafiske-togruter1/">Grafische Fahrpläne</a> (Stand 2020)</td>
   <td>Gemeinfrei</td>
   <td>Selbst abgetippt</td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/banenor.html">banenor</a>
   </td>
   <td>
    #_NSB
   </td>
  </tr>
  <tr>
   <th>#VOR</th>
   <td>Betriebsstellen der Wiener Linien</td>
   <td><a href="https://bahn.hauptsignal.at/">Christoph Schönweilers hauptsignal.at</a> (Stand 2020)</td>
   <td></td>
   <td>Datenbanksuche auf <a href="https://bahn.hauptsignal.at/bsb.php">hauptsignal.at</a></td>
   <td>
    <a href="https://ds100.frankfurtium.de/dumps/wien_vor.html">wien_vor</a>
   </td>
   <td>
    #_VOR
   </td>
  </tr>
  <tr>
   <th>#BOT</th>
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
