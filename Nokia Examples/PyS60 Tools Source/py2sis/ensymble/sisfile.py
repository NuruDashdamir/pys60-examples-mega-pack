#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# sisfile.py - Symbian OS v9.x SIS file utilities
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

import os
import time
import struct
import sha

import symbianutil
import cryptutil
import sisfield


##############################################################################
# Public module-level functions
##############################################################################

def parseexpression(expr):
    '''Create a SISExpression SISField out of the given expression string.

    parseexpression(...) -> SISExpression

    expr            the expression, a string

    SISExpression   the returned SISExpression SISField

    NOTE: Only expressions of form "language == nn" are supported, for now.'''

    elist = expr.lower().split()

    # TODO: Only "language == nn" expressions supported for now.
    # Going to need a real parser for general expression support, though.
    try:
        if len(elist) != 3 or elist[0] != 'language' or elist[1] != '==':
            raise ValueError
        langnum = int(elist[2])
    except ValueError:
        raise ValueError("invalid expression '%s'" % expr)

    # Create a SISExpression SISField of type EPrimTypeVariable.
    leftfield = sisfield.SISExpression(Operator = sisfield.EPrimTypeVariable,
                                       IntegerValue = sisfield.EVarLanguage)

    # Create a SISExpression SISField of type EPrimTypeNumber.
    rightfield = sisfield.SISExpression(Operator = sisfield.EPrimTypeNumber,
                                       IntegerValue = langnum)

    # Create an equality test SISExpression SISField and return it.
    return sisfield.SISExpression(Operator = sisfield.EBinOpEqual,
                                  IntegerValue = 0,
                                  LeftExpression = leftfield,
                                  RightExpression = rightfield)

def signstring(privkey, passphrase, string):
    '''Sign a binary string using a given private key and its pass phrase.

    signstring(...) -> (signature, algorithm oid)

    privkey         private key (RSA or DSA), a binary string in PEM format
    passphrase      pass phrase (non-Unicode) for the private key or None
    string          binary string from which the signature is to be calculated

    signature       signature, a binary string
    algorithm oid   signature algorithm object identifier, a string'''

    # Sign string.
    signature, keytype = cryptutil.signstring(privkey, passphrase, string)

    # Determine algorithm object identifier.
    if keytype == "DSA":
        algoid = "1.2.840.10040.4.3"
    elif keytype == "RSA":
        algoid = "1.2.840.113549.1.1.5"
    else:
        raise ValueError("unknown key type '%s'" % keytype)

    return (signature, algoid)


##############################################################################
# Module-level functions which are normally only used by this module
##############################################################################

def makefiledata(contents):
    '''Make a SISFileData SISField out of the given binary string.

    makefiledata(...) -> SISFileData

    contents        file contents, a binary string

    SISFileData     the returned SISFileData instance

    NOTE: Data is compressed only if it is beneficial.'''

    # Wrap data inside SISCompressed SISField.
    cfield = sisfield.SISCompressed(Data = contents,
        CompressionAlgorithm = sisfield.ECompressAuto,
        rawdatainside = True)

    # Create a SISFileData SISField out of the wrapped data and return it.
    return sisfield.SISFileData(FileData = cfield)

