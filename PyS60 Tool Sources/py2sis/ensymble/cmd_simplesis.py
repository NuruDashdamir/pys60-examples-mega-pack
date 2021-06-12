#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# cmd_simplesis.py - Ensymble command line tool, simplesis command
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
import re
import getopt
import getpass
import locale
import struct
import zlib

import sisfile
import sisfield
import symbianutil
import rscfile
import miffile


##############################################################################
# Help texts
##############################################################################

shorthelp = 'Create a SIS package from a directory structure'
longhelp  = '''simplesis
    [--uid=0x01234567] [--version=1.0.0] [--lang=EN,...]
    [--caption="Package Name",...] [--drive=C] [--textfile=mytext_%C.txt]
    [--cert=mycert.cer] [--privkey=mykey.key] [--passphrase=12345]
    [--vendor="Vendor Name",...] [--encoding=terminal,filesystem]
    [--verbose]
    <srcdir> [sisfile]

Create a SIS package from a directory structure. Only supports very
simple SIS files. There is no support for conditionally included
files, dependencies etc.

Options:
    srcdir       - Source directory
    sisfile      - Path of the created SIS file
    uid          - Symbian OS UID for the SIS package
    version      - SIS package version: X.Y.Z or X,Y,Z (major, minor, build)
    lang         - Comma separated list of two-character language codes
    caption      - Comma separated list of package names in all languages
    drive        - Drive where the package will be installed (any by default)
    textfile     - Text file (or pattern, see below) to display during install
    cert         - Certificate to use for signing (PEM format)
    privkey      - Private key of the certificate (PEM format)
    passphrase   - Pass phrase of the private key (insecure, use stdin instead)
    vendor       - Vendor name or a comma separated list of names in all lang.
    encoding     - Local character encodings for terminal and filesystem
    verbose      - Print extra statistics

If no certificate and its private key are given, a default self-signed
certificate is used to sign the SIS file. Software authors are encouraged
to create their own unique certificates for SIS packages that are to be
distributed.

Text to display uses UTF-8 encoding. The file name may contain formatting
characters that are substituted for each selected language. If no formatting
characters are present, the same text will be used for all languages.

    %%           - literal %
    %n           - language number (01 - 99)
    %c           - two-character language code in lowercase letters
    %C           - two-character language code in capital letters
    %l           - language name in English, using only lowercase letters
    %l           - language name in English, using mixed case letters
'''


##############################################################################
# Parameters
##############################################################################

