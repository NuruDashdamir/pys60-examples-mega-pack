#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# symbianutil.py - Utilities for working with Symbian OS-related data
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

import struct
import zlib


##############################################################################
# Miscellaneous functions
##############################################################################

def uidstostring(uid1, uid2, uid3):
    '''Return a string of UIDs and a checksum.'''

    crc = uidcrc(uid1, uid2, uid3)
    return struct.pack("<LLLL", uid1, uid2, uid3, crc)

def ise32image(string):
    '''Check if a given string contains a valid E32Image header.
    Return "EXE", "DLL" or None.'''

    if len(string) < 156:
        # Minimum header size is 156 bytes.
        return None

    if string[16:20] != "EPOC":
        # Wrong cookie, not an E32Image header.
        return None

    # Get UIDs as integers.
    uid1, uid2, uid3 = struct.unpack("<LLL", string[:12])

    # Verify UID checksum.
    uidstr = uidstostring(uid1, uid2, uid3)
    if uidstr != string[:16]:
        # Invalid UID checksum.
        return None

    # Check type of E32Image header.
    if uid1 == 0x10000079L:
        return "DLL"
    elif uid1 == 0x1000007AL:
        return "EXE"

    # Not an EXE or DLL.
    return None

def e32imageinfo(image):
    '''Return a tuple with the UID1, UID2, UID3, secure ID, vendor ID and
    capabilities (as a string) of the given e32image.'''

    if ise32image(image) == None:
        raise ValueError("not a valid e32image header")

    uid1, uid2, uid3 = struct.unpack("<LLL", image[:12])
    secureid = struct.unpack("<L", image[128:132])[0]
    vendorid = struct.unpack("<L", image[132:136])[0]
    capabilities = struct.unpack("<Q", image[136:144])[0]

    return (uid1, uid2, uid3, secureid, vendorid, capabilities)

def parseintmagnitude(string):
    '''Parse an integer and a magnitude. Magnitude can be "k" or "M" (case
    is not important). There may be no white-space between the integer and
    magnitude. Magnitudes are interpreted as 1024 and 1048576.'''

    string = string.lower()

    if string[-1] == "k":
        magnitude = 1024
        string = string[:-1]
    elif string[-1] == "m":
        magnitude = 1024 * 1024
        string = string[:-1]
    else:
        magnitude = 1

    return int(string, 10) * magnitude

def uidfromname(basename):
    '''Generate a test-range UID (0xe0000000 to 0xefffffff) from a
    Unicode name.'''

    # Normalise case.
    basename = basename.lower()

    # Convert Unicode name to an unambiguous byte string.
    basename = basename.encode("utf8")

    # Calculate a 32-bit CCITT CRC and set top four bits to "e".
    return (crc32ccitt(basename) & 0x0fffffffL) | 0xe0000000L

def e32imagecaps(string):
    '''Check if a given string is an E32Image file and return its
    capabilities or None if not an E32Image.

    Returned value can be directly used as the "capabilities"
    attribute of sisfile.SimpleSISWriter().addfile() call.'''

    if ise32image(string) == None:
        return None

    return struct.unpack("<Q", string[136:144])[0]


##############################################################################
# Checksum functions for various types of checksums in Symbian OS
##############################################################################

def crc16ccitt(string, initialvalue = 0x0000, finalxor = 0x0000):
    '''Calculate a CCITT CRC-16 checksum using a
    slow and straightforward algorithm.'''

    value = initialvalue
    for c in string:
        value ^= (ord(c) << 8)
        for b in xrange(8):
            value <<= 1
            if value & 0x10000:
                value ^= 0x1021
            value &= 0xffff

    return value ^ finalxor

def crc32ccitt(data, initialvalue = 0x00000000L, finalxor = 0x00000000L):
    '''Use zlib to calculate a CCITT CRC-32 checksum. Work around zlib
    signedness problems.'''

    if initialvalue >= 0x80000000L:
        initialvalue -= 0x100000000L
    initialvalue = int(initialvalue)

    value = long(zlib.crc32(data, initialvalue))

    if value < 0:
        value += 0x100000000L

    return value ^ finalxor