def makefiledesc(contents, compressedlen, index, target = None,
                 mimetype = None, capabilities = None,
                 operation = sisfield.EOpInstall, options = 0):
    '''Make a SISFileDescription SISField for the given file.

    makefiledesc(...) -> SISFileDescription

    contents            file contents for SHA-1 digest calc., a binary string
    compressedlen       length of file contents inside a SISCompressed SISField
    index               index of file inside a SISDataUnit SISField, an integer
    target              install path in target device, a string or None
    mimetype            MIME type, a string or None
    capabilities        Symbian OS capabilities for EXE-files, int. mask or None
    operation           what to do with the file, an integer bit mask
    options             operation dependent install options, an integer bit mask

    SISFileDescription  the returned SISFileDescription instance

    Constants for operation and options can be found in the sisfield module.
    Operation is one of EOpInstall, EOpRun, EOpText or EOpNull. Options
    depend on the selected operation, for example EInstVerifyOnRestore.'''

    # Create a SISString of target path.
    if target == None:
        # Target may be None. The file is not installed anywhere in that case.
        target = ""
    targetfield = sisfield.SISString(String = target)

    # Create a SISString of MIME type.
    if mimetype == None:
        # MIME type may be None (and usually is).
        mimetype = ""
    mimetypefield = sisfield.SISString(String = mimetype)

    # Create a SISCapabilities SISField for executable capabilities.
    if capabilities != None and capabilities != 0L:
        # SISCapabilities expects a binary string, need to convert the
        # capability mask. If capability mask is 0, no capability field
        # is generated. Otherwise signsis.exe cannot sign the resulting
        # SIS file.
        capstring = symbianutil.capmasktorawdata(capabilities)
        capfield = sisfield.SISCapabilities(Capabilities = capstring)
    else:
        # Only EXE- and DLL-files have a concept of capability.
        capfield = None

    # Calculate file hash using SHA-1. Create a SISHash SISField out of it.
    # Contents may be None, to properly support the EOpNull install operation.
    if contents != None:
        sha1hash = sha.new(contents).digest()
    else:
        # No data, the containing SISBlob is mandatory but empty.
        sha1hash = ""
    hashblob = sisfield.SISBlob(Data = sha1hash)
    hashfield = sisfield.SISHash(HashAlgorithm = sisfield.ESISHashAlgSHA1,
                                 HashData = hashblob)

    # Create a SISFileDescription SISField and return it.
    return sisfield.SISFileDescription(Target = targetfield,
                                       MIMEType = mimetypefield,
                                       Capabilities = capfield,
                                       Hash = hashfield,
                                       Operation = operation,
                                       OperationOptions = options,
                                       Length = compressedlen,
                                       UncompressedLength = len(contents),
                                       FileIndex = index)

def makedependency(uid, fromversion, toversion, names):
    '''Make a SISDependency SISField for the given UID, version dependency.

    makedependency(...) -> SISDependency

    uid             UID, an unsigned integer
    fromversion     from-version, a triple-item list/tuple (major, minor, build)
    toversion       to-version, a triple-item list/tuple or None
    names           names for the dependency, a list of string per language

    SISDependency   the returned SISDependency SISField

    NOTE: toversion may be None, indicating any version after fromversion.'''

    # Convert parameters to SISFields.
    uidfield = sisfield.SISUid(UID1 = uid)

    fromverfield = sisfield.SISVersion(Major = fromversion[0],
                                       Minor = fromversion[1],
                                       Build = fromversion[2])
    if toversion != None:
        toverfield = sisfield.SISVersion(Major = toversion[0],
                                         Minor = toversion[1],
                                         Build = toversion[2])
    else:
        toverfield = None

    verrangefield = sisfield.SISVersionRange(FromVersion = fromverfield,
                                             ToVersion = toverfield)

    l = []
    for name in names:
        l.append(sisfield.SISString(String = name))
    namesfield = sisfield.SISArray(SISFields = l, SISFieldType = "SISString")

    # Create a SISDependency SISField and return it.
    return sisfield.SISDependency(UID = uidfield,
                                  VersionRange = verrangefield,
                                  DependencyNames = namesfield)


def makeinstallblock(files = [], embeddedsisfiles = [], ifblocks = []):
    '''Make a SISInstallBlock SISField out of the given lists of SISFields.

    makeinstallblock(...) -> SISInstallBlock

    files             a list of SISFileDescription SISFields (normal files)
    embeddedsisfiles  a list of SISController SISFields (embedded SIS files)
    ifblocks          a list of SISIf SISFields (conditionally installed files)

    SISInstallBlock   the returned SISInstallBlock instance

    NOTE: Any of the lists may be empty (and are, by default).'''


    # Convert lists to SISArrays.
    sa1 = sisfield.SISArray(SISFields = files,
                            SISFieldType = "SISFileDescription")
    sa2 = sisfield.SISArray(SISFields = embeddedsisfiles,
                            SISFieldType = "SISController")
    sa3 = sisfield.SISArray(SISFields = ifblocks,
                            SISFieldType = "SISIf")

    # Create a SISInstallBlock SISField and return it.
    return sisfield.SISInstallBlock(Files = sa1, EmbeddedSISFiles = sa2,
                                    IfBlocks = sa3)