MAXPASSPHRASELENGTH     = 256
MAXCERTIFICATELENGTH    = 65536
MAXPRIVATEKEYLENGTH     = 65536
MAXFILESIZE             = 1024 * 1024 * 8   # Eight megabytes
MAXTEXTFILELENGTH       = 1024


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
    short_opts = "u:r:l:c:f:t:a:k:p:d:e:vh"
    long_opts = [
        "uid=", "version=", "lang=", "caption=",
        "drive=", "textfile=", "cert=", "privkey=", "passphrase=", "vendor=",
        "encoding=", "verbose", "debug", "help"
    ]
    args = gopt(argv, short_opts, long_opts)

    opts = dict(args[0])
    pargs = args[1]

    if len(pargs) == 0:
        raise ValueError("no source file name given")

    # Override character encoding of command line and filesystem.
    encs = opts.get("--encoding", opts.get("-e", "%s,%s" % (terminalenc,
                                                            filesystemenc)))
    try:
        terminalenc, filesystemenc = encs.split(",")
    except (ValueError, TypeError):
        raise ValueError("invalid encoding string '%s'" % encs)

    # Get source directory name.
    src = pargs[0].decode(terminalenc).encode(filesystemenc)
    if os.path.isdir(src):
        # Remove trailing slashes (or whatever the separator is).
        src = os.path.split(src + os.sep)[0]

        # Use last directory component as the name.
        basename = os.path.basename(src)

        # Source is a directory, recursively collect files it contains.
        srcdir = src
        srcfiles = []
        prefixlen = len(srcdir) + len(os.sep)
        def getfiles(arg, dirname, names):
            for name in names:
                path = os.path.join(dirname, name)
                if not os.path.isdir(path):
                    arg.append(path[prefixlen:])
        os.path.walk(srcdir, getfiles, srcfiles)
    else:
        raise ValueError("%s: not a directory" % src)

    # Parse version string, use 1.0.0 by default.
    version = opts.get("--version", opts.get("-r", None))
    if version == None:
        version = "1.0.0"
        print ("%s: warning: no package version given, "
               "using %s" % (pgmname, version))
    try:
        version = parseversion(version)
    except (ValueError, IndexError, TypeError):
        raise ValueError("invalid version string '%s'" % version)

    # Determine output SIS file name.
    if len(pargs) == 1:
        # Derive output file name from input file name.
        outfile = "%s_v%d_%d_%d.sis" % (basename, version[0],
                                        version[1], version[2])
    elif len(pargs) == 2:
        outfile = pargs[1].decode(terminalenc).encode(filesystemenc)
        if os.path.isdir(outfile):
            # Output to directory, derive output name from input file name.
            outfile = os.path.join(outfile, "%s_v%d_%d_%d.sis" % (
                basename, version[0], version[1], version[2]))
        if not outfile.lower().endswith(".sis"):
            outfile += ".sis"
    else:
        raise ValueError("wrong number of arguments")

    # Auto-generate a test-range UID from basename.
    autouid = symbianutil.uidfromname(basename.decode(filesystemenc))

    # Get package UID.
    puid = opts.get("--uid", opts.get("-u", None))
    if puid == None:
        # No UID given, use auto-generated UID.
        puid = autouid
        print ("%s: warning: no UID given, using auto-generated "
               "test-range UID 0x%08x" % (pgmname, puid))
    elif puid.lower().startswith("0x"):
        # Prefer hex UIDs with leading "0x".
        puid = long(puid, 16)
    else:
        try:
            if len(puid) == 8:
                # Assuming hex UID even without leading "0x".
                print ('%s: warning: assuming hex UID even '
                       'without leading "0x"' % pgmname)
                puid = long(puid, 16)
            else:
                # Decimal UID.
                puid = long(puid)
                print ('%s: warning: decimal UID converted to 0x%08x' %
                       (pgmname, puid))
        except ValueError:
            raise ValueError("invalid UID string '%s'" % puid)

    # Warn against specifying a test-range UID manually.
    if puid & 0xf0000000L == 0xe0000000L and puid != autouid:
        print ("%s: warning: manually specifying a test-range UID is "
               "not recommended" % pgmname)

    # Determine package language(s), use "EN" by default.
    lang = opts.get("--lang", opts.get("-l", "EN")).split(",")
    numlang = len(lang)

    # Verify that the language codes are correct.
    for l in lang:
        try:
            symbianutil.langidtonum[l]
        except KeyError:
            raise ValueError("%s: no such language code" % l)

    # Determine package caption(s), use basename by default.
    caption = opts.get("--caption", opts.get("-c", ""))
    caption = caption.decode(terminalenc)
    if len(caption) == 0:
        # Caption not given, use basename.
        caption = [basename] * numlang
    else:
        caption = caption.split(",")

    # Compare the number of languages and captions.
    if len(caption) != numlang:
        raise ValueError("invalid number of captions")

    # Determine installation drive, any by default.
    drive = opts.get("--drive", opts.get("-f", "any")).upper()
    if drive == "ANY" or drive == "!":
        drive = "!"
    elif drive != "C" and drive != "E":
        raise ValueError("%s: invalid drive letter" % drive)

    # Determine vendor name(s), use "Ensymble" by default.
    vendor = opts.get("--vendor", opts.get("-d", "Ensymble"))
    vendor = vendor.decode(terminalenc)
    vendor = vendor.split(",")
    if len(vendor) == 1:
        # Only one vendor name given, use it for all languages.
        vendor = vendor * numlang
    elif len(vendor) != numlang:
        raise ValueError("invalid number of vendor names")

    # Load text files.
    texts = []
    textfile = opts.get("--textfile", opts.get("-t", None))
    if textfile != None:
        texts = readtextfiles(textfile, lang)

    # Get certificate and its private key file names.
    cert = opts.get("--cert", opts.get("-a", None))
    privkey = opts.get("--privkey", opts.get("-k", None))
    if cert != None and privkey != None:
        # Convert file names from terminal encoding to filesystem encoding.
        cert = cert.decode(terminalenc).encode(filesystemenc)
        privkey = privkey.decode(terminalenc).encode(filesystemenc)

        # Read certificate file.
        f = file(cert, "rb")
        certdata = f.read(MAXCERTIFICATELENGTH + 1)
        f.close()

        if len(certdata) > MAXCERTIFICATELENGTH:
            raise ValueError("certificate file too large")

        # Read private key file.
        f = file(privkey, "rb")
        privkeydata = f.read(MAXPRIVATEKEYLENGTH + 1)
        f.close()

        if len(privkeydata) > MAXPRIVATEKEYLENGTH:
            raise ValueError("private key file too large")
    elif cert == None and privkey == None:
        # No certificate given, use the Ensymble default certificate.
        # defaultcert.py is not imported when not needed. This speeds
        # up program start-up a little.
        import defaultcert
        certdata = defaultcert.cert
        privkeydata = defaultcert.privkey

        print ("%s: warning: no certificate given, using "
               "insecure built-in one" % pgmname)

        # Warn if the UID is in the protected range.
        # Resulting SIS file will probably not install.
        if puid < 0x80000000L:
            print ("%s: warning: UID is in the protected range "
                   "(0x00000000 - 0x7ffffff)" % pgmname)
    else:
        raise ValueError("missing certificate or private key")

    # Get pass phrase. Pass phrase remains in terminal encoding.
    passphrase = opts.get("--passphrase", opts.get("-p", None))
    if passphrase == None and privkey != None:
        # Private key given without "--passphrase" option, ask it.
        if sys.stdin.isatty():
            # Standard input is a TTY, ask password interactively.
            passphrase = getpass.getpass("Enter private key pass phrase:")
        else:
            # Not connected to a TTY, read stdin non-interactively instead.
            passphrase = sys.stdin.read(MAXPASSPHRASELENGTH + 1)

            if len(passphrase) > MAXPASSPHRASELENGTH:
                raise ValueError("pass phrase too long")

            passphrase = passphrase.strip()

    # Determine verbosity.
    verbose = False
    if "--verbose" in opts.keys() or "-v" in opts.keys():
        verbose = True

    # Determine if debug output is requested.
    if "--debug" in opts.keys():
        debug = True

        # Enable debug output for OpenSSL-related functions.
        import cryptutil
        cryptutil.setdebug(True)

    # Ingredients for successful SIS generation:
    #
    # terminalenc   Terminal character encoding (autodetected)
    # filesystemenc File system name encoding (autodetected)
    # basename      Base for generated file names on host, filesystemenc encoded
    # srcdir        Directory of source files, filesystemenc encoded
    # srcfiles      List of filesystemenc encoded source file names in srcdir
    # outfile       Output SIS file name, filesystemenc encoded
    # puid          Package UID, long integer
    # version       A triple-item tuple (major, minor, build)
    # lang          List of two-character language codes, ASCII strings
    # caption       List of Unicode package captions, one per language
    # drive         Installation drive letter or "!"
    # textfile      File name pattern of text file(s) to display during install
    # texts         Actual texts to display during install, one per language
    # cert          Certificate in PEM format
    # privkey       Certificate private key in PEM format
    # passphrase    Pass phrase of private key, terminalenc encoded string
    # vendor        List of Unicode vendor names, one per language
    # verbose       Boolean indicating verbose terminal output

    if verbose:
        print
        print "Input files         %s"          % " ".join(
            [s.decode(filesystemenc).encode(terminalenc) for s in srcfiles])
        print "Output SIS file     %s"          % (
            outfile.decode(filesystemenc).encode(terminalenc))
        print "UID                 0x%08x"      % puid
        print "Version             %d.%d.%d"    % (
            version[0], version[1], version[2])
        print "Language(s)         %s"          % ", ".join(lang)
        print "Package caption(s)  %s"          % ", ".join(
            [s.encode(terminalenc) for s in caption])
        print "Install drive       %s"        % ((drive == "!") and
            "<any>" or drive)
        print "Text file(s)        %s"          % ((textfile and
            textfile.decode(filesystemenc).encode(terminalenc)) or "<none>")
        print "Certificate         %s"          % ((cert and
            cert.decode(filesystemenc).encode(terminalenc)) or "<default>")
        print "Private key         %s"          % ((privkey and
            privkey.decode(filesystemenc).encode(terminalenc)) or "<default>")
        print "Vendor name(s)      %s"          % ", ".join(
            [s.encode(terminalenc) for s in vendor])
        print

    # Generate SimpleSISWriter object.
    sw = sisfile.SimpleSISWriter(lang, caption, puid, version,
                                 vendor[0], vendor)

    # Add text file or files to the SIS object. Text dialog is
    # supposed to be displayed before anything else is installed.
    if len(texts) == 1:
        sw.addfile(texts[0], operation = sisfield.EOpText)
    elif len(texts) > 1:
        sw.addlangdepfile(texts, operation = sisfield.EOpText)

    # Add files to SIS object.
    sysbinprefix = os.path.join("sys", "bin", "")
    for srcfile in srcfiles:
        # Read file.
        f = file(os.path.join(srcdir, srcfile), "rb")
        string = f.read(MAXFILESIZE + 1)
        f.close()

        if len(string) > MAXFILESIZE:
            raise ValueError("input file too large")

        # Check if the file is an E32Image (EXE or DLL).
        caps = symbianutil.e32imagecaps(string)

        if caps != None and not srcfile.startswith(sysbinprefix):
            print ("%s: warning: %s is an E32Image (EXE or DLL) outside %s%s" %
                    (pgmname, srcfile, os.sep, sysbinprefix))

        # Add file to the SIS object.
        target = srcfile.decode(filesystemenc).replace(os.sep, "\\")
        sw.addfile(string, "%s:\\%s" % (drive, target), capabilities = caps)
        del string

    # Add target device dependency.
    sw.addtargetdevice(0x101f7961L, (0, 0, 0), None,
                       ["Series60ProductID"] * numlang)

    # Add certificate.
    sw.addcertificate(privkeydata, certdata, passphrase)

    # Generate SIS file out of the SimpleSISWriter object.
    sw.tofile(outfile)


