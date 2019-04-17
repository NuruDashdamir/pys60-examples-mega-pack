#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# sisfield.py - Symbian OS v9.x SIS file utilities, SISField support classes
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

import struct
import zlib

import symbianutil


# TODO: 1. Make all tostring() methods cache the result.
# TODO: 2. Allow modifying objects after creation, keeping string cache in sync.
# TODO: 3. Implement a list-of-strings type, which the tostring() (or
#          some other method with a better name) can use, to eliminate
#          superfluous string concatenations.


##############################################################################
# Parameters
##############################################################################

DEBUG               = 0     # (0: None, 1: Basic, 2: Verbose)
MAXNUMSIGNATURES    = 8     # Maximum number of signatures in a SISController


##############################################################################
# Public SISField constants (in original Symbian OS naming style)
##############################################################################

ECompressAuto                   = -1    # Not a real compression type
ECompressNone                   = 0
ECompressDeflate                = 1

EInstInstallation               = 0
EInstAugmentation               = 1
EInstPartialUpgrade             = 2
EInstPreInstalledApp            = 3
EInstPreInstalledPatch          = 4

EInstFlagShutdownApps           = 1

EOpInstall                      = 1
EOpRun                          = 2
EOpText                         = 4
EOpNull                         = 8

EInstVerifyOnRestore            = 1 << 15

EInstFileRunOptionInstall       = 1 << 1
EInstFileRunOptionUninstall     = 1 << 2
EInstFileRunOptionByMimeType    = 1 << 3
EInstFileRunOptionWaitEnd       = 1 << 4
EInstFileRunOptionSendEnd       = 1 << 5

EInstFileTextOptionContinue     = 1 << 9    # Not used by makesis v. 4, 0, 0, 2
EInstFileTextOptionSkipIfNo     = 1 << 10
EInstFileTextOptionAbortIfNo    = 1 << 11
EInstFileTextOptionExitIfNo     = 1 << 12

ESISHashAlgSHA1                 = 1

ESISSignatureAlgSHA1RSA         = "1.2.840.113549.1.1.5"
ESISSignatureAlgSHA1DSA         = "1.2.840.10040.4.3"

EBinOpEqual                     = 1
EBinOpNotEqual                  = 2
EBinOpGreaterThan               = 3
EBinOpLessThan                  = 4
EBinOpGreaterOrEqual            = 5
EBinOpLessOrEqual               = 6
ELogOpAnd                       = 7
ELogOpOr                        = 8
EUnaryOpNot                     = 9
EFuncExists                     = 10
EFuncAppProperties              = 11
EFuncDevProperties              = 12
EPrimTypeString                 = 13
EPrimTypeOption                 = 14
EPrimTypeVariable               = 15
EPrimTypeNumber                 = 16

EVarLanguage                    = 0x1000
EVarRemoteInstall               = 0x1001


##############################################################################
# Public exception class for SIS parsing / generation
##############################################################################

class SISException(StandardError):
    '''SIS parsing / generation error'''
    pass


##############################################################################
# Public module-level functions
##############################################################################

def SISField(fromstring, exactlength = True):
    '''Generator function for creating SISField subclass instances from a string

    If exactlength is False, return a tuple of (SISField, bytes consumed).
    Otherwise return SISField directly.'''

    # Determine SISField subclass type.
    ftype, hdrlen, flen, padlen = parsesisfieldheader(fromstring, None,
                                                      exactlength)

    try:
        fclass = fieldnumtoclass[ftype]
    except KeyError:
        raise SISException("invalid SISField type '%d'" % ftype)

    # Limit string to actual data length (in case exactlength was False).
    fromstring = fromstring[:(hdrlen + flen + padlen)]

    # Create a subclass instance.
    field = fclass(fromstring = fromstring)

    if exactlength:
        return field
    else:
        # Normal SISField subclasses use SISField() to parse adjacent SISFields.
        # Number of consumed bytes need to be passed back in that case. This
        # may violate the idea of a generator function somewhat, but eliminates
        # a bit of duplicated code.
        return (field, len(fromstring))

def stripheaderandpadding(fromstring):
    '''Return the actual content of SISField string.

    stripheaderandpadding(...) -> contents

    fromstring  a SISField string

    contents    SISField contents without the header and padding'''

    # Parse field header.
    ftype, hdrlen, flen, padlen = parsesisfieldheader(fromstring)

    # Return field contents.
    return fromstring[hdrlen:(hdrlen + flen)]


##############################################################################
# Module-level functions which are normally only used by this module
##############################################################################

def parsesisfieldheader(string, requiredtype = None, exactlength = True):
    '''Parse the header of a SISField string and return the field type and
    lengths of the various parts (header, data, padding). Optionally, check
    that the type is correct and that the string length is not too long.'''

    hdrlen = 8
    if hdrlen > len(string):
        raise SISException("not enough data for a complete SISField header")

    # Get SISField type and first part of the length.
    ftype, flen = struct.unpack("<LL", string[:8])

    # Get rest of the SISField length, 31-bit or 63-bit.
    flen2 = None
    if flen & 0x8000000L:
        # 63-bit length, read rest of length.
        hdrlen = 12
        if hdrlen > len(string):
            raise SISException("not enough data for a complete SISField header")
        flen2 = struct.unpack("<L", string[8:12])[0]
        flen = (flen & 0x7ffffffL) | (flen2 << 31)

    # Calculate padding to 32-bit boundary.
    padlen = ((flen + 3) & ~0x3L) - flen

    if requiredtype != None and ftype != requiredtype:
        raise SISException("invalid SISField type '%d'" % ftype)

    if (hdrlen + flen + padlen) > len(string):
        raise SISException("SISField contents too short")

    # Allow oversized strings when parsing recursive SISFields.
    if exactlength and (hdrlen + flen + padlen) < len(string):
        raise SISException("SISField contents too long")

    return ftype, hdrlen, flen, padlen