def makelangconditional(languages, langdepfiles):
    '''Make a SISIf and SISElseIfs for language dependent installation of files.

    makelangconditional(...) -> SISIf or None

    languages       a list of language numbers (not names, IDs or SISLanguages)
    landepfiles     a list of file lists, where each file list is a list of
                    alternative SISFileDescription SISFields for each language

    SISIf           the returned SISIf instance or None if no files'''

    if len(langdepfiles) == 0:
        # No language dependent files, leave.
        return None

    # Create a file list per language.
    filesperlang = []
    for n in xrange(len(languages)):
        filesperlang.append([])

    # Gather all files from the same language to a single list.
    for files in langdepfiles:
        if len(files) != len(languages):
            raise ValueError("%d files given but number of languages is %d" %
                             (len(files), len(languages)))

        for n in xrange(len(languages)):
            filesperlang[n].append(files[n])

    if len(languages) == 0:
        # No languages, leave. (This is down here so that errors
        # can still be caught above.)
        return None

    # Create a SISArray of SISElseIf SISFields.
    elseiffields = []
    for n in xrange(1, len(languages)):
        elseifexpfield = parseexpression("language == %d" % languages[n])
        elseiffield = sisfield.SISElseIf(Expression = elseifexpfield,
            InstallBlock = makeinstallblock(filesperlang[n]))
        elseiffields.append(elseiffield)
    elseiffieldarray = sisfield.SISArray(SISFields = elseiffields,
                                         SISFieldType = "SISElseIf")

    # Create and return the final SISIf SISField.
    ifexpfield = parseexpression("language == %d" % languages[0])
    return sisfield.SISIf(Expression = ifexpfield,
                          InstallBlock = makeinstallblock(filesperlang[0]),
                          ElseIfs = elseiffieldarray)


##############################################################################
# SimpleSISWriter class for no-frills SIS file generation
##############################################################################