##############################################################################
# Module-level functions which are normally only used by this module
##############################################################################

def parseversion(version):
    '''Parse a version string: "v1.2.3" or similar.

    Initial "v" can optionally be a capital "V" or omitted altogether. Minor
    and build numbers can also be omitted. Separator can be a comma or a
    period.'''

    version = version.strip().lower()

    # Strip initial "v" or "V".
    if version[0] == "v":
        version = version[1:]

    if "." in version:
        parts = [int(n) for n in version.split(".")]
    else:
        parts = [int(n) for n in version.split(",")]

    # Allow missing minor and build numbers.
    parts.extend([0, 0])

    return parts[0:3]

def readtextfiles(pattern, languages):
    '''Read language dependent text files.

    Files are assumed to be in UTF-8 encoding and re-encoded
    in UCS-2 (UTF-16LE) for Symbian OS to display during installation.'''

    if "%" not in pattern:
        # Only one file, read it.
        filenames = [pattern]
    else:
        filenames = []
        for langid in languages:
            langnum  = symbianutil.langidtonum[langid]
            langname = symbianutil.langnumtoname[langnum]

            # Replace formatting characters in file name pattern.
            filename = pattern
            filename = filename.replace("%n", "%02d" % langnum)
            filename = filename.replace("%c", langid.lower())
            filename = filename.replace("%C", langid.upper())
            filename = filename.replace("%l", langname.lower())
            filename = filename.replace("%L", langname)
            filename = filename.replace("%%", "%")

            filenames.append(filename)

    texts = []

    for filename in filenames:
        f = file(filename, "r") # Read as text.
        text = f.read(MAXTEXTFILELENGTH + 1)
        f.close()

        if len(text) > MAXTEXTFILELENGTH:
            raise ValueError("%s: text file too large" % filename)

        texts.append(text.decode("UTF-8").encode("UTF-16LE"))

    return texts
