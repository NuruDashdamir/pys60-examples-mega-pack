#!/usr/bin/env python
# -*- coding: iso8859-1 -*-

##############################################################################
# cmd_genuid.py - Ensymble command line tool, genuid command
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

shorthelp = 'Generate a new test-range UID from a name'
longhelp  = '''genuid
    [--encoding=terminal,filesystem] [--verbose]
    <name>...

Generate a new test-range UID from a name.

Options:
    name        - Name used for UID generation
    encoding    - Local character encodings for terminal and filesystem
    verbose     - Not used

Generated UID is compatible with the automatic UID generation of py2sis
and simplesis commands. The name must not contain version information or
any file prefixes, just the name itself, e.g. "mymodule" instead of
"mymodule_v1.2.3.sis".
'''


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
        raise ValueError("no name given")

    # Override character encoding of command line and filesystem.
    encs = opts.get("--encoding", opts.get("-e", "%s,%s" % (terminalenc,
                                                            filesystemenc)))
    try:
        terminalenc, filesystemenc = encs.split(",")
    except (ValueError, TypeError):
        raise ValueError("invalid encoding string '%s'" % encs)

    # Convert name(s) to Unicode.
    names = [name.decode(terminalenc) for name in pargs]

    # Determine verbosity.
    verbose = False
    if "--verbose" in opts.keys() or "-v" in opts.keys():
        verbose = True

    # Determine if debug output is requested.
    if "--debug" in opts.keys():
        debug = True

    # Ingredients for successful UID generation:
    #
    # terminalenc          Terminal character encoding (autodetected)
    # filesystemenc        File system name encoding (autodetected)
    # names                Names to generate the UID from, filesystemenc encoded
    # verbose              Boolean indicating verbose terminal output (no-op)

    for name in names:
        # Auto-generate a test-range UID from name.
        autouid = symbianutil.uidfromname(name)

        print "%s: 0x%08x" % (name.decode(filesystemenc).encode(terminalenc),
                              autouid)