def uidcrc(uid1, uid2, uid3):
    '''Calculate a Symbian OS UID checksum.'''

    # Convert UIDs to a string and group even and odd characters
    # into separate strings (in a Python v2.2 compatible way).
    uidstr = struct.pack("<LLL", uid1, uid2, uid3)
    evenchars = "".join([uidstr[n] for n in range(0, 12, 2)])
    oddchars  = "".join([uidstr[n] for n in range(1, 12, 2)])

    # Calculate 16-bit CCITT CRCs for even and odd characters.
    evencrc = crc16ccitt(evenchars)
    oddcrc  = crc16ccitt(oddchars)

    # Resulting 32-bit UID CRC is a combination of the two 16-bit CCITT CRCs.
    return (long(oddcrc) << 16) | evencrc

def e32imagecrc(image, uid3 = None, secureid = None, vendorid = None,
                heapsizemin = None, heapsizemax = None, capabilities = None):
    '''Return a modified e32image (or just the header) with UID checksum
    and header checksum (CCITT CRC-32) recalculated. Optionally modify
    the UID3, secure ID, vendor ID, heap size and capability bit mask.'''

    if ise32image(image) == None:
        raise ValueError("not a valid e32image header")

    # Get original UIDs as integers.
    uid1, uid2, uid3_orig = struct.unpack("<LLL", image[:12])

    # Get modified or original IDs depending on parameters. Convert to strings.
    if uid3 == None:
        uid3 = uid3_orig
    uid3str = struct.pack("<L", uid3)

    if secureid == None:
        secureidstr = image[128:132]
    else:
        secureidstr = struct.pack("<L", secureid)

    if vendorid == None:
        vendoridstr = image[132:136]
    else:
        vendoridstr = struct.pack("<L", vendorid)

    if heapsizemin == None:
        heapsizeminstr = image[56:60]
    else:
        heapsizeminstr = struct.pack("<l", heapsizemin)

    if heapsizemax == None:
        heapsizemaxstr = image[60:64]
    else:
        heapsizemaxstr = struct.pack("<l", heapsizemax)

    if capabilities == None:
        capabilitiesstr = image[136:144]
    else:
        capabilitiesstr = struct.pack("<Q", capabilities)

    # Re-calculate UID checksum.
    uidstr = uidstostring(uid1, uid2, uid3)

    # Use initial CRC of 0xc90fdaa2L (KImageCrcInitialiser in f32image.h).
    initialcrcstr = struct.pack("<L", 0xc90fdaa2L)

    # Construct a new header for CRC-32 calculation.
    newheader = "%s%s%s%s%s%s%s%s%s%s%s" % (uidstr, image[16:20], initialcrcstr,
                                            image[24:56], heapsizeminstr,
                                            heapsizemaxstr, image[64:128],
                                            secureidstr, vendoridstr,
                                            capabilitiesstr, image[144:156])

    crc32 = crc32ccitt(newheader, 0xffffffffL, 0xffffffffL)
    crc32str = struct.pack("<L", crc32)

    # Construct and return a new image (or header) with the correct checksum.
    return "%s%s%s%s" % (newheader[0:20], crc32str,
                         newheader[24:156], image[156:])


##############################################################################
# Symbian OS language mappings
##############################################################################