def makesisfieldheader(fieldtype, fieldlen):
    '''Create a SISField header string from type and length.'''

    if fieldlen < 0x80000000L:
        # 31-bit length
        return struct.pack("<LL", fieldtype, fieldlen)
    else:
        # 63-bit length
        fieldlen2 = fieldlen >> 31
        fieldlen  = (fieldlen & 0x7fffffffL) | 0x80000000L
        return struct.pack("<LLL", fieldtype, fieldlen, fieldlen2)

def makesisfieldpadding(fieldlen):
    '''Create a string of zero bytes for padding to 32-bit boundary.
    Parameter may be either the whole field length (header + data)
    or just the data length.'''

    # Calculate padding to 32-bit boundary.
    padlen = ((fieldlen + 3) & ~0x3L) - fieldlen

    return "\x00" * padlen


##############################################################################
# SISField base classes
##############################################################################

class SISFieldBase(object):
    '''SISField base class'''
    def __init__(self, **kwds):
        if DEBUG > 0:
            # DEBUG: Print class name during initialization.
            print "%s.__init__()" % self.__class__.__name__

        # Get the names of all instance variables.
        validkwds = self.__dict__.keys()

        # Filter out private instance variables (all in lowercase).
        validkwds = filter(lambda s: s != s.lower(), validkwds)

        # Set type code.
        self.fieldtype = fieldnametonum[self.__class__.__name__]

        if "fromstring" in kwds:
            if DEBUG > 1:
                # DEBUG: Dump of string parameter.
                print repr(kwds["fromstring"])

            # Load instance variables from string.
            if len(kwds) != 1:
                raise TypeError(
                    "keyword 'fromstring' may not be given with other keywords")
            self.fromstring(kwds["fromstring"])
        else:
            # Load instance variables from keywords.
            # Only accept existing variable names.
            for kwd in kwds.keys():
                if kwd not in validkwds:
                    raise AttributeError("'%s' object has no attribute '%s'" %
                                         (self.__class__.__name__, kwd))
                self.__dict__[kwd] = kwds[kwd]

    def __str__(self):
        # Default __str__() for SISFields, only return the field name.
        return "<%s>" % self.__class__.__name__

class SISFieldNormal(SISFieldBase):
    '''SISField base class for normal fields (fields containing only other
    fields and integers)'''

    # Subfield types
    FTYPE_INTEGRAL  = 0     # Integer
    FTYPE_MANDATORY = 1     # Mandatory SISField
    FTYPE_OPTIONAL  = 2     # Optional SISField
    FTYPE_ARRAY     = 3     # SISArray with zero or more items

    def __init__(self, **kwds):
        # Initialize instance variables to None.
        for fattr, fkind, ffmt in self.subfields:
            self.__dict__[fattr] = None

        # Set instance variables.
        SISFieldBase.__init__(self, **kwds)

        for fattr, fkind, ffmt in self.subfields:
            # Check that all required instance variables are set.
            if fkind != self.FTYPE_OPTIONAL and self.__dict__[fattr] == None:
                raise AttributeError("missing '%s' attribute for '%s'" %
                                     (fattr, self.__class__.__name__))

            if fkind in (self.FTYPE_MANDATORY, self.FTYPE_OPTIONAL):
                # Verify SISField types.
                if (self.__dict__[fattr] != None and
                    fieldnumtoname[self.__dict__[fattr].fieldtype] != ffmt):
                    raise TypeError(
                        "attribute '%s' for '%s' is of invalid SISField type" %
                        (fattr, self.__class__.__name__))
            elif fkind == self.FTYPE_ARRAY:
                # Verify SISArray contents.
                if (fieldnumtoname[self.__dict__[fattr].fieldtype] != "SISArray"
                    or
                    fieldnumtoname[self.__dict__[fattr].SISFieldType] != ffmt):
                    raise TypeError(
                        "SISArray attribute '%s' for '%s' is of invalid type" %
                        (fattr, self.__class__.__name__))

    def fromstring(self, string):
        # Parse field header.
        ftype, hdrlen, flen, padlen = parsesisfieldheader(string,
                                                          self.fieldtype)

        # Recursively parse subfields.
        pos = hdrlen
        reuse = None    # SISField to re-use or None
        try:
            for fattr, fkind, ffmt in self.subfields:
                field = None    # No value by default

                if fkind == self.FTYPE_INTEGRAL:
                    # Integer, unpack it.
                    if reuse:
                        # It is an error if there is a field to
                        # re-use present at this time.
                        raise ValueError("integral field preceded optional")

                    n = struct.calcsize(ffmt)
                    field = struct.unpack(ffmt, string[pos:(pos + n)])[0]
                    pos += n
                else:
                    # SISField, read data from string or
                    # re-use field from previous round.
                    if not reuse:
                        # No old field to handle, convert string to SISField.
                        if pos < (hdrlen + flen):
                            field, n = SISField(string[pos:(hdrlen + flen)],
                                                False)
                            pos += n
                        elif fkind != self.FTYPE_OPTIONAL:
                            # No more data in string, raise an exception.
                            raise ValueError("unexpected end-of-data")
                    else:
                        # Field from previous round present, re-use it.
                        field = reuse
                        reuse = None

                    # Verify SISField type.
                    if field != None:
                        fname = fieldnumtoname[field.fieldtype]
                        if fkind == self.FTYPE_ARRAY:
                            if (fname != "SISArray" or
                                fieldnumtoname[field.SISFieldType] != ffmt):
                                    # Wrong type of fields inside SISArray,
                                    # raise an exception.
                                    raise ValueError("invalid SISArray type")
                        elif fkind == self.FTYPE_MANDATORY:
                            if fname != ffmt:
                                # Mandatory field missing, raise an exception.
                                raise ValueError("mandatory field missing")
                        elif fkind == self.FTYPE_OPTIONAL:
                            if fname != ffmt:
                                # Wrong type for optional field. Skip optional
                                # field and re-use already parsed field on next
                                # round.
                                reuse = field
                                field = None

                # Introduce field as an instance variable.
                self.__dict__[fattr] = field
        except (ValueError, KeyError, struct.error):
            if DEBUG > 0:
                # DEBUG: Raise a detailed exception.
                raise
            else:
                raise SISException("invalid '%s' structure" %
                                   self.__class__.__name__)

    def tostring(self):
        # Recursively create strings from subfields.
        fstrings = [None]
        totlen = 0
        for fattr, fkind, ffmt in self.subfields:
            field = self.__dict__[fattr]
            if fkind == self.FTYPE_INTEGRAL:
                # Integer, pack it.
                try:
                    string = struct.pack(ffmt, field)
                except:
                    print "%s %s %s" % (self.__class__, ffmt, repr(field))
                    raise
                fstrings.append(string)
                totlen += len(string)
            else:
                if field == None:
                    if fkind == self.FTYPE_OPTIONAL:
                        # Optional field missing, skip it.
                        pass
                    else:
                        # Mandatory field missing, raise an exception.
                        raise SISException("field '%s' missing for '%s'" %
                                           (fattr, self.__dict__.__name__))
                else:
                    # Convert SISField to string.
                    string = field.tostring()
                    fstrings.append(string)
                    totlen += len(string)

        try:
            del string  # Try to free some memory early.
        except:
            pass

        fstrings[0] = makesisfieldheader(self.fieldtype, totlen)
        fstrings.append(makesisfieldpadding(totlen))

        # TODO: Heavy on memory, optimize (new string type with concat.)
        return "".join(fstrings)

