@echo off
echo *******************************************************************
echo This is a simple and wasteful but hopefully foolproof build script.
echo After running this for the first time, you can rebuild with just
echo "abld build armv5 urel" or "abld build winscw udeb".
echo *******************************************************************

call bldmake clean
call bldmake bldfiles
call abld reallyclean
call abld build gcce urel
call abld freeze
call abld build gcce urel
call abld build winscw udeb
call abld freeze
call abld build winscw udeb
