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
(‚FF‘) oder besteht er nur aus ‚__\#__‘ (‚\#FF‘), werden die Quellen
__\#DS__ oder __\#BOT__ benutzt; ist dieser Teil ‚__$__‘, so wird die
Quelle __$DS__ benutzt.

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
  </tr>
  <tr>
   <th>#BOT</th>
   <td>Informationen über den Bot</td>
   <td>Eigene Zusammenstellung</td>
   <td>Gemeinfrei</td>
   <td></td>
  </tr>
 <tbody>
</table>