class SISFieldSpecial(SISFieldBase):
    '''SISField base class for special fields (fields that do something
    special for the data they contain or the data is of variable length)'''
    def __init__(self, **kwds):
        # Set instance variables.
        SISFieldBase.__init__(self, **kwds)


##############################################################################
# Special SISField subclasses
##############################################################################

class SISString(SISFieldSpecial):
    '''UCS-2 (UTF-16LE) string'''
    def __init__(self, **kwds):
        # Set default values.
        self.String = None

        # Parse keyword parameters.
        SISFieldSpecial.__init__(self, **kwds)

        # Check that all required instance variables are set.
        if self.String == None:
            raise AttributeError("missing '%s' attribute for '%s'" %
                                 ("String", self.__class__.__name__))

    def fromstring(self, string):
        ftype, hdrlen, flen, padlen = parsesisfieldheader(string,
                                                          self.fieldtype)
        self.String = string[hdrlen:(hdrlen + flen)].decode("UTF-16LE")

    def tostring(self):
        encstr = self.String.encode("UTF-16LE")
        return "%s%s%s" % (makesisfieldheader(self.fieldtype, len(encstr)),
                           encstr, makesisfieldpadding(len(encstr)))

    def __str__(self):
        # Always return Unicode string. Let Python default encoding handle it.
        return u"<SISString '%s'>" % self.String

class SISArray(SISFieldSpecial):
    '''An array of other SISFields, all of the same type'''
    def __init__(self, **kwds):
        # Set default values.
        self.SISFieldType = None    # Invalid type, checked later.
        self.SISFields = []

        # Parse keyword parameters.
        SISFieldSpecial.__init__(self, **kwds)

        # Make a copy of the supplied list
        # (caller may try to modify the original).
        self.SISFields = self.SISFields[:]

        # Allow type to be a string or number.
        self.SISFieldType = fieldnametonum.get(self.SISFieldType,
                                               self.SISFieldType)

        # Get type of first field if not given explicitly.
        if self.SISFieldType == None:
            if len(self.SISFields) > 0:
                self.SISFieldType = self.SISFields[0].fieldtype
            else:
                raise AttributeError("no SISFieldType given")

        # Check that all fields are of the same type.
        for f in self.SISFields:
            if f.fieldtype != self.SISFieldType:
                raise TypeError("SISFieldType mismatch for SISArray")

    def fromstring(self, string):
        # Parse field header.
        ftype, hdrlen, flen, padlen = parsesisfieldheader(string,
                                                          self.fieldtype)

        if flen < 4:
            raise SISException("not enough data for a complete SISArray header")

        # Get array type (type of SISFields in the array).
        atype = struct.unpack("<L", string[hdrlen:(hdrlen + 4)])[0]

        pos = hdrlen + 4    # Skip SISFieldType.
        totlen = hdrlen + flen
        fields = []
        while pos < totlen:
            # Get first part of the SISField length.
            alen = struct.unpack("<L", string[pos:(pos+4)])[0]
            pos += 4

            # Get rest of the SISField length, 31-bit or 63-bit.
            alen2 = None
            if alen & 0x8000000L:
                # 63-bit length, read rest of length.
                alen2 = struct.unpack("<L", string[pos:(pos+4)])[0]
                alen = (alen & 0x7ffffffL) | (alen2 << 31)
                pos += 4

            # Calculate padding to 32-bit boundary.
            apadlen = ((alen + 3) & ~0x3L) - alen

            # Construct a valid SISField header and proper padding.
            fhdr = makesisfieldheader(atype, alen)
            fpad = makesisfieldpadding(alen)

            # Create a SISField.
            # TODO: Heavy on memory, optimize (new string type with concat.)
            field = SISField(fhdr + string[pos:(pos + alen)] + fpad)

            fields.append(field)

            pos += alen + apadlen

        self.SISFieldType = atype
        self.SISFields = fields

    def tostring(self):
        totlen = 4  # For the SISFieldType of the array
        fstrings = ["", struct.pack("<L", self.SISFieldType)]
        for f in self.SISFields:
            s = f.tostring()[4:]    # Strip type code.
            fstrings.append(s)
            totlen += len(s)
        fstrings[0] = makesisfieldheader(self.fieldtype, totlen)
        fstrings.append(makesisfieldpadding(totlen))    # Not really necessary.
        return "".join(fstrings)

    def __str__(self):
        return "<SISArray of %d %s fields>" % (
            len(self.SISFields), fieldnumtoname[self.SISFieldType])

    # Standard list semantics ([n:m], len, append, insert, pop, del, iteration)
    def __getitem__(self, key):
        # Support older Python versions as well (v2.0 onwards).
        try:
            return self.SISFields[key]
        except TypeError:
            return self.SISFields[key.start:key.stop]

    def __setitem__(self, key, value):
        # Support older Python versions as well (v2.0 onwards).
        try:
            self.SISFields[key] = value
        except TypeError:
            self.SISFields[key.start:key.stop] = value

    def __delitem__(self, key):
        # Support older Python versions as well (v2.0 onwards).
        try:
            del self.SISFields[key]
        except TypeError:
            del self.SISFields[key.start:key.stop]

