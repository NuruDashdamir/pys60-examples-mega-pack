#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# cmd_mergesis.py - Ensymble command line tool, mergesis command
# Copyright 2006, 2007 Jussi Ylänen
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
import getpass
import locale

import sisfile
import sisfield
import cryptutil


##############################################################################
# Help texts
##############################################################################

shorthelp = 'Merge several SIS packages into one'
longhelp  = '''mergesis
    [--cert=mycert.cer] [--privkey=mykey.key] [--passphrase=12345]
    [--encoding=terminal,filesystem] [--verbose]
    <infile> [mergefile]... <outfile>

Merge several SIS packages into one and sign the resulting SIS file with
the certificate provided. The first SIS file is used as the base file and
the remaining SIS files are added as unconditional embedded SIS files
into it. Any signatures present in the first SIS file are stripped.

Options:
    infile      - Path of the base SIS file
    mergefile   - Path of SIS file(s) to add to the base SIS file
    outfile     - Path of the resulting SIS file
    cert        - Certificate to use for signing (PEM format)
    privkey     - Private key of the certificate (PEM format)
    passphrase  - Pass phrase of the private key (insecure, use stdin instead)
    encoding    - Local character encodings for terminal and filesystem
    verbose     - Print extra statistics

Merging SIS files that already contain other SIS files is not supported.
'''


##############################################################################
# Parameters
##############################################################################

MAXPASSPHRASELENGTH     = 256
MAXCERTIFICATELENGTH    = 65536
MAXPRIVATEKEYLENGTH     = 65536
MAXSISFILESIZE          = 1024 * 1024 * 8   # Eight megabytes


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
    short_opts = "a:k:p:e:vh"
    long_opts = [
        "cert=", "privkey=", "passphrase=",
        "encoding=", "verbose", "debug", "help"
    ]
    args = gopt(argv, short_opts, long_opts)

    opts = dict(args[0])
    pargs = args[1]

    if len(pargs) < 2:
        raise ValueError("wrong number of arguments")

    # Override character encoding of command line and filesystem.
    encs = opts.get("--encoding", opts.get("-e", "%s,%s" % (terminalenc,
                                                            filesystemenc)))
    try:
        terminalenc, filesystemenc = encs.split(",")
    except (ValueError, TypeError):
        raise ValueError("invalid encoding string '%s'" % encs)

    # Get input SIS file names.
    infiles = [f.decode(terminalenc).encode(filesystemenc) for f in pargs[:-1]]

    # Determine output SIS file name.
    outfile = pargs[-1].decode(terminalenc).encode(filesystemenc)
    if os.path.isdir(outfile):
        # Output to directory, use input file name.
        outfile = os.path.join(outfile, os.path.basename(infiles[0]))

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
        cryptutil.setdebug(True)

    # Ingredients for successful SIS generation:
    #
    # terminalenc          Terminal character encoding (autodetected)
    # filesystemenc        File system name encoding (autodetected)
    # infiles              A list of input SIS file names, filesystemenc encoded
    # outfile              Output SIS file name, filesystemenc encoded
    # cert                 Certificate in PEM format
    # privkey              Certificate private key in PEM format
    # passphrase           Pass phrase of priv. key, terminalenc encoded string
    # verbose              Boolean indicating verbose terminal output

    if verbose:
        print
        print "Input SIS files   %s"        % " ".join(
            [f.decode(filesystemenc).encode(terminalenc) for f in infiles])
        print "Output SIS file   %s"        % (
            outfile.decode(filesystemenc).encode(terminalenc))
        print "Certificate       %s"        % ((cert and
            cert.decode(filesystemenc).encode(terminalenc)) or "<default>")
        print "Private key       %s"        % ((privkey and
            privkey.decode(filesystemenc).encode(terminalenc)) or "<default>")
        print

    insis = []
    for n in xrange(len(infiles)):
        # Read input SIS files.
        f = file(infiles[n], "rb")
        instring = f.read(MAXSISFILESIZE + 1)
        f.close()

        if len(instring) > MAXSISFILESIZE:
            raise ValueError("%s: input SIS file too large" % infiles[n])

        if n == 0:
            # Store UIDs for later use.
            uids = instring[:16]    # UID1, UID2, UID3 and UIDCRC

        # Convert input SIS file to SISFields.
        sf, rlen = sisfield.SISField(instring[16:], False)

        # Ignore extra bytes after SIS file.
        if len(instring) > (rlen + 16):
            print ("%s: %s: warning: %d extra bytes after SIS file (ignored)" %
                   (pgmname, infiles[n], (len(instring) - (rlen + 16))))

        # Try to release some memory early.
        del instring

        # Check that there are no embedded SIS files.
        if len(sf.Data.DataUnits) > 1:
            raise ValueError("%s: input SIS file contains "
                             "embedded SIS files" % infiles[n])

        insis.append(sf)

    # Temporarily remove the SISDataIndex SISField from the first SISController.
    ctrlfield = insis[0].Controller.Data
    didxfield = ctrlfield.DataIndex
    ctrlfield.DataIndex = None

    # Remove old signatures from the first SIS file.
    if len(ctrlfield.getsignatures()) > 0:
        print ("%s: warning: removing old signatures "
               "from the first input SIS file" % pgmname)
        ctrlfield.setsignatures([])

    for n in xrange(1, len(insis)):
        # Append SISDataUnit SISFields into SISData array of the first SIS file.
        insis[0].Data.DataUnits.append(insis[n].Data.DataUnits[0])

        # Set data index in SISController SISField.
        insis[n].Controller.Data.DataIndex.DataIndex = n

        # Embed SISController into SISInstallBlock of the first SIS file.
        ctrlfield.InstallBlock.EmbeddedSISFiles.append(insis[n].Controller.Data)

    # Calculate a signature of the modified SISController.
    string = ctrlfield.tostring()
    string = sisfield.stripheaderandpadding(string)
    signature, algoid = sisfile.signstring(privkeydata, passphrase, string)

    # Create a SISCertificateChain SISField from certificate data.
    sf1 = sisfield.SISBlob(Data = cryptutil.certtobinary(certdata))
    sf2 = sisfield.SISCertificateChain(CertificateData = sf1)

    # Create a SISSignature SISField from calculated signature.
    sf3 = sisfield.SISString(String = algoid)
    sf4 = sisfield.SISSignatureAlgorithm(AlgorithmIdentifier = sf3)
    sf5 = sisfield.SISBlob(Data = signature)
    sf6 = sisfield.SISSignature(SignatureAlgorithm = sf4, SignatureData = sf5)

    # Create a new SISSignatureCertificateChain SISField.
    sa  = sisfield.SISArray(SISFields = [sf6])
    sf7 = sisfield.SISSignatureCertificateChain(Signatures = sa,
                                                CertificateChain = sf2)

    # Set certificate, restore data index.
    ctrlfield.Signature0 = sf7
    ctrlfield.DataIndex = didxfield

    # Convert SISFields to string.
    outstring = insis[0].tostring()

    # Write output SIS file.
    f = file(outfile, "wb")
    f.write(uids)
    f.write(outstring)
    f.close()
