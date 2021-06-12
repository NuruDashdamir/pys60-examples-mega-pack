#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# cmd_signsis.py - Ensymble command line tool, signsis command
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
import getpass
import locale
import struct
import sha

import sisfile
import sisfield
import symbianutil
import cryptutil


##############################################################################
# Help texts
##############################################################################

shorthelp = 'Sign a SIS package'
longhelp  = '''signsis
    [--unsign] [--cert=mycert.cer] [--privkey=mykey.key] [--passphrase=12345]
    [--execaps=Cap1+Cap2+...] [--dllcaps=Cap1+Cap2+...]
    [--encoding=terminal,filesystem] [--verbose]
    <infile> [outfile]

Sign a SIS file with the certificate provided (stripping out any
existing certificates, if any). Optionally modify capabilities of
all EXE and DLL files contained in the SIS package.

Options:
    infile      - Path of the original SIS file
    outfile     - Path of the signed SIS file (or the original is overwritten)
    unsign      - Remove all signatures from SIS file instead of signing
    cert        - Certificate to use for signing (PEM format)
    privkey     - Private key of the certificate (PEM format)
    passphrase  - Pass phrase of the private key (insecure, use stdin instead)
    execaps     - Capability names, separated by "+" (not altered by default)
    dllcaps     - Capability names, separated by "+" (not altered by default)
    encoding    - Local character encodings for terminal and filesystem
    verbose     - Print extra statistics

If no certificate and its private key are given, a default self-signed
certificate is used to sign the SIS file. Software authors are encouraged
to create their own unique certificates for SIS packages that are to be
distributed.

Embedded SIS files are ignored, i.e their certificates are not modified.
Also, capabilities of EXE and DLL files inside embedded SIS files are
not affected.
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
    short_opts = "ua:k:p:b:d:e:vh"
    long_opts = [
        "unsign", "cert=", "privkey=", "passphrase=", "execaps=",
        "dllcaps=", "encoding=", "verbose", "debug", "help"
    ]
    args = gopt(argv, short_opts, long_opts)

    opts = dict(args[0])
    pargs = args[1]

    if len(pargs) == 0:
        raise ValueError("no SIS file name given")

    # Override character encoding of command line and filesystem.
    encs = opts.get("--encoding", opts.get("-e", "%s,%s" % (terminalenc,
                                                            filesystemenc)))
    try:
        terminalenc, filesystemenc = encs.split(",")
    except (ValueError, TypeError):
        raise ValueError("invalid encoding string '%s'" % encs)

    # Get input SIS file name.
    infile = pargs[0].decode(terminalenc).encode(filesystemenc)

    # Determine output SIS file name.
    if len(pargs) == 1:
        # No output file, overwrite original SIS file.
        outfile = infile
    elif len(pargs) == 2:
        outfile = pargs[1].decode(terminalenc).encode(filesystemenc)
        if os.path.isdir(outfile):
            # Output to directory, use input file name.
            outfile = os.path.join(outfile, os.path.basename(infile))
    else:
        raise ValueError("wrong number of arguments")

    # Get unsign option.
    unsign = False
    if "--unsign" in opts.keys() or "-u" in opts.keys():
        unsign = True

    # Get certificate and its private key file names.
    cert = opts.get("--cert", opts.get("-a", None))
    privkey = opts.get("--privkey", opts.get("-k", None))
    if unsign:
        if cert != None or privkey != None:
            raise ValueError("certificate or private key given when unsigning")
    elif cert != None and privkey != None:
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

    # Get EXE capabilities and normalize the names.
    execaps = opts.get("--execaps", opts.get("-b", None))
    if execaps != None:
        execapmask = symbianutil.capstringtomask(execaps)
        execaps = symbianutil.capmasktostring(execapmask, True)
    else:
        execapmask = None

    # Get DLL capabilities and normalize the names.
    dllcaps = opts.get("--dllcaps", opts.get("-d", None))
    if dllcaps != None:
        dllcapmask = symbianutil.capstringtomask(dllcaps)
        dllcaps = symbianutil.capmasktostring(dllcapmask, True)
    else:
        dllcapmask = None

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
    # infile               Input SIS file name, filesystemenc encoded
    # outfile              Output SIS file name, filesystemenc encoded
    # cert                 Certificate in PEM format
    # privkey              Certificate private key in PEM format
    # passphrase           Pass phrase of priv. key, terminalenc encoded string
    # execaps, execapmask  Capability names and bitmask for EXE files or None
    # dllcaps, dllcapmask  Capability names and bitmask for DLL files or None
    # verbose              Boolean indicating verbose terminal output

    if verbose:
        print
        print "Input SIS file    %s"        % (
            infile.decode(filesystemenc).encode(terminalenc))
        print "Output SIS file   %s"        % (
            outfile.decode(filesystemenc).encode(terminalenc))
        if unsign:
            print "Remove signatures Yes"
        else:
            print "Certificate       %s"        % ((cert and
                cert.decode(filesystemenc).encode(terminalenc)) or
                            "<default>")
            print "Private key       %s"        % ((privkey and
                privkey.decode(filesystemenc).encode(terminalenc)) or
                               "<default>")
        if execaps != None:
            print "EXE capabilities  0x%x (%s)" % (execapmask, execaps)
        else:
            print "EXE capabilities  <not set>"
        if dllcaps != None:
            print "DLL capabilities  0x%x (%s)" % (dllcapmask, dllcaps)
        else:
            print "DLL capabilities  <not set>"
        print

    # Read input SIS file.
    f = file(infile, "rb")
    instring = f.read(MAXSISFILESIZE + 1)
    f.close()

    if len(instring) > MAXSISFILESIZE:
        raise ValueError("input SIS file too large")

    # Convert input SIS file to SISFields.
    uids = instring[:16]    # UID1, UID2, UID3 and UIDCRC
    insis, rlen = sisfield.SISField(instring[16:], False)

    # Ignore extra bytes after SIS file.
    if len(instring) > (rlen + 16):
        print ("%s: warning: %d extra bytes after input SIS file (ignored)" %
               (pgmname, (len(instring) - (rlen + 16))))

    # Try to release some memory early.
    del instring

    # Check if there are embedded SIS files. Warn if there are.
    if len(insis.Data.DataUnits) > 1:
        print ("%s: warning: input SIS file contains "
               "embedded SIS files (ignored)" % pgmname)

    # Modify EXE- and DLL-files according to new capabilities.
    if execaps != None or dllcaps != None:
        # Generate FileIndex to SISFileDescription mapping.
        sisfiledescmap = mapfiledesc(insis.Controller.Data.InstallBlock)

        exemods, dllmods = modifycaps(insis, sisfiledescmap,
                                      execapmask, dllcapmask)
        print ("%s: %d EXE-files will be modified, "
               "%d DLL-files will be modified" % (pgmname, exemods, dllmods))

    # Temporarily remove the SISDataIndex SISField from SISController.
    ctrlfield = insis.Controller.Data
    didxfield = ctrlfield.DataIndex
    ctrlfield.DataIndex = None

    if not unsign:
        # Remove old signatures.
        if len(ctrlfield.getsignatures()) > 0:
            print ("%s: warning: removing old signatures "
                   "from input SIS file" % pgmname)
            ctrlfield.setsignatures([])

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
        sf6 = sisfield.SISSignature(SignatureAlgorithm = sf4,
                                    SignatureData = sf5)

        # Create a new SISSignatureCertificateChain SISField.
        sa  = sisfield.SISArray(SISFields = [sf6])
        sf7 = sisfield.SISSignatureCertificateChain(Signatures = sa,
                                                    CertificateChain = sf2)

        # Set new certificate.
        ctrlfield.Signature0 = sf7
    else:
        # Unsign, remove old signatures.
        ctrlfield.setsignatures([])

    # Restore data index.
    ctrlfield.DataIndex = didxfield

    # Convert SISFields to string.
    outstring = insis.tostring()

    # Write output SIS file.
    f = file(outfile, "wb")
    f.write(uids)
    f.write(outstring)
    f.close()


##############################################################################
# Module-level functions which are normally only used by this module
##############################################################################

def modifycaps(siscontents, sisfiledescmap, execapmask, dllcapmask):
    '''Scan SISData SISFields for EXE- and DLL-files
    and modify their headers for the new capabilities.'''

    # Prepare UID1 strings for EXE and DLL.
    exeuids = struct.pack("<L", 0x1000007AL)
    dlluids = struct.pack("<L", 0x10000079L)

    exemods = 0
    dllmods = 0

    # Only examine the first SISDataUnit. Ignore embedded SIS files.
    sisfiledata = siscontents.Data.DataUnits[0].FileData

    for fileindex in xrange(len(sisfiledata)):
        capmask = None

        # Get file contents (uncompressed).
        contents = sisfiledata[fileindex].FileData.Data

        # Determine file type.
        if execapmask != None and contents[:4] == exeuids:
            capmask = execapmask
            exemods += 1
        elif dllcapmask != None and contents[:4] == dlluids:
            capmask = dllcapmask
            dllmods += 1

        if capmask != None:
            # Modify capabilities contained in the E32Image header.
            contents = symbianutil.e32imagecrc(contents, capabilities = capmask)

            # Replace file contents.
            sisfiledata[fileindex].FileData.Data = contents

            # Find the SISFileDescription SISField for this file index.
            try:
                sisfiledesc = sisfiledescmap[fileindex]
            except KeyError:
                # No file index found, SIS file is probably corrupted.
                raise ValueError("missing file metadata in input SIS file")

            # Set new capabilities in the SISFileDescription SISField.
            if capmask != 0:
                capstring = symbianutil.capmasktorawdata(capmask)
                capfield = sisfield.SISCapabilities(Capabilities = capstring)
                sisfiledesc.Capabilities = capfield
            else:
                # If capability mask is 0, no capability field is generated.
                # Otherwise the original signsis.exe from Symbian cannot
                # sign the resulting SIS file.
                sisfiledesc.Capabilities = None

            # Re-calculate file hash in the SISFileDescription SISField.
            sha1hash = sha.new(contents).digest()
            hashblob = sisfield.SISBlob(Data = sha1hash)
            hashfield = sisfield.SISHash(HashAlgorithm =
                                         sisfield.ESISHashAlgSHA1,
                                         HashData = hashblob)
            sisfiledesc.Hash = hashfield

            if debug:
                # Print target names of modified files.
                print sisfiledesc.Target.String

    return (exemods, dllmods)

def mapfiledesc(sisinstallblock, sisfiledescmap = {}):
    '''Recursively scan SISInstallBlocks for file indexes in
    SISFileDescription SISFields.'''

    # First add normal files to SISFileDescription file index map.
    for filedesc in sisinstallblock.Files:
        idx = filedesc.FileIndex
        if idx in sisfiledescmap.keys():
            # In theory, SIS files could re-use file data by using the
            # same file index in more than one place. This special case
            # is not supported, for now.
            raise ValueError("duplicate file index in input SIS file")
        sisfiledescmap[idx] = filedesc

    # Then, recursively call mapfiledesc() for SISIf and SISElseIf SISArrays.
    for sisif in sisinstallblock.IfBlocks:
        mapfiledesc(sisif.InstallBlock, sisfiledescmap) # Map modified in-place.

        for siselseif in sisif.ElseIfs:
            mapfiledesc(siselseif.InstallBlock, sisfiledescmap)

    return sisfiledescmap
