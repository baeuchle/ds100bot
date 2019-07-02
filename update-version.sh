#!/bin/bash

exec 3>&1 1>version.py

echo "gitdescribe='$(git describe --always --dirty)'"
echo "githash='$(git log --pretty=%H -1)'"
echo "datahash = {}"
for srcfile in data_sources/*; do
    src=${srcfile/.csv/}
    echo "datahash['$src']='$(sha1sum $srcfile | awk '{print $1}')'"
done

echo "changelog = {}"

for target_version in $(git log --pretty=%H); do
    echo "changelog['$target_version'] = \"\"\""
    git log $target_version..HEAD \
      | grep ^\\s\\+CHANGELOG \
      | perl -pe 's/^\s+CHANGELOG/•/'
    echo '"""'
done

echo "changelog['0000000000000000000000000000000000000000'] = \"\"\""
git log \
  | grep ^\\s\\+CHANGELOG \
  | perl -pe 's/^\s+CHANGELOG/•/'
echo '"""'

exec 1>&3
cd html/
. create.sh

tdir=/var/www/ds100
if [ -d "$tdir" ]; then
    rsync *.html *.css $tdir/
    chmod 664 $tdir/*.html
fi

adir=/var/www/avatar
if [ -d "$adir" ]; then
    cp ../avatar.svg $adir/ds100.svg
    chmod 664 $adir/ds100.svg
fi