langinfo = [
    ("AF", "Afrikaans",             34),
    ("SQ", "Albanian",              35),
    ("AM", "AmericanEnglish",       10),
    ("AH", "Amharic",               36),
    ("AR", "Arabic",                37),
    ("HY", "Armenian",              38),
    ("AU", "Australian",            20),
    ("AS", "Austrian",              22),
    ("BE", "Belarussian",           40),
    ("BL", "BelgianFlemish",        19),
    ("BF", "BelgianFrench",         21),
    ("BN", "Bengali",               41),
    ("BP", "BrazilianPortuguese",   76),
    ("BG", "Bulgarian",             42),
    ("MY", "Burmese",               43),
    ("CE", "CanadianEnglish",       46),
    ("CF", "CanadianFrench",        51),
    ("CA", "Catalan",               44),
    ("HR", "Croatian",              45),
    ("CG", "CyprusGreek",           55),
    ("CT", "CyprusTurkish",         91),
    ("CS", "Czech",                 25),
    ("DA", "Danish",                7),
    ("DU", "Dutch",                 18),
    ("EN", "English",               1),
    ("ET", "Estonian",              49),
    ("FA", "Farsi",                 50),
    ("FS", "FinlandSwedish",        85),
    ("FI", "Finnish",               9),
    ("FR", "French",                2),
    ("KA", "Georgian",              53),
    ("GE", "German",                3),
    ("EL", "Greek",                 54),
    ("GU", "Gujarati",              56),
    ("HE", "Hebrew",                57),
    ("HI", "Hindi",                 58),
    ("HK", "HongKongChinese",       30),
    ("HU", "Hungarian",             17),
    ("IC", "Icelandic",             15),
    ("IN", "Indonesian",            59),
    ("IE", "InternationalEnglish",  47),
    ("IF", "InternationalFrench",   24),
    ("OS", "InternationalSpanish",  82),
    ("GA", "Irish",                 60),
    ("IT", "Italian",               5),
    ("JA", "Japanese",              32),
    ("KN", "Kannada",               62),
    ("KK", "Kazakh",                63),
    ("KM", "Khmer",                 64),
    ("KO", "Korean",                65),
    ("LO", "Laothian",              66),
    ("LS", "LatinAmericanSpanish",  83),
    ("LV", "Latvian",               67),
    ("LT", "Lithuanian",            68),
    ("MK", "Macedonian",            69),
    ("MS", "Malay",                 70),
    ("ML", "Malayalam",             71),
    ("MR", "Marathi",               72),
    ("MO", "Moldavian",             73),
    ("MN", "Mongolian",             74),
    ("NZ", "NewZealand",            23),
    ("NO", "Norwegian",             8),
    ("NN", "NorwegianNynorsk",      75),
    ("PL", "Polish",                27),
    ("PO", "Portuguese",            13),
    ("ZH", "PRCChinese",            31),
    ("PA", "Punjabi",               77),
    ("RO", "Romanian",              78),
    ("RU", "Russian",               16),
    ("GD", "ScotsGaelic",           52),
    ("SR", "Serbian",               79),
    ("SI", "Sinhalese",             80),
    ("SK", "Slovak",                26),
    ("SL", "Slovenian",             28),
    ("SO", "Somali",                81),
    ("SF", "SouthAfricanEnglish",   48),    # "SF" is also "SwissFrench"
    ("SP", "Spanish",               4),
    ("SH", "Swahili",               84),
    ("SW", "Swedish",               6),
    ("SF", "SwissFrench",           11),    # "SF" is also "SouthAfricanEnglish"
    ("SG", "SwissGerman",           12),
    ("SZ", "SwissItalian",          61),
    ("TL", "Tagalog",               39),
    ("TC", "TaiwanChinese",         29),
    ("TA", "Tamil",                 87),
    ("TE", "Telugu",                88),
    ("TH", "Thai",                  33),
    ("BO", "Tibetan",               89),
    ("TI", "Tigrinya",              90),
    ("TU", "Turkish",               14),
    ("TK", "Turkmen",               92),
    ("UK", "Ukrainian",             93),
    ("UR", "Urdu",                  94),
    ("VI", "Vietnamese",            96),
    ("CY", "Welsh",                 97),
    ("ZU", "Zulu",                  98)
]

langidtonum     = dict([(lid,   lnum)  for lid, lname, lnum in langinfo])
langnametonum   = dict([(lname, lnum)  for lid, lname, lnum in langinfo])
langnumtoname   = dict([(lnum,  lname) for lid, lname, lnum in langinfo])


##############################################################################
# Symbian OS capabilities
##############################################################################