# Not supported in Python v2.2, where __getitem__() is used instead.
#    def __iter__(self):
#        return self.SISFields.__iter__()

    def __len__(self):
        return self.SISFields.__len__()

    def append(self, obj):
        return self.SISFields.append(obj)

    def insert(self, idx, obj):
        return self.SISFields.insert(idx, obj)

    def extend(self, iterable):
        return self.SISFields.extend(iterable)

    def pop(self):
        return self.SISFields.pop()

class SISCompressed(SISFieldSpecial):
    '''A compression wrapper for another SISField or raw data'''
    def __init__(self, **kwds):
        # Set default values.
        self.CompressionAlgorithm = None
        self.Data = None

        if "rawdatainside" in kwds:
            self.rawdatainside = kwds["rawdatainside"]
            del kwds["rawdatainside"]
        else:
            # Wrap a SISField by default.
            self.rawdatainside = False

        # Parse keyword parameters.
        SISFieldSpecial.__init__(self, **kwds)

        # Check that all required instance variables are set.
        if self.CompressionAlgorithm == None or self.Data == None:
            raise AttributeError("missing '%s' or '%s' attribute for '%s'" %
                                 ("CompressionAlgorithm", "Data",
                                  self.__class__.__name__))

        # Check that the compression algorithm is a known one.
        if self.CompressionAlgorithm not in (ECompressAuto, ECompressNone,
                                             ECompressDeflate):
            raise TypeError("invalid CompressionAlgorithm '%d'" %
                            self.CompressionAlgorithm)

    def fromstring(self, string):
        # Parse field header.
        ftype, hdrlen, flen, padlen = parsesisfieldheader(string,
                                                          self.fieldtype)

        if flen < 12:
            raise SISException("SISCompressed contents too short")

        compalgo, uncomplen = struct.unpack("<LQ", string[hdrlen:(hdrlen + 12)])

        if compalgo == ECompressNone:
            # No compression, use as-is.
            dstring = string[(hdrlen + 12):(hdrlen + flen)]
        elif compalgo == ECompressDeflate:
            # RFC1950 (zlib header and checksum) compression, decompress.
            dstring = zlib.decompress(string[(hdrlen + 12):(hdrlen + flen)])
        else:
            raise SISException("invalid SISCompressed algorithm '%d'" %
                               compalgo)

        if uncomplen != len(dstring):
            raise SISException(
                "SISCompressed uncompressed data length mismatch")

        if self.rawdatainside:
            # Raw data inside
            self.Data = dstring
        else:
            # SISField inside
            if dstring != "":
                # Construct a SISField out of the decompressed data.
                self.Data = SISField(dstring)
            else:
                # Decompressed to nothing, duh!
                self.Data = None

        self.CompressionAlgorithm = compalgo

    def tostring(self):
        if self.rawdatainside:
            # Raw data inside
            string = self.Data
        else:
            # SISField inside
            if self.Data != None:
                # Compress the enclosed SISField.
                string = self.Data.tostring()
            else:
                # No data inside, compress an empty string.
                string = ""

        # Compress or not, depending on selected algorithm.
        if self.CompressionAlgorithm in (ECompressAuto, ECompressDeflate):
            cstring = zlib.compress(string, 9)  # Maximum compression
            compalgo = ECompressDeflate

        if self.CompressionAlgorithm == ECompressAuto:
            if len(cstring) >= len(string):
                # Compression is not beneficial, use data as-is.
                cstring = string
                compalgo = ECompressNone
        elif self.CompressionAlgorithm == ECompressNone:
            # No compression, simply use data as-is.
            cstring = string
            compalgo = ECompressNone
        elif self.CompressionAlgorithm == ECompressDeflate:
            # Already handled above.
            pass
        else:
            raise SISException("invalid SISCompressed algorithm '%d'" %
                               self.CompressionAlgorithm)

        # Construct the SISCompressed and SISField headers.
        chdr = struct.pack("<LQ", compalgo, len(string))
        fhdr = makesisfieldheader(self.fieldtype, len(chdr) + len(cstring))
        fpad = makesisfieldpadding(len(cstring))

        del string      # Try to free some memory early.

        # TODO: Heavy on memory, optimize (new string type with concat.)
        return "%s%s%s%s" % (fhdr, chdr, cstring, fpad)

    def __str__(self):
        dtype = (self.rawdatainside and "raw data") or "SISField"
        compalgo = ("not compressed",
                    "compressed with \"deflate\"")[self.CompressionAlgorithm]
        return "<SISCompressed %s, %s>" % (dtype, compalgo)

