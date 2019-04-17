#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# cmd_signsis.py - Ensymble command line tool, altere32 command
# Copyright 2006, 2007, 2008 Jussi Ylänen
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

shorthelp = 'Alter the IDs and capabilities of e32image files (EXEs, DLLs)'
longhelp  = '''altere32
    [--uid=0x01234567] [--secureid=0x01234567] [--vendorid=0x01234567]
    [--caps=Cap1+Cap2+...] [--heapsize=min,max] [--inplace]
    [--encoding=terminal,filesystem] [--verbose]
    <infile> [outfile]

Alter the IDs, capabilities and heap sizes of e32image files (Symbian OS
EXEs and DLLs).

Options:
    infile      - Path of the original e32image file (or many, if --inplace set)
    outfile     - Path of the modified e32image file (not used with --inplace)
    uid         - Symbian OS UID for the e32image
    secureid    - Secure ID for the e32image (should normally be same as UID)
    vendorid    - Vendor ID for the e32image
    caps        - Capability names, separated by "+"
    heapsize    - Heap size, minimum and/or maximum (not altered by default)
    inplace     - Allow more than one input file, modify input files in-place
    encoding    - Local character encodings for terminal and filesystem
    verbose     - Print extra statistics

When modifying the UID, the secure ID should be modified accordingly.
Modifying UIDs of application EXEs is generally not possible, because
applications usually include the UID in program code as well.
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

    # Parse command line arguments.
    short_opts = "u:s:r:b:H:ie:vh"
    long_opts = [
        "uid=", "secureid=", "vendorid=", "caps=", "heapsize=",
        "inplace", "encoding=", "verbose", "debug", "help"
    ]
    args = gopt(argv, short_opts, long_opts)

    opts = dict(args[0])
    pargs = args[1]

    if len(pargs) == 0:
        raise ValueError("no input e32image file name given")

    # Override character encoding of command line and filesystem.
    encs = opts.get("--encoding", opts.get("-e", "%s,%s" % (terminalenc,
                                                            filesystemenc)))
    try:
        terminalenc, filesystemenc = encs.split(",")
    except (ValueError, TypeError):
        raise ValueError("invalid encoding string '%s'" % encs)

    # Get UID3.
    uid3 = opts.get("--uid", opts.get("-u", None))
    if uid3 != None:
        uid3 = parseuid(pgmname, uid3)

    # Get secure ID.
    secureid = opts.get("--secureid", opts.get("-s", None))
    if secureid != None:
        secureid = parseuid(pgmname, secureid)

    # Get vendor ID.
    vendorid = opts.get("--vendorid", opts.get("-r", None))
    if vendorid != None:
        vendorid = parseuid(pgmname, vendorid)

    # Get capabilities and normalize the names.
    caps = opts.get("--caps", opts.get("-b", None))
    if caps != None:
        capmask = symbianutil.capstringtomask(caps)
        caps = symbianutil.capmasktostring(capmask, True)
    else:
        capmask = None

    # Get heap sizes.
    heapsize = opts.get("--heapsize", opts.get("-H", None))
    if heapsize != None:
        try:
            heapsize = heapsize.split(",", 1)
            heapsizemin = symbianutil.parseintmagnitude(heapsize[0])
            if len(heapsize) == 1:
                # Only one size given, use it as both.
                heapsizemax = heapsizemin
            else:
                heapsizemax = symbianutil.parseintmagnitude(heapsize[1])
        except (ValueError, TypeError, IndexError):
            raise ValueError("%s: invalid heap size, one or two values expected"
                             % ",".join(heapsize))

        # Warn if the minimum heap size is larger than the maximum heap size.
        # Resulting e32image file will probably prevent any SIS from installing.
        if heapsizemin > heapsizemax:
            print ("%s: warning: minimum heap size larger than "
                   "maximum heap size" % pgmname)
    else:
        heapsizemin = None
        heapsizemax = None

    # Determine parameter format. Modifying files in-place or not.
    inplace = False
    if "--inplace" in opts.keys() or "-i" in opts.keys():
        inplace = True

    # Determine e32image input / output file names.
    files = [name.decode(terminalenc).encode(filesystemenc) for name in pargs]
    if not inplace:
        if len(files) == 2:
            if os.path.isdir(files[1]):
                # Output to directory, use input file name.
                files[1] = os.path.join(files[1], os.path.basename(files[0]))
        else:
            raise ValueError("wrong number of arguments")

    # Determine verbosity.
    verbose = False
    if "--verbose" in opts.keys() or "-v" in opts.keys():
        verbose = True

    # Determine if debug output is requested.
    if "--debug" in opts.keys():
        debug = True

    # Ingredients for successful e32image file alteration:
    #
    # terminalenc      Terminal character encoding (autodetected)
    # filesystemenc    File system name encoding (autodetected)
    # files            File names of e32image files, filesystemenc encoded
    # uid3             Application UID3, long integer or None
    # secureid         Secure ID, long integer or None
    # vendorid         Vendor ID, long integer or None
    # caps, capmask    Capability names and bitmask or None
    # heapsizemin      Heap that must be available for the app. to start or None
    # heapsizemax      Maximum amount of heap the app. can allocate or None
    # inplace          Multiple input files or single input / output pair
    # verbose          Boolean indicating verbose terminal output

    if verbose:
        print
        if not inplace:
            print "Input e32image file      %s"        % (
                files[0].decode(filesystemenc).encode(terminalenc))
            print "Output e32image file     %s"        % (
                files[1].decode(filesystemenc).encode(terminalenc))
        else:
            print "Input e32image file(s)   %s"        % " ".join(
                [f.decode(filesystemenc).encode(terminalenc) for f in files])
        if uid3 != None:
            print "UID                      0x%08x" % uid3
        else:
            print "UID                      <not set>"
        if secureid != None:
            print "Secure ID                0x%08x" % secureid
        else:
            print "Secure ID                <not set>"
        if vendorid != None:
            print "Vendor ID                0x%08x" % vendorid
        else:
            print "Vendor ID                <not set>"
        if caps != None:
            print "Capabilities             0x%x (%s)" % (capmask, caps)
        else:
            print "Capabilities             <not set>"
        if heapsizemin != None:
            print "Heap size in bytes       %d, %d" % (heapsizemin, heapsizemax)
        else:
            print "Heap size in bytes       <not set>"
        print

    if ((uid3, secureid, vendorid, caps, heapsizemin) ==
        (None, None, None, None, None)):
        print "%s: no options set, doing nothing" % pgmname
        return

    for infile in files:
        # Read input e32image file.
        f = file(infile, "rb")
        instring = f.read(MAXE32FILESIZE + 1)
        f.close()

        if len(instring) > MAXE32FILESIZE:
            raise ValueError("input e32image file too large")

        # Modify the e32image header.
        try:
            outstring = symbianutil.e32imagecrc(instring, uid3,
                                                secureid, vendorid, heapsizemin,
                                                heapsizemax, capmask)
        except ValueError:
            raise ValueError("%s: not a valid e32image file" % infile)

        if not inplace:
            outfile = files[1]
        else:
            outfile = infile

        # Write output e32image file.
        f = file(outfile, "wb")
        f.write(outstring)
        f.close()

        if not inplace:
            # While --inplace is not in effect, files[1] is the output
            # file name, so must stop after one iteration.
            break


##############################################################################
# Module-level functions which are normally only used by this module
##############################################################################

def parseuid(pgmname, uid):
    if uid.lower().startswith("0x"):
        # Prefer hex UIDs with leading "0x".
        uid = long(uid, 16)
    else:
        try:
            if len(uid) == 8:
                # Assuming hex UID even without leading "0x".
                print ('%s: warning: assuming hex UID even '
                       'without leading "0x"' % pgmname)
                uid = long(uid, 16)
            else:
                # Decimal UID.
                uid = long(uid)
                print ('%s: warning: decimal UID converted to 0x%08x' %
                       (pgmname, uid))
        except ValueError:
            raise ValueError("invalid UID string '%s'" % uid)
    return uid
