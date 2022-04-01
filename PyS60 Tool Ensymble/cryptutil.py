#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# cryptutil.py - OpenSSL command line utility wrappers for Ensymble
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
import errno
import tempfile
import random


opensslcommand = None   # Path to OpenSSL command line tool
openssldebug   = False  # True for extra debug output


##############################################################################
# Public module-level functions
##############################################################################

def setdebug(active):
    '''
    Activate or deactivate debug output.

    setdebug(...) -> None

    active      Debug output enabled / disabled, a boolean value

    Debug output consists of OpenSSL binary command line and
    any output produced to the standard error stream by OpenSSL.
    '''

    global openssldebug
    openssldebug =  not not active  # Convert to boolean.

def signstring(privkey, passphrase, string):
    '''
    Sign a binary string using a given private key and its pass phrase.

    signstring(...) -> (signature, keytype)

    privkey     RSA or DSA private key, a string in PEM (base-64) format
    passphrase  pass phrase for the private key, a non-Unicode string or None
    string      a binary string to sign

    signature   signature, an ASN.1 encoded binary string
    keytype     detected key type, string, "RSA" or "DSA"

    NOTE: On platforms with poor file system security, decrypted version
    of the private key may be grabbed from the temporary directory!
    '''

    if passphrase == None or len(passphrase) == 0:
        # OpenSSL does not like empty stdin while reading a passphrase from it.
        passphrase = "\n"

    # Create a temporary directory for OpenSSL to work in.
    tempdir = mkdtemp("ensymble-XXXXXX")

    keyfilename     = os.path.join(tempdir, "privkey.pem")
    sigfilename     = os.path.join(tempdir, "signature.dat")
    stringfilename  = os.path.join(tempdir, "string.dat")

    try:
        # If the private key is in PKCS#8 format, it needs to be converted.
        privkey = convertpkcs8key(tempdir, privkey, passphrase)

        # Decrypt the private key. Older versions of OpenSSL do not
        # accept the "-passin" parameter for the "dgst" command.
        privkey, keytype = decryptkey(tempdir, privkey, passphrase)

        if keytype == "DSA":
            signcmd = "-dss1"
        elif keytype == "RSA":
            signcmd = "-sha1"
        else:
            raise ValueError("unknown private key type %s" % keytype)

        # Write decrypted PEM format private key to file.
        keyfile = file(keyfilename, "wb")
        keyfile.write(privkey)
        keyfile.close()

        # Write binary string to a file. On some systems, stdin is
        # always in text mode and thus unsuitable for binary data.
        stringfile = file(stringfilename, "wb")
        stringfile.write(string)
        stringfile.close()

        # Sign binary string using the decrypted private key.
        command = ("dgst %s -binary -sign %s "
                   "-out %s %s") % (signcmd, quote(keyfilename),
                                    quote(sigfilename), quote(stringfilename))
        runopenssl(command)

        signature = ""
        if os.path.isfile(sigfilename):
            # Read signature from file.
            sigfile = file(sigfilename, "rb")
            signature = sigfile.read()
            sigfile.close()

        if signature.strip() == "":
            # OpenSSL did not create output, something went wrong.
            raise ValueError("unspecified error during signing")
    finally:
        # Delete temporary files.
        for fname in (keyfilename, sigfilename, stringfilename):
            try:
                os.remove(fname)
            except OSError:
               pass

        # Remove temporary directory.
        os.rmdir(tempdir)

    return (signature, keytype)


