#!/bin/sh

if test -z "$1"; then
  echo "install.sh targetpath [name]"
  exit 1
fi

if test -z "$PYTHON"; then
  PYTHON="python"
fi

name=ensymble
if test -n "$2"; then
  name="`basename "$2" .py`"
fi

"$PYTHON" squeeze/squeeze.py -1 -o "$name" -b cmdmain cmdmain.py \
  cmd_altere32.py cmd_genuid.py cmd_infoe32.py cmd_mergesis.py cmd_py2sis.py \
  cmd_signsis.py cmd_simplesis.py cmd_version.py cryptutil.py miffile.py \
  rscfile.py sisfield.py sisfile.py symbianutil.py defaultcert.py
cp "$name".py "$1"
chmod +x "$1"/"$name".py
rm "$name".py

echo "Ensymble command line tool installed as $1/$name.py"
