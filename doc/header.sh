#!/bin/bash

function bot_header {
cat <<EOF
<?xml version="1.0" encoding="utf-8" standalone="no"?>
<html>
 <head>
  <meta charset="utf-8">
  <link rel="stylesheet" type="text/css" href="/bot.css"/>
  <link rel="shortcut icon" type="image/svg+xml" href="https://avatar.frankfurtium.de/ds100.svg" />
  <title>$1</title>
 </head>
 <body>
EOF
}

function bot_footer {

cat <<EOF
  <hr/>
  <ul class="flat">
   <li><a href="index.html">DS100-bot</a></li>
   <li><a href="finderegeln.html">Finden von Tweets</a></li>
   <li><a href="blacklist.html">Schwarzliste (blacklist)</a></li>
   <li><a href="contribute.html">Beitragen</a></li>
   <li><a href="motivation.html">Motivation</a></li>
   <li><a href="haftung.html">Haftungsausschluss</a></li>
   <li><a href="copyright.html">Daten / Urheberrecht</a></li>
   <li><a href="dumps/">Dumps</a></li>
   <li><a href="datenschutz.html">Datenschutz</a></li>
   <li><a href="impressum.html">Impressum</a></li>
   <li>Version: $1</li>
  </ul>
 </body>
</html>
EOF
}