class SimpleSISWriter(object):
    '''A no-frills SIS file generator

    Limitations:

    - Option lists are not supported.
    - Condition blocks are not supported. Languages are, however.
    - Nested SIS files are not supported.
    - SIS type is always a full installation package (type EInstInstallation).
    - Package options (EInstFlagShutdownApps) are not supported.'''

    def __init__(self, languages, names, uid, version,
                 vendorname, vendornames, creationtime = None):
        # Set empty list of languages, names, files, certificates and so on.
        self.languages      = []
        self.filedata       = []
        self.files          = []
        self.langdepfiles   = []
        self.logo           = None
        self.certificates   = []
        self.targetdevices  = []
        self.dependencies   = []
        self.properties     = []

        # Convert language IDs/names to language numbers.
        for lang in languages:
            try:
                langnum = symbianutil.langidtonum[lang]
            except KeyError:
                # Not a language ID, try names next.
                try:
                    langnum = symbianutil.langnametonum[lang]
                except KeyError:
                    raise ValueError("invalid language '%s'" % lang)
            self.languages.append(langnum)

        # Verify number of names and vendor names wrt. number of languages.
        if len(names) != len(self.languages):
            raise ValueError(
                "%d package names given but number of languages is %d" %
                (len(names), len(self.languages)))

        if len(vendornames) != len(self.languages):
            raise ValueError(
                "%d vendor names given but number of languages is %d" %
                (len(vendornames), len(self.languages)))

        # Convert language dependent names to a SISArray of SISStrings.
        l = []
        for name in names:
            l.append(sisfield.SISString(String = name))
        self.names = sisfield.SISArray(SISFields = l,
                                       SISFieldType = "SISString")

        # Convert integer UID to SISUid SISField.
        self.uid = sisfield.SISUid(UID1 = uid)

        # Convert version number triplet to SISVersion SISField.
        self.version = sisfield.SISVersion(Major = version[0],
                                           Minor = version[1],
                                           Build = version[2])

        # Convert unique vendor name to SISString SISField.
        self.vendorname = sisfield.SISString(String = vendorname)

        # Convert language dependent vendor names to a SISArray of SISStrings.
        l = []
        for name in vendornames:
            l.append(sisfield.SISString(String = name))
        self.vendornames = sisfield.SISArray(SISFields = l,
                                             SISFieldType = "SISString")

        if creationtime == None:
            # If no creation time given, use the time
            # of SimpleSISWriter instantiation.
            creationtime = time.gmtime()

        # Convert standard Python time representation to SISFields.
        datefield = sisfield.SISDate(Year = creationtime.tm_year,
                                     Month = creationtime.tm_mon - 1,
                                     Day = creationtime.tm_mday)
        timefield = sisfield.SISTime(Hours = creationtime.tm_hour,
                                     Minutes = creationtime.tm_min,
                                     Seconds = creationtime.tm_sec)
        self.creationtime = sisfield.SISDateTime(Date = datefield,
                                                 Time = timefield)

    def setlogo(self, contents, mimetype):
        '''Add a logo graphics to generated SIS file.

        NOTE: Not all devices display a logo during installation.'''

        if self.logo != None:
            raise ValueError("logo already set")

        # Create SISFileData and SISFileDescription SISFields.
        filedata = makefiledata(contents)
        complen = filedata.getcompressedlength()
        runopts = (sisfield.EInstFileRunOptionInstall |
                   sisfield.EInstFileRunOptionByMimeType)
        filedesc = makefiledesc(contents, complen, len(self.filedata),
                                None, mimetype, None, sisfield.EOpRun, runopts)
        self.logo = sisfield.SISLogo(LogoFile = filedesc)
        self.filedata.append(filedata)

    def addfile(self, contents, target = None, mimetype = None,
                capabilities = None, operation = sisfield.EOpInstall,
                options = 0):
        '''Add a file that is same for all languages to generated SIS file.'''

        # Create SISFileData and SISFileDescription SISFields.
        filedata = makefiledata(contents)
        complen = filedata.getcompressedlength()
        metadata = makefiledesc(contents, complen, len(self.filedata),
                                target, mimetype, capabilities,
                                operation, options)
        self.files.append(metadata)
        self.filedata.append(filedata)

    def addlangdepfile(self, clist, target = None, mimetype = None,
                       capabilities = None, operation = sisfield.EOpInstall,
                       options = 0):
        '''Add language dependent files to generated SIS file.

        A conditional expression is automatically generated for the file.'''

        if len(clist) != len(self.languages):
            raise ValueError("%d files given but number of languages is %d" %
                             (len(clist), len(self.languages)))

        data = []
        files = []
        index = len(self.filedata)
        for contents in clist:
            # Create SISFileData and SISFileDescription SISFields.
            filedata = makefiledata(contents)
            complen = filedata.getcompressedlength()
            metadata = makefiledesc(contents, complen, index,
                                    target, mimetype, capabilities,
                                    operation, options)
            files.append(metadata)
            data.append(filedata)
            index += 1

        self.langdepfiles.append(files)
        self.filedata.extend(data)

    def addcertificate(self, privkey, cert, passphrase):
        '''Add a certificate to SIS file.

        Private key and certificate are in PEM (base-64) format.'''

        self.certificates.append((privkey, cert, passphrase))

    def addtargetdevice(self, uid, fromversion, toversion, names):
        '''Add a mandatory target device UID to generated SIS file.

        NOTE: Names are not usually displayed. Instead, the device vendor
        has specified what the names must be.'''

        if len(names) != len(self.languages):
            raise ValueError(
                "%d device names given but number of languages is %d" %
                (len(names), len(self.languages)))

        depfield = makedependency(uid, fromversion, toversion, names)
        self.targetdevices.append(depfield)

    def adddependency(self, uid, fromversion, toversion, names):
        '''Add an installed package dependency to generated SIS file.

        NOTE: Some devices display the first name of the dependency
        regardless of the device language.'''

        if len(names) != len(self.languages):
            raise ValueError(
                "%d dependency names given but number of languages is %d" %
                (len(names), len(self.languages)))

        depfield = makedependency(uid, fromversion, toversion, names)
        self.dependencies.append(depfield)

    def addproperty(self, key, value):
        '''Add a property key, value pair to generated SIS file.

        When installing other SIS files, they may query these properties.'''

        # Convert parameters to a SISProperty SISField.
        self.properties.append(sisfield.SISProperty(Key = key,
                                                    Value = value))

    def tostring(self):
        '''Convert this SIS instance to a (possibly very large) string.'''

        # Generate a SISInfo SISField.
        infofield = sisfield.SISInfo(UID = self.uid,
                                     VendorUniqueName = self.vendorname,
                                     Names = self.names,
                                     VendorNames = self.vendornames,
                                     Version = self.version,
                                     CreationTime = self.creationtime,
                                     InstallType = sisfield.EInstInstallation,
                                     InstallFlags = 0)

        # Generate an empty SISSupportedOptions SISField.
        # Option lists are not supported by SimpleSISWriter.
        sa = sisfield.SISArray(SISFields = [],
                               SISFieldType = "SISSupportedOption")
        optfield = sisfield.SISSupportedOptions(Options = sa)

        # Convert language numbers to SISArray of SISLanguages
        # and generate a SISSupportedLanguages SISField.
        langfieldlist = []
        for lang in self.languages:
            langfieldlist.append(sisfield.SISLanguage(Language = lang))
        sa = sisfield.SISArray(SISFields = langfieldlist,
                               SISFieldType = "SISLanguage")
        langfield = sisfield.SISSupportedLanguages(Languages = sa)

        # Generate SISPrerequisites SISField.
        sa1 = sisfield.SISArray(SISFields = self.targetdevices,
                                SISFieldType = "SISDependency")
        sa2 = sisfield.SISArray(SISFields = self.dependencies,
                                SISFieldType = "SISDependency")
        prereqfield = sisfield.SISPrerequisites(TargetDevices = sa1,
                                                Dependencies = sa2)

        # Generate SISProperties SISField.
        sa = sisfield.SISArray(SISFields = self.properties,
                               SISFieldType = "SISProperty")
        propfield = sisfield.SISProperties(Properties = sa)

        # Generate SISInstallBlock SISField.
        iffield = makelangconditional(self.languages, self.langdepfiles)
        if iffield:
            # Some language dependent files
            iffieldlist = [iffield]
        else:
            # No language dependent files
            iffieldlist = []
        ibfield = makeinstallblock(self.files, [], iffieldlist)

        # Generate a data index field. No embedded SIS files, index is 0.
        didxfield = sisfield.SISDataIndex(DataIndex = 0)

        # Generate a SISController SISField without any signatures.
        ctrlfield = sisfield.SISController(Info = infofield,
                                           Options = optfield,
                                           Languages = langfield,
                                           Prerequisites = prereqfield,
                                           Properties = propfield,
                                           Logo = self.logo,
                                           InstallBlock = ibfield)

        # Calculate metadata signature for each certificate.
        certfieldlist = []
        for cert in self.certificates:
            # Calculate a signature of the SISController so far.
            string = ctrlfield.tostring()
            string = sisfield.stripheaderandpadding(string)
            signature, algoid = signstring(cert[0], cert[2], string)

            # Create a SISCertificateChain SISField from certificate data.
            sf1 = sisfield.SISBlob(Data = cryptutil.certtobinary(cert[1]))
            sf2 = sisfield.SISCertificateChain(CertificateData = sf1)

            # Create a SISSignature SISField from calculated signature.
            sf3 = sisfield.SISString(String = algoid)
            sf4 = sisfield.SISSignatureAlgorithm(AlgorithmIdentifier = sf3)
            sf5 = sisfield.SISBlob(Data = signature)
            sf6 = sisfield.SISSignature(SignatureAlgorithm = sf4,
                                        SignatureData = sf5)

            # Create a new SISSignatureCertificateChain SISField.
            sa = sisfield.SISArray(SISFields = [sf6])
            certfieldlist.append(sisfield.SISSignatureCertificateChain(
                Signatures = sa, CertificateChain = sf2))

            # Add certificate to SISController SISField.
            ctrlfield.setsignatures(certfieldlist)

        # Finally add a data index field to SISController SISField.
        # and wrap it in SISCompressed SISField.
        ctrlfield.DataIndex = didxfield
        ctrlcompfield = sisfield.SISCompressed(Data = ctrlfield,
            CompressionAlgorithm = sisfield.ECompressDeflate)

        # Generate SISData SISField.
        sa = sisfield.SISArray(SISFields = self.filedata,
                               SISFieldType = "SISFileData")
        dufield = sisfield.SISDataUnit(FileData = sa)
        sa = sisfield.SISArray(SISFields = [dufield])
        datafield = sisfield.SISData(DataUnits = sa)

        # Calculate SISController checksum.
        # TODO: Requires an extra tostring() conversion.
        ctrlcs = symbianutil.crc16ccitt(ctrlcompfield.tostring())
        ctrlcsfield = sisfield.SISControllerChecksum(Checksum = ctrlcs)

        # Calculate SISData checksum.
        # TODO: Requires an extra tostring() conversion.
        datacs = symbianutil.crc16ccitt(datafield.tostring())
        datacsfield = sisfield.SISDataChecksum(Checksum = datacs)

        # Generate SISContents SISField.
        contentsfield = sisfield.SISContents(ControllerChecksum = ctrlcsfield,
                                             DataChecksum = datacsfield,
                                             Controller = ctrlcompfield,
                                             Data = datafield)

        # Generate a SIS UID string.
        uidstring = symbianutil.uidstostring(0x10201a7aL, 0x00000000L,
                                             self.uid.UID1)

        # Return the completed SIS file as a string.
        return uidstring + contentsfield.tostring()

    def tofile(self, outfile):
        '''Write this SIS instance to a file object or a named file.'''

        s = self.tostring()

        try:
            f = file(outfile, "wb")
            try:
                f.write(s)
            finally:
                f.close()
        except TypeError:
            f.write(s)
