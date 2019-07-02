#!/bin/bash

headfile=header.sh

. $headfile
version="$(git describe --always --dirty)"
echo $version

for md in *.md; do
  echo "Writing $md to ${md/md/html}"
  TITLE="@_ds_100: $(head -n 1 $md)"
  exec 3>&1 1>${md/md/html}
  echo "$(bot_header "$TITLE")"
  markdown $md
  echo "$(bot_footer $version)"
  exec 1>&3
done
