@echo off
echo *******************************************************************
echo This is a simple and wasteful but hopefully foolproof build script.
echo After running this for the first time, you can rebuild with just
echo "abld build armi urel" or "abld build wins udeb".
echo *******************************************************************

call bldmake clean
call bldmake bldfiles
call abld reallyclean
call abld build armi urel
call abld freeze
call abld build armi urel
call abld build wins udeb
call abld freeze
call abld build wins udeb