class SISBlob(SISFieldSpecial):
    '''Arbitrary binary data holder'''
    def __init__(self, **kwds):
        # Set default values.
        self.Data = None

        # Parse keyword parameters.
        SISFieldSpecial.__init__(self, **kwds)

        # Check that all required instance variables are set.
        if self.Data == None:
            raise AttributeError("missing '%s' attribute for '%s'" %
                                 ("Data", self.__class__.__name__))

    def fromstring(self, string):
        ftype, hdrlen, flen, padlen = parsesisfieldheader(string,
                                                          self.fieldtype)

        # Does not get any simpler than this.
        self.Data = string[hdrlen:(hdrlen + flen)]

    def tostring(self):
        # TODO: Heavy on memory, optimize (new string type with concat.)
        return "%s%s%s" % (makesisfieldheader(self.fieldtype, len(self.Data)),
                           self.Data, makesisfieldpadding(len(self.Data)))

    def __str__(self):
        return u"<SISBlob, %d bytes>" % len(self.Data)

class SISFileData(SISFieldSpecial):
    '''File binary data holder (wraps a special SISCompressed SISField)'''
    def __init__(self, **kwds):
        # Create a special SISCompressed object.
        self.FileData = SISCompressed(CompressionAlgorithm = ECompressNone,
                                      Data = "", rawdatainside = True)

        # Parse keyword parameters.
        SISFieldSpecial.__init__(self, **kwds)

    def fromstring(self, string):
        # Parse field header.
        ftype, hdrlen, flen, padlen = parsesisfieldheader(string,
                                                          self.fieldtype)

        if flen < 20:
            raise SISException("SISFileData contents too short")

        self.FileData.fromstring(string[hdrlen:(hdrlen + flen)])

    def tostring(self):
        string = self.FileData.tostring()

        # TODO: Heavy on memory, optimize (new string type with concat.)
        return "%s%s%s" % (makesisfieldheader(self.fieldtype, len(string)),
                           string, makesisfieldpadding(len(string)))

    def getcompressedlength(self):
        # TODO: This is stupid! Compressing the data just
        # to find the resulting length is not very efficient...
        string = self.FileData.tostring()

        ftype, hdrlen, flen, padlen = parsesisfieldheader(string)

        return (flen - 12)  # SISCompressed has an internal header of 12 bytes.

    def __str__(self):
        return "<SISFileData, %d bytes>" % len(self.FileData.Data)

class SISCapabilities(SISFieldSpecial):
    '''Variable length capability bitmask'''
    def __init__(self, **kwds):
        # Set default values.
        self.Capabilities = None

        # Parse keyword parameters.
        SISFieldSpecial.__init__(self, **kwds)

        # Check that all required instance variables are set.
        if self.Capabilities == None:
            raise AttributeError("missing '%s' attribute for '%s'" %
                                 ("Capabilities", self.__class__.__name__))

        # Check that the bitmask is a multiple of 32 bits.
        if len(self.Capabilities) & 3 != 0:
            raise SISException("capabilities length not a multiple of 32 bits")

    def fromstring(self, string):
        ftype, hdrlen, flen, padlen = parsesisfieldheader(string,
                                                          self.fieldtype)

        caps = string[hdrlen:(hdrlen + flen)]
        if len(caps) & 3 != 0:
            raise SISException("capabilities length not a multiple of 32 bits")

        self.Capabilities = caps

    def tostring(self):
        if len(self.Capabilities) & 3 != 0:
            raise SISException("capabilities length not a multiple of 32 bits")

        return "%s%s" % (makesisfieldheader(self.fieldtype,
                         len(self.Capabilities)), self.Capabilities)


##############################################################################
# Normal SISField subclasses (fields containing only other fields and integers)
##############################################################################

class SISVersion(SISFieldNormal):
    '''Major, minor and build numbers'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Major", self.FTYPE_INTEGRAL, "<l"),
            ("Minor", self.FTYPE_INTEGRAL, "<l"),
            ("Build", self.FTYPE_INTEGRAL, "<l")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISVersion %d, %d, %d>" % (self.Major, self.Minor, self.Build)

class SISVersionRange(SISFieldNormal):
    '''A range of two SISVersions, or optionally only one'''
    def __init__(self, **kwds):
        self.subfields = [
            ("FromVersion", self.FTYPE_MANDATORY, "SISVersion"),
            ("ToVersion",   self.FTYPE_OPTIONAL,  "SISVersion")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        ver1 = "from %d, %d, %d" % (self.FromVersion.Major,
                               self.FromVersion.Minor,
                               self.FromVersion.Build)
        ver2 = "onwards"
        if self.ToVersion:
            ver2 = "to %d, %d, %d" % (self.ToVersion.Major,
                                   self.ToVersion.Minor,
                                   self.ToVersion.Build)
        return "<SISVersionRange %s %s>" % (ver1, ver2)

class SISDate(SISFieldNormal):
    '''Year, month (0-11) and day (1-31)'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Year",  self.FTYPE_INTEGRAL, "<H"),
            ("Month", self.FTYPE_INTEGRAL, "<B"),
            ("Day",   self.FTYPE_INTEGRAL, "<B")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISDate %04d-%02d-%02d>" % (self.Year, self.Month + 1,
                                             self.Day)

