#!/bin/bash

cd doc/
. create.sh

tdir=/var/www/ds100
if [ -d "$tdir" ]; then
    rsync -via output/ $tdir/
    chmod 664 $tdir/*.*
    chmod 664 $tdir/*/*.*
fi

adir=/var/www/avatar
if [ -d "$adir" ]; then
    chmod 664 ../avatar.svg
    cp ../avatar.svg $adir/ds100.svg
fi
