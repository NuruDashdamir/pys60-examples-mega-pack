
Ensymble for PyS60 1.9.x
=========================
This is a modified version of ensymble for "Python for S60" that can be 
downloaded from http://www.nbl.fi/~nbl928/ensymble.html.

This creates a sis package for PyS60 1.9.x.


Creating sis files with ensymble.py
===================================
Read ensymble-0.26/README or read the help message shown by ensymble.py.

NOTE: To execute ensymble.py on windows, download openssl.zip from here http://www.stunnel.org/download/binaries.html and extract the contents to 
the directory in which ensymble.py is placed. Installing stunnel-x.exe 
(available from the same link) may also be required.


Steps to create ensymble.py with a new stub exe
===============================================

1. Compile the source under python25-stub for 'armv5 urel' to produce the 
   stub exe.

2. Update the execstubdata variable in ensymble-0.26/cmd_py2sis.py with the 
   base-64-encoded form of stub exe.

3. Execute ensymble-0.26/install.sh to get a squeezed version of the tool.