class SISTime(SISFieldNormal):
    '''Hours (0-23), minutes (0-59) and seconds (0-59)'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Hours",   self.FTYPE_INTEGRAL, "<B"),
            ("Minutes", self.FTYPE_INTEGRAL, "<B"),
            ("Seconds", self.FTYPE_INTEGRAL, "<B")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISTime %02d:%02d:%02d>" % (
            self.Hours, self.Minutes, self.Seconds)

class SISDateTime(SISFieldNormal):
    '''A bundled SISDate and a SISTime'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Date", self.FTYPE_MANDATORY, "SISDate"),
            ("Time", self.FTYPE_MANDATORY, "SISTime")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISDateTime %04d-%02d-%02d %02d:%02d:%02d>" % (
            self.Date.Year, self.Date.Month, self.Date.Day,
            self.Time.Hours, self.Time.Minutes, self.Time.Seconds)

class SISUid(SISFieldNormal):
    '''A 32-bit Symbian OS UID'''
    def __init__(self, **kwds):
        self.subfields = [("UID1", self.FTYPE_INTEGRAL, "<L")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISUid 0x%08x>" % self.UID1

class SISLanguage(SISFieldNormal):
    '''A Symbian OS language number'''
    def __init__(self, **kwds):
        self.subfields = [("Language", self.FTYPE_INTEGRAL, "<L")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        try:
            lname = symbianutil.langnumtoname[self.Language]
        except KeyError:
            lname = "Unknown"
        return "<SISLanguage %d (%s)>" % (self.Language, lname)

class SISContents(SISFieldNormal):
    '''The root type of a SIS file'''
    def __init__(self, **kwds):
        self.subfields = [
            ("ControllerChecksum", self.FTYPE_OPTIONAL,  "SISControllerChecksum"),
            ("DataChecksum",       self.FTYPE_OPTIONAL,  "SISDataChecksum"),
            ("Controller",         self.FTYPE_MANDATORY, "SISCompressed"),
            ("Data",               self.FTYPE_MANDATORY, "SISData")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        cksum1 = "N/A"
        if self.ControllerChecksum:
            cksum1 = "0x%04x" % self.ControllerChecksum.Checksum
        cksum2 = "N/A"
        if self.DataChecksum:
            cksum2 = "0x%04x" % self.DataChecksum.Checksum
        return "<SISContents, checksums: %s, %s>" % (cksum1, cksum2)

class SISController(SISFieldNormal):
    '''SIS file metadata'''
    def __init__(self, **kwds):
        # Convert a list of signatures to separate parameters
        # so that base class constructor can parse them.
        # Support upto MAXNUMSIGNATURES signature certificates.
        if "Signatures" in kwds:
            signatures = kwds["Signatures"]
            if len(signatures) > MAXNUMSIGNATURES:
                raise ValueError("too many signatures for SISController")
            for n in xrange(len(signatures)):
                kwds["Signature%d" % n] = signatures[n]
            del kwds["Signatures"]

        # DataIndex is really not optional. However, calculating
        # signatures require that SISController strings without
        # the DataIndex field can be generated.
        self.subfields = [
            ("Info",          self.FTYPE_MANDATORY, "SISInfo"),
            ("Options",       self.FTYPE_MANDATORY, "SISSupportedOptions"),
            ("Languages",     self.FTYPE_MANDATORY, "SISSupportedLanguages"),
            ("Prerequisites", self.FTYPE_MANDATORY, "SISPrerequisites"),
            ("Properties",    self.FTYPE_MANDATORY, "SISProperties"),
            ("Logo",          self.FTYPE_OPTIONAL,  "SISLogo"),
            ("InstallBlock",  self.FTYPE_MANDATORY, "SISInstallBlock"),
            ("Signature0",    self.FTYPE_OPTIONAL,  "SISSignatureCertificateChain"),
            ("Signature1",    self.FTYPE_OPTIONAL,  "SISSignatureCertificateChain"),
            ("Signature2",    self.FTYPE_OPTIONAL,  "SISSignatureCertificateChain"),
            ("Signature3",    self.FTYPE_OPTIONAL,  "SISSignatureCertificateChain"),
            ("Signature4",    self.FTYPE_OPTIONAL,  "SISSignatureCertificateChain"),
            ("Signature5",    self.FTYPE_OPTIONAL,  "SISSignatureCertificateChain"),
            ("Signature6",    self.FTYPE_OPTIONAL,  "SISSignatureCertificateChain"),
            ("Signature7",    self.FTYPE_OPTIONAL,  "SISSignatureCertificateChain"),
            ("DataIndex",     self.FTYPE_OPTIONAL,  "SISDataIndex")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    # Helper routines to deal with the special signature fields.
    def getsignatures(self):
        # Return signatures as a list.
        signatures = []
        for n in xrange(MAXNUMSIGNATURES):
            sig = self.__dict__["Signature%d" % n]
            if sig != None:
                signatures.append(sig)
        return signatures

    def setsignatures(self, signatures):
        # Replace signatures with the ones from list. If there are
        # less than MAXNUMSIGNATURES signatures in the list, the
        # rest are erased. To erase all signatures, call
        # controller.setsignatures([]).
        numsig = len(signatures)
        if numsig > MAXNUMSIGNATURES:
            raise ValueError("too many signatures for SISController")
        for n in xrange(MAXNUMSIGNATURES):
            if n < numsig:
                sig = signatures[n]
            else:
                sig = None
            self.__dict__["Signature%d" % n] = sig

class SISInfo(SISFieldNormal):
    '''Information about the SIS file'''
    def __init__(self, **kwds):
        self.subfields = [
            ("UID",              self.FTYPE_MANDATORY, "SISUid"),
            ("VendorUniqueName", self.FTYPE_MANDATORY, "SISString"),
            ("Names",            self.FTYPE_ARRAY,     "SISString"),
            ("VendorNames",      self.FTYPE_ARRAY,     "SISString"),
            ("Version",          self.FTYPE_MANDATORY, "SISVersion"),
            ("CreationTime",     self.FTYPE_MANDATORY, "SISDateTime"),
            ("InstallType",      self.FTYPE_INTEGRAL,  "<B"),
            ("InstallFlags",     self.FTYPE_INTEGRAL,  "<B")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISSupportedLanguages(SISFieldNormal):
    '''An array of SISLanguage fields'''
    def __init__(self, **kwds):
        self.subfields = [("Languages", self.FTYPE_ARRAY, "SISLanguage")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISSupportedOptions(SISFieldNormal):
    '''An array of SISSupportedOption fields, user selectable options'''
    def __init__(self, **kwds):
        self.subfields = [("Options", self.FTYPE_ARRAY, "SISSupportedOption")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISPrerequisites(SISFieldNormal):
    '''An array of SISDependency fields'''
    def __init__(self, **kwds):
        self.subfields = [
            ("TargetDevices", self.FTYPE_ARRAY, "SISDependency"),
            ("Dependencies",  self.FTYPE_ARRAY, "SISDependency")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISDependency(SISFieldNormal):
    '''Versioned SIS package dependency'''
    def __init__(self, **kwds):
        self.subfields = [
            ("UID",             self.FTYPE_MANDATORY, "SISUid"),
            ("VersionRange",    self.FTYPE_OPTIONAL,  "SISVersionRange"),
            ("DependencyNames", self.FTYPE_ARRAY,     "SISString")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISProperties(SISFieldNormal):
    '''An array of SISProperty fields'''
    def __init__(self, **kwds):
        self.subfields = [("Properties", self.FTYPE_ARRAY, "SISProperty")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISProperty(SISFieldNormal):
    '''Key:value pair'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Key",   self.FTYPE_INTEGRAL, "<l"),
            ("Value", self.FTYPE_INTEGRAL, "<l")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

# SISSignatures: Legacy field type, not used
#
# class SISSignatures(SISFieldNormal):
#     pass

class SISCertificateChain(SISFieldNormal):
    '''ASN.1 encoded X509 certificate chain'''
    def __init__(self, **kwds):
        self.subfields = [("CertificateData", self.FTYPE_MANDATORY, "SISBlob")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISLogo(SISFieldNormal):
    '''A logo file to display during installation'''
    def __init__(self, **kwds):
        self.subfields = [
            ("LogoFile", self.FTYPE_MANDATORY, "SISFileDescription")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISFileDescription(SISFieldNormal):
    '''Information about an enclosed file'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Target",             self.FTYPE_MANDATORY, "SISString"),
            ("MIMEType",           self.FTYPE_MANDATORY, "SISString"),
            ("Capabilities",       self.FTYPE_OPTIONAL,  "SISCapabilities"),
            ("Hash",               self.FTYPE_MANDATORY, "SISHash"),
            ("Operation",          self.FTYPE_INTEGRAL,  "<L"),
            ("OperationOptions",   self.FTYPE_INTEGRAL,  "<L"),
            ("Length",             self.FTYPE_INTEGRAL,  "<Q"),
            ("UncompressedLength", self.FTYPE_INTEGRAL,  "<Q"),
            ("FileIndex",          self.FTYPE_INTEGRAL,  "<L")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISHash(SISFieldNormal):
    '''File hash'''
    def __init__(self, **kwds):
        self.subfields = [
            ("HashAlgorithm", self.FTYPE_INTEGRAL,  "<L"),
            ("HashData",      self.FTYPE_MANDATORY, "SISBlob")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

        # Check that the hash algorithm is a supported one (SHA-1 only for now).
        if self.HashAlgorithm != ESISHashAlgSHA1:
            raise SISException("invalid SISHash algorithm '%d'" %
                               self.HashAlgorithm)

class SISIf(SISFieldNormal):
    '''An "if"-branch of a conditional expression'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Expression",   self.FTYPE_MANDATORY, "SISExpression"),
            ("InstallBlock", self.FTYPE_MANDATORY, "SISInstallBlock"),
            ("ElseIfs",      self.FTYPE_ARRAY,     "SISElseIf")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISElseIf(SISFieldNormal):
    '''An "else if"-branch of a conditional expression'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Expression",   self.FTYPE_MANDATORY, "SISExpression"),
            ("InstallBlock", self.FTYPE_MANDATORY, "SISInstallBlock")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISInstallBlock(SISFieldNormal):
    '''A conditional file installation hierarchy'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Files",            self.FTYPE_ARRAY, "SISFileDescription"),
            ("EmbeddedSISFiles", self.FTYPE_ARRAY, "SISController"),
            ("IfBlocks",         self.FTYPE_ARRAY, "SISIf")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISExpression(SISFieldNormal):
    '''A conditional expression'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Operator",        self.FTYPE_INTEGRAL, "<L"),
            ("IntegerValue",    self.FTYPE_INTEGRAL, "<l"),
            ("StringValue",     self.FTYPE_OPTIONAL, "SISString"),
            ("LeftExpression",  self.FTYPE_OPTIONAL, "SISExpression"),
            ("RightExpression", self.FTYPE_OPTIONAL, "SISExpression")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISData(SISFieldNormal):
    '''An array of SISDataUnit fields'''
    def __init__(self, **kwds):
        self.subfields = [("DataUnits", self.FTYPE_ARRAY, "SISDataUnit")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISDataUnit(SISFieldNormal):
    '''An array of SISFileData fields'''
    def __init__(self, **kwds):
        self.subfields = [("FileData", self.FTYPE_ARRAY, "SISFileData")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISSupportedOption(SISFieldNormal):
    '''An array of supported option names in different languages'''
    def __init__(self, **kwds):
        self.subfields = [("Names", self.FTYPE_ARRAY, "SISString")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISControllerChecksum(SISFieldNormal):
    '''CCITT CRC-16 of the SISController SISField'''
    def __init__(self, **kwds):
        self.subfields = [("Checksum", self.FTYPE_INTEGRAL, "<H")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISControllerChecksum 0x%04x>" % self.Checksum

class SISDataChecksum(SISFieldNormal):
    '''CCITT CRC-16 of the SISData SISField'''
    def __init__(self, **kwds):
        self.subfields = [("Checksum", self.FTYPE_INTEGRAL, "<H")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISDataChecksum 0x%04x>" % self.Checksum

class SISSignature(SISFieldNormal):
    '''Cryptographic signature of preceding SIS metadata'''
    def __init__(self, **kwds):
        self.subfields = [
            ("SignatureAlgorithm", self.FTYPE_MANDATORY, "SISSignatureAlgorithm"),
            ("SignatureData",      self.FTYPE_MANDATORY, "SISBlob")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISSignatureAlgorithm(SISFieldNormal):
    '''Object identifier string of a signature algorithm'''
    def __init__(self, **kwds):
        self.subfields = [
            ("AlgorithmIdentifier", self.FTYPE_MANDATORY, "SISString")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISSignatureAlgorithm '%s'>" % (
            self.AlgorithmIdentifier.String)

class SISSignatureCertificateChain(SISFieldNormal):
    '''An array of SISSignatures and a SIScertificateChain
    for signature validation'''
    def __init__(self, **kwds):
        self.subfields = [
            ("Signatures",       self.FTYPE_ARRAY,     "SISSignature"),
            ("CertificateChain", self.FTYPE_MANDATORY, "SISCertificateChain")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

class SISDataIndex(SISFieldNormal):
    '''Data index for files belonging to a SISController'''
    def __init__(self, **kwds):
        self.subfields = [("DataIndex", self.FTYPE_INTEGRAL, "<L")]

        # Parse keyword parameters.
        SISFieldNormal.__init__(self, **kwds)

    def __str__(self):
        return "<SISDataIndex %d>" % self.DataIndex


##############################################################################
# Utility dictionaries
##############################################################################

fieldinfo = [
    (1,     "SISString",                    SISString),
    (2,     "SISArray",                     SISArray),
    (3,     "SISCompressed",                SISCompressed),
    (4,     "SISVersion",                   SISVersion),
    (5,     "SISVersionRange",              SISVersionRange),
    (6,     "SISDate",                      SISDate),
    (7,     "SISTime",                      SISTime),
    (8,     "SISDateTime",                  SISDateTime),
    (9,     "SISUid",                       SISUid),
    (11,    "SISLanguage",                  SISLanguage),
    (12,    "SISContents",                  SISContents),
    (13,    "SISController",                SISController),
    (14,    "SISInfo",                      SISInfo),
    (15,    "SISSupportedLanguages",        SISSupportedLanguages),
    (16,    "SISSupportedOptions",          SISSupportedOptions),
    (17,    "SISPrerequisites",             SISPrerequisites),
    (18,    "SISDependency",                SISDependency),
    (19,    "SISProperties",                SISProperties),
    (20,    "SISProperty",                  SISProperty),
# SISSignatures: Legacy field type, not used
#    (21,    "SISSignatures",                SISSignatures),
    (22,    "SISCertificateChain",          SISCertificateChain),
    (23,    "SISLogo",                      SISLogo),
    (24,    "SISFileDescription",           SISFileDescription),
    (25,    "SISHash",                      SISHash),
    (26,    "SISIf",                        SISIf),
    (27,    "SISElseIf",                    SISElseIf),
    (28,    "SISInstallBlock",              SISInstallBlock),
    (29,    "SISExpression",                SISExpression),
    (30,    "SISData",                      SISData),
    (31,    "SISDataUnit",                  SISDataUnit),
    (32,    "SISFileData",                  SISFileData),
    (33,    "SISSupportedOption",           SISSupportedOption),
    (34,    "SISControllerChecksum",        SISControllerChecksum),
    (35,    "SISDataChecksum",              SISDataChecksum),
    (36,    "SISSignature",                 SISSignature),
    (37,    "SISBlob",                      SISBlob),
    (38,    "SISSignatureAlgorithm",        SISSignatureAlgorithm),
    (39,    "SISSignatureCertificateChain", SISSignatureCertificateChain),
    (40,    "SISDataIndex",                 SISDataIndex),
    (41,    "SISCapabilities",              SISCapabilities)
]

fieldnumtoclass = dict([(num,  klass) for num, name, klass in fieldinfo])
fieldnametonum  = dict([(name, num)   for num, name, klass in fieldinfo])
fieldnumtoname  = dict([(num,  name)  for num, name, klass in fieldinfo])