def certtobinary(pemcert):
    '''
    Convert X.509 certificates from PEM (base-64) format to DER (binary).

    certtobinary(...) -> dercert

    pemcert     One or more X.509 certificates in PEM (base-64) format, a string

    dercert     X.509 certificate(s), an ASN.1 encoded binary string
    '''

    # Find base-64 encoded data between header and footer.
    header = "-----BEGIN CERTIFICATE-----"
    footer = "-----END CERTIFICATE-----"
    endoffset = 0
    certs = []
    while True:
        # First find a header.
        startoffset = pemcert.find(header, endoffset)
        if startoffset < 0:
            # No header found, stop search.
            break

        startoffset += len(header)

        # Next find a footer.
        endoffset = pemcert.find(footer, startoffset)
        if endoffset < 0:
            # No footer found.
            raise ValueError("missing PEM certificate footer")

        # Extract the base-64 encoded certificate and decode it.
        try:
            cert = pemcert[startoffset:endoffset].decode("base-64")
        except:
            # Base-64 decoding error.
            raise ValueError("invalid PEM format certificate")

        certs.append(cert)

        endoffset += len(footer)

    if len(certs) == 0:
        raise ValueError("not a PEM format certificate")

    # DER certificates are simply raw binary versions
    # of the base-64 encoded PEM certificates.
    return "".join(certs)


##############################################################################
# Module-level functions which are normally only used by this module
##############################################################################

def convertpkcs8key(tempdir, privkey, passphrase):
    '''
    Convert a PKCS#8-format RSA or DSA private key to an older
    SSLeay-compatible format.

    convertpkcs8key(...) -> privkeyout

    tempdir     Path to pre-existing temporary directory with read/write access
    privkey     RSA or DSA private key, a string in PEM (base-64) format
    passphrase  pass phrase for the private key, a non-Unicode string or None

    privkeyout  decrypted private key in PEM (base-64) format
    '''

    # Determine PKCS#8 private key type.
    if privkey.find("-----BEGIN PRIVATE KEY-----") >= 0:
        # Unencrypted PKCS#8 private key
        encryptcmd = "-nocrypt"
    elif privkey.find("-----BEGIN ENCRYPTED PRIVATE KEY-----") >= 0:
        # Encrypted PKCS#8 private key
        encryptcmd = ""
    else:
        # Not a PKCS#8 private key, nothing to do.
        return privkey

    keyinfilename = os.path.join(tempdir, "keyin.pem")
    keyoutfilename = os.path.join(tempdir, "keyout.pem")

    try:
        # Write PEM format private key to file.
        keyinfile = file(keyinfilename, "wb")
        keyinfile.write(privkey)
        keyinfile.close()

        # Convert a PKCS#8 private key to older SSLeay-compatible format.
        # Keep pass phrase as-is.
        runopenssl("pkcs8 -in %s -out %s -passin stdin -passout stdin %s" %
                   (quote(keyinfilename), quote(keyoutfilename), encryptcmd),
                   "%s\n%s\n" % (passphrase, passphrase))

        privkey = ""
        if os.path.isfile(keyoutfilename):
            # Read converted private key back.
            keyoutfile = file(keyoutfilename, "rb")
            privkey = keyoutfile.read()
            keyoutfile.close()

        if privkey.strip() == "":
            # OpenSSL did not create output. Probably a wrong pass phrase.
            raise ValueError("wrong pass phrase or invalid PKCS#8 private key")
    finally:
        # Delete temporary files.
        for fname in (keyinfilename, keyoutfilename):
            try:
                os.remove(fname)
            except OSError:
               pass

    return privkey

