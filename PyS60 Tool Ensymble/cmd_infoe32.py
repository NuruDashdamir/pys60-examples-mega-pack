#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# cmd_infoe32.py - Ensymble command line tool, infoe32 command
# Copyright 2006, 2007, 2008, 2009 Jussi Ylänen
#
# This file is part of Ensymble developer utilities for Symbian OS(TM).
#
# Ensymble is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ensymble is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ensymble; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
##############################################################################

import sys
import os
import getopt
import locale
import struct

import symbianutil


##############################################################################
# Help texts
##############################################################################

shorthelp = 'Show the IDs and capabilities of e32image files (EXEs, DLLs)'
longhelp  = '''infoe32
    [--encoding=terminal,filesystem] [--verbose]
    <infile>...

Show the IDs and capabilities of e32image files (Symbian OS EXEs and DLLs).

Options:
    infile      - Path of the e32image file/files
    encoding    - Local character encodings for terminal and filesystem
    verbose     - Not used
'''


##############################################################################
# Parameters
##############################################################################

MAXE32FILESIZE  = 1024 * 1024 * 8   # Eight megabytes


##############################################################################
# Global variables
##############################################################################

debug = False


##############################################################################
# Public module-level functions
##############################################################################

def run(pgmname, argv):
    global debug

    # Determine system character encodings.
    try:
        # getdefaultlocale() may sometimes return None.
        # Fall back to ASCII encoding in that case.
        terminalenc = locale.getdefaultlocale()[1] + ""
    except TypeError:
        # Invalid locale, fall back to ASCII terminal encoding.
        terminalenc = "ascii"

    try:
        # sys.getfilesystemencoding() was introduced in Python v2.3 and
        # it can sometimes return None. Fall back to ASCII if something
        # goes wrong.
        filesystemenc = sys.getfilesystemencoding() + ""
    except (AttributeError, TypeError):
        filesystemenc = "ascii"

    try:
        gopt = getopt.gnu_getopt
    except:
        # Python <v2.3, GNU-style parameter ordering not supported.
        gopt = getopt.getopt

    short_opts = "e:vh"
    long_opts = [
        "encoding=", "verbose", "debug", "help"
    ]
    args = gopt(argv, short_opts, long_opts)

    opts = dict(args[0])
    pargs = args[1]

    if len(pargs) == 0:
        raise ValueError("no e32image file name given")

    # Override character encoding of command line and filesystem.
    encs = opts.get("--encoding", opts.get("-e", "%s,%s" % (terminalenc,
                                                            filesystemenc)))
    try:
        terminalenc, filesystemenc = encs.split(",")
    except (ValueError, TypeError):
        raise ValueError("invalid encoding string '%s'" % encs)

    # Determine e32image file name(s).
    files = [name.decode(terminalenc).encode(filesystemenc) for name in pargs]

    # Determine verbosity.
    verbose = False
    if "--verbose" in opts.keys() or "-v" in opts.keys():
        verbose = True

    # Determine if debug output is requested.
    if "--debug" in opts.keys():
        debug = True

    # Ingredients for successful e32image inspection:
    #
    # terminalenc          Terminal character encoding (autodetected)
    # filesystemenc        File system name encoding (autodetected)
    # files                File names of e32image files, filesystemenc encoded
    # verbose              Boolean indicating verbose terminal output (no-op)

    for infile in files:
        # Read input e32image file.
        f = file(infile, "rb")
        instring = f.read(MAXE32FILESIZE + 1)
        f.close()

        if len(instring) > MAXE32FILESIZE:
            raise ValueError("input e32image file too large")

        # Get info about the e32image
        try:
            (uid1, uid2, uid3,
             sid, vid, capmask) = symbianutil.e32imageinfo(instring)
            caps = symbianutil.capmasktostring(capmask, True)

            print "%s:" % infile
            print "    UID1          0x%08x" % uid1
            print "    UID2          0x%08x" % uid2
            print "    UID3          0x%08x" % uid3
            print "    Secure ID     0x%08x" % sid
            print "    Vendor ID     0x%08x" % vid
            print "    Capabilities  0x%x (%s)" % (capmask, caps)
        except ValueError:
            raise ValueError("%s: not a valid e32image file" % infile)
