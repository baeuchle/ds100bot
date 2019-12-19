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

function link_liste {
    sed "s/VERSION/$1/" links.snip
}

function bot_footer {
cat <<EOF
  <hr/>
EOF
link_liste $1
cat <<EOF
 </body>
</html>
EOF
}