def decryptkey(tempdir, privkey, passphrase):
    '''
    decryptkey(...) -> (privkeyout, keytype)

    tempdir     Path to pre-existing temporary directory with read/write access
    privkey     RSA or DSA private key, a string in PEM (base-64) format
    passphrase  pass phrase for the private key, a non-Unicode string or None
    string      a binary string to sign

    keytype     detected key type, string, "RSA" or "DSA"
    privkeyout  decrypted private key in PEM (base-64) format

    NOTE: On platforms with poor file system security, decrypted version
    of the private key may be grabbed from the temporary directory!
    '''

    # Determine private key type.
    if privkey.find("-----BEGIN DSA PRIVATE KEY-----") >= 0:
        keytype = "DSA"
        convcmd = "dsa"
    elif privkey.find("-----BEGIN RSA PRIVATE KEY-----") >= 0:
        keytype = "RSA"
        convcmd = "rsa"
    else:
        raise ValueError("not an RSA or DSA private key in PEM format")

    keyinfilename = os.path.join(tempdir, "keyin.pem")
    keyoutfilename = os.path.join(tempdir, "keyout.pem")

    try:
        # Write PEM format private key to file.
        keyinfile = file(keyinfilename, "wb")
        keyinfile.write(privkey)
        keyinfile.close()

        # Decrypt the private key. Older versions of OpenSSL do not
        # accept the "-passin" parameter for the "dgst" command.
        runopenssl("%s -in %s -out %s -passin stdin" %
                   (convcmd, quote(keyinfilename),
                    quote(keyoutfilename)), passphrase)

        privkey = ""
        if os.path.isfile(keyoutfilename):
            # Read decrypted private key back.
            keyoutfile = file(keyoutfilename, "rb")
            privkey = keyoutfile.read()
            keyoutfile.close()

        if privkey.strip() == "":
            # OpenSSL did not create output. Probably a wrong pass phrase.
            raise ValueError("wrong pass phrase or invalid private key")
    finally:
        # Delete temporary files.
        for fname in (keyinfilename, keyoutfilename):
            try:
                os.remove(fname)
            except OSError:
               pass

    return (privkey, keytype)

def mkdtemp(template):
    '''
    Create a unique temporary directory.

    tempfile.mkdtemp() was introduced in Python v2.3. This is for
    backward compatibility.
    '''

    # Cross-platform way to determine a suitable location for temporary files.
    systemp = tempfile.gettempdir()

    if not template.endswith("XXXXXX"):
        raise ValueError("invalid template for mkdtemp(): %s" % template)

    for n in xrange(10000):
        randchars = []
        for m in xrange(6):
            randchars.append(random.choice("abcdefghijklmnopqrstuvwxyz"))

        tempdir = os.path.join(systemp, template[: -6]) + "".join(randchars)

        try:
            os.mkdir(tempdir, 0700)
            return tempdir
        except OSError:
            pass
    else:
        # All unique names in use, raise an error.
        raise OSError(errno.EEXIST, os.strerror(errno.EEXIST),
                      os.path.join(systemp, template))

def quote(filename):
    '''Quote a filename if it has spaces in it.'''
    if " " in filename:
        filename = '"%s"' % filename
    return filename

def runopenssl(command, datain = ""):
    '''Run the OpenSSL command line tool with the given parameters and data.'''

    global opensslcommand

    if opensslcommand == None:
        # Find path to the OpenSSL command.
        findopenssl()

    # Construct a command line for os.popen3().
    cmdline = '%s %s' % (opensslcommand, command)

    if openssldebug:
        # Print command line.
        print "DEBUG: os.popen3(%s)" % repr(cmdline)

    # Run command. Use os.popen3() to capture stdout and stderr.
    pipein, pipeout, pipeerr = os.popen3(cmdline)
    pipein.write(datain)
    pipein.close()
    dataout = pipeout.read()
    pipeout.close()
    errout = pipeerr.read()
    pipeerr.close()

    if openssldebug:
        # Print standard error output.
        print "DEBUG: pipeerr.read() = %s" % repr(errout)

    return (dataout, errout)

def findopenssl():
    '''Find the OpenSSL command line tool.'''

    global opensslcommand

    # Get PATH and split it to a list of paths.
    paths = os.environ["PATH"].split(os.pathsep)

    # Insert script path in front of others.
    # On Windows, this is where openssl.exe resides by default.
    if sys.path[0] != "":
        paths.insert(0, sys.path[0])

    for path in paths:
        cmd = os.path.join(path, "openssl")
        try:
            # Try to query OpenSSL version.
            pin, pout = os.popen4('"%s" version' % cmd)
            pin.close()
            verstr = pout.read()
            pout.close()
        except OSError:
            # Could not run command, skip to the next path candidate.
            continue

        if verstr.split()[0] == "OpenSSL":
            # Command found, stop searching.
            break
    else:
        raise IOError("no valid OpenSSL command line tool found in PATH")

    # Add quotes around command in case of embedded whitespace on path.
    opensslcommand = quote(cmd)
