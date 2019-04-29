Python File Server
------------------

This package implements a simple file server that makes it possible to
update the files on the phone faster than by sending them over OBEX.

Disclaimer
----------

After connecting the phone to the PC, the PC has the power to execute
arbitrary code and to rewrite any file on the phone. It goes without
saying that you should connect only to targets that are known to be
safe.

Prerequisites
-------------

- PyS60 installed on phone. Any version should work.
- Cygwin version of Python 2.4 installed on the PC
- Bluetooth connectivity on the PC

Usage
-----

1. Install fileserver.py to the phone as a library, and fsgui.py as a
script.

2. Add a Bluetooth serial port to the PC. You will probably want to
have _two_ BT serial ports available: one for the file server and one
for the Bluetooth console.

3. Edit the end of fctool so it connects to the correct serial
port. /dev/ttyS4 == COM5, /dev/ttyS5 == COM6 etc.

4. Place fileclient.py into /lib/python2.4/site-packages in your Cygwin
environment, and fctool into your PATH.

5. Start fsgui.py, and select the serial port you want to use.

6. Run "fctool ping". If it says that the file server is alive, all is well.

7. Write a synchronization script. An example (dosync) is included.

Notes
-----

The fsgui.py script will store the Bluetooth address and port in the file
C:\system\apps\python\fileserver_conf.txt. If Python is installed on other
drive than C: then this file is not automatically removed when Python is
uninstalled.
