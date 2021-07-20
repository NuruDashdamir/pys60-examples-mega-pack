#!/bin/sh

if test -z "$1"; then
  echo "gendist.sh sourcedir"
  exit 1
fi

SRCDIR="$1"
VERSION="`grep -E '"Ensymble v[0-9\.]+ [0-9-]+"' "$SRCDIR/cmd_version.py" | sed -re 's/^.*Ensymble v([0-9\.]+).*$/\1/'`"

echo "Ensymble version $VERSION"

# Create a suitably named tar.gz archive.
cp -a "$SRCDIR" "ensymble-$VERSION"
rm -f "ensymble-$VERSION.tar.gz" "ensymble-$VERSION.zip"
tar zcvf "ensymble-$VERSION.tar.gz" --exclude CVS --exclude "*~" --exclude "*.pyc" "ensymble-$VERSION"
rm -r "ensymble-$VERSION"

echo "ensymble-$VERSION.tar.gz created."