capinfo = [
    ("TCB",             0),
    ("CommDD",          1),
    ("PowerMgmt",       2),
    ("MultimediaDD",    3),
    ("ReadDeviceData",  4),
    ("WriteDeviceData", 5),
    ("DRM",             6),
    ("TrustedUI",       7),
    ("ProtServ",        8),
    ("DiskAdmin",       9),
    ("NetworkControl",  10),
    ("AllFiles",        11),
    ("SwEvent",         12),
    ("NetworkServices", 13),
    ("LocalServices",   14),
    ("ReadUserData",    15),
    ("WriteUserData",   16),
    ("Location",        17),
    ("SurroundingsDD",  18),
    ("UserEnvironment", 19)
]

numcaps = 20
allcapsmask = (1L << numcaps) - 1

capnametonum = dict([(cname.lower(), cnum) for cname, cnum in capinfo])

def capstringtomask(string):
    '''Parse a capability string in which capability
    names are separated with + (include capability)
    and - (exclude capability).'''

    if string == "":
        # Empty string denotes no capabilities.
        return 0L

    try:
        # Allow numerical representation for capabilities.
        capmask = int(string, 0)
        if capmask < 0:
            raise ValueError
        return capmask
    except ValueError:
        # Capabilities not in numerical form, continue with parsing.
        pass

    # Erase an optional initial "+" character.
    if string[0] == '+':
        string = string[1:]

    # Split string before each "+" and "-" character.
    startpos = 0
    capnames = []
    for stoppos in xrange(len(string)):
        if string[stoppos] in ("+", "-"):
            capnames.append(string[startpos:stoppos])
            startpos = stoppos
    capnames.append(string[startpos:])  # The last one

    # Add initial "+" for the first name.
    capnames[0] = "+%s" % capnames[0]

    # Find a bit mask for each capability name.
    capmask = 0x00000000L
    for cname in capnames:
        # Convert capability name to lowercase for capnametonum[].
        cnamelower = cname.lower()

        if cnamelower[1:] == "all":
            mask = allcapsmask
        elif cnamelower[1:] == "none":
            mask = 0x00000000L
        else:
            try:
                mask = 1L << (capnametonum[cnamelower[1:]])
            except KeyError:
                raise ValueError("invalid capability name '%s'" % cname[1:])

        if cname[0] == '-':
            # Remove capability.
            capmask &= ~mask
        else:
            # Add capability.
            capmask |= mask

    return capmask

def capmasktostring(capmask, shortest = False):
    '''Generate (optionally) the shortest possible capability
    string using either capability names separated with + (include
    capability) or - (exclude capability).'''

    if capmask == 0L:
        # Special string for no capabilities.
        return "NONE"

    # Construct a list of set and unset capabilities.
    poscnames = []
    negcnames = ["ALL"]
    for cap in capinfo:
        mask = (1L << cap[1])
        if capmask & mask:
            poscnames.append(cap[0])
            capmask &= ~mask
        else:
            negcnames.append(cap[0])

    # Check that all capability bits are handled.
    if capmask != 0L:
        raise ValueError("invalid capability bits in mask: 0x%08x" % capmask)

    posstring = "+".join(poscnames)
    negstring = "-".join(negcnames)

    # Return the shortest string if requested, otherwise the "positive" string.
    if shortest and len(posstring) > len(negstring):
        return negstring
    return posstring

def capmasktorawdata(capmask):
    '''Convert capability bit mask to raw four- or eight-character string.'''

    if capmask < (1L << 32):
        return struct.pack("<L", int(capmask))
    elif capmask < (1L << 64):
        return struct.pack("<Q", capmask)
    else:
        raise ValueError("capability bit mask too long")

def rawdatatocapmask(rawdata):
    '''Convert raw four- or eight-character string to capability bit mask.'''

    if len(rawdata) == 4:
        return struct.unpack("<L", rawdata)[0]
    elif len(rawdata) == 8:
        return struct.unpack("<Q", rawdata)[0]
    else:
        raise ValueError("string length not a multiple of 32 bits")
