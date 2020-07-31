Konfigurationen
===============

Im Quelltextverzeichnis data/ sind die Daten-Konfigurationen, die
bestimmen, welche Daten in die Datenbank geladen werden und mit welchen
Hashtags, Quellen und Typen sie verfügbar sind. Die Datenlisten sind in
sources/ zu finden.

Format
------

Die einzelnen Dateien sind im JSON-Format, spezifisch so, dass die
python3-json-Bibliothek sie parsen kann. (Im Zweifel die vorhandenen
Dateien als Vorlage benutzen.)

Inhalt
------

In der obersten Ebene müssen folgende Schlüssel vorhanden sein:

- id (string): Gibt der Quelle einen eindeutigen Namen
- access (liste, siehe unten)
- data (liste, siehe unten)

Folgende Schlüssel werden zusätzlich erkannt:

- headline (string): Die Überschrift dieser Quelle. Wenn nicht
  vorhanden, wird description benutzt, wenn auch nicht vorhanden, wird
  die id benutzt.
- description (string): Der "Untertitel" der Quelle. Wenn nicht
  vorhanden, wird keiner benutzt.
 
### access

Der Schlüssel access enthält eine Liste von Arten, wie auf diese Quelle
zugegriffen werden kann, bestehend aus (alle Schlüssel müssen vorhanden
sein):

- type [string]: Das Typenzeichen für diese Art von Listen. Momentan
  wird verwendet:
  - \# für Orte und Betriebsstellen
  - $ für Strecken
  - % für Signale
  - / für Linien
  - &amp; für allgemeine Abkürzungen
- m\_hashtag [string]: Der Magic Hashtag für diese Quelle, in dessen
  Bereich ein Suchbegriff ohne explizit angegebene Quelle dieser Quelle
  zugeordnet wird. (Ohne führendes \#!)
- x\_source [string]: Die explizite Quellenangabe (siehe unten)

Die explizite Quelle darf nur aus Großbuchstaben bestehen. Der Magic
Hashtag sollte gleich der expliziten Quelle sein, aber mit einem
Unterstrich davor, also z.B. '\_FFM' zu 'FFM'.

### data

Der Schlüssel data enthält eine Liste von Datenlisten, die dieser Quelle
hinzugefügt werden sollen. Grundsätzlich sollten Sammlungen, die
verschiedene Herkünfte haben, und daher unterschiedliche
Ersteller\*innen und/oder Lizenzen, in verschiedenen Datenlisten sein
und können hier zusammengesetzt werden.

Folgende Schlüssel sind unbedingt erforderlich:

- id [string]: Identifiziert diese Datenliste. Darf bei **einer**
  Datenliste pro Quelle weggelassen werden, diese 'erbt' dann die id der
  Quelle.
- file [string]: Verweist auf die CSV-Datei, die die Daten enthält.
  Relativ zum Hauptverzeichnis, also meistens
  "source/datenlistenname.csv".
- short [string]: Spaltenname im CSV, das die zu findenden Abkürzungen
  enthält
- long [string]: Spaltenname im CSV, das die langform enthält
- source [siehe unten]

Folgende Schlüssel werden erkannt, wenn sie vorhanden sind:

- add [string] Spaltenname im CSV für zusätzliche Informationen. Diese
  werden bisher an keiner Stelle ausgelesen und/oder verarbeitet.
- delim [string, default ';']: Das Zeichen, mit dem Spalten im CSV
  voneinander getrennt sind
- nolink [boolean (true/false), default false]: Wenn true, werden alle
  Punkte in der Datenliste durch ein Ersatzzeichen (U+2024) ersetzt, um
  zu verhindern, dass Twitter versehentlich eine Antwort als Link
  interpretiert.
- comments [liste von strings]: Kommentare zur Datenliste. Beliebiger
  Text, der zum Verständnis der Quelle, der Inhalte oder der Herkunft
  wichtig sein könnte.
- filter [liste, siehe unten]
- license [siehe unten]

#### source

Spezifiziert die Herkunft der Datenliste.

Benötigte Schlüssel:

- name [string, darf nicht leer sein]: Bezeichnung der Herkunft. (z.B.
  "Eigene Zusammenstellung", "Dokument 1234 der
  Boteisenbahngesellschaft")

Optionale Schlüssel:

- url [url]: Link zur externen Quelle, aus der die Datenliste genommen
  wurde
- modified [boolean (true/false), default false]: Gibt an, dass die
  Datenliste hier gegenüber der externen Quelle geändert wurde.

#### license

Spezifiziert das Urheberrecht an dieser Datenliste. Wenn nicht
vorhanden, bedeutet das, dass das Urheberrecht dieser Liste beim Autor
des Bots liegt und die Liste unter Apache Lizenz 2.0 veröffentlicht ist.

Benötigt:

- name [string, darf nicht leer sein]: Name der Lizenz. Darf eine
  gängige Abkürzung sein ("CC-BY-SA 4.0", "CC0") oder auch ein Text
  ("gemeinfrei").

Optional:

- url [url]: Link zum Text der Lizenz, falls vorhanden
- owner [objekt]: Spezifiziert, wer das Urheberrecht auf diese
  Datenliste innehat. Darf weggelassen werden, wenn es bei der
  speziellen Lizenz keinen Sinn macht (etwa, wenn die Lizenz
  'gemeinfrei' ist). Besteht aus:
  - type [string]: Welcher Art dieses Objekt ist. Mögliche Arten:
    - "name": "name" ist einfach nur ein Name.
    - "twitter": "name" ist eine Twitter-Userin (ohne \@, also "\_ds\_100")
    - "github": "name" ist eine Github-Userin
    - "link": Hier wird ein beliebiger Link gesetzt mit dem Text "name"
      und dem Ziel "url"
  - name [string]: Siehe oben
  - url [url, optional]: Siehe oben.
