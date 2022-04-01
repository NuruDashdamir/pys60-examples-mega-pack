#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# rscfile.py - Symbian OS compiled resource file (RSC) utilities
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

import symbianutil


##############################################################################
# Module-level functions which are normally only used by this module
##############################################################################

def makeuidfromoffset(offset):
    '''Convert a Symbian OS resource file offset to a UID.

    ---- From rcomp v7.01 source ----
    space: 0, A: 1, B: 2, ..., Z: 26

    ABCD corresponds to the number 4321 which becomes
    ((4*27 + 3) * 27 + 2) * 27 + 1.
    ----                         ----

    The description above contains an error. The actual situation
    is reversed: ABCD corresponds to the number 1234 which results in
    ((1*27 + 2) * 27 + 3) * 27 + 4.
    '''

    if len(offset) not in range(1, 5):
        raise ValueError("offset must be four characters or less")
    uid = 0L
    offset = offset.upper()
    for c in offset:
        try:
            ordc = " ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(c)
        except ValueError:
            raise ValueError("invalid character '%s' in offset" % c)
        uid *= 27
        uid += ordc
    return uid


##############################################################################
# Resource class for containing binary fields
##############################################################################

class Resource(object):
    '''A Symbian OS resource type

    Limitations:

    - Write only
    - Available types are limited to BYTE, WORD, LONG, LLINK and LTEXT.
    - Unicode compression is not supported.'''

    def __init__(self, fieldtypes, *args):
        self.fieldtypes = fieldtypes
        self.fieldvalues = []

        if len(self.fieldtypes) != len(args):
            raise ValueError("invalid number of field values")

        offset = 0
        for n in xrange(len(args)):
            ftype = self.fieldtypes[n]
            fval = args[n]
            if ftype == "BYTE":
                if fval < 0:
                    fval += 0x100
                if fval < 0 or fval > 255:
                    raise ValueError("byte integer too large")
                self.fieldvalues.append(struct.pack("<B", fval))
                offset += 1
            elif ftype == "WORD":
                if fval < 0:
                    fval += 0x10000
                if fval < 0 or fval > 65535:
                    raise ValueError("word integer too large")
                self.fieldvalues.append(struct.pack("<H", fval))
                offset += 2
            elif ftype == "LONG" or ftype == "LLINK":
                if fval < 0:
                    fval += 0x100000000L
                if fval < 0 or fval > 4294967295:
                    raise ValueError("long integer too large")
                self.fieldvalues.append(struct.pack("<L", fval))
                offset += 4
            elif ftype == "LTEXT":
                if len(fval) > 255:
                    raise ValueError("Unicode string too long")
                self.fieldvalues.append(struct.pack("<B", len(fval)))
                offset += 1
                if len(fval) > 0:
                    if (offset & 1) != 0:
                        # Odd offset. Add padding byte (only if length > 0).
                        self.fieldvalues.append(struct.pack("B", 0xab))
                        offset += 1
                    fval_enc = fval.encode("UTF-16LE")
                    self.fieldvalues.append(fval_enc)
                    offset += len(fval_enc)

            # TODO: Arrays, recursive structs
            # TODO: TEXT, DOUBLE, BUF, BUF8, BUF<n>, LINK, SRLINK

    def tostring(self):
        return "".join(self.fieldvalues)

    # TODO: fromstring()


##############################################################################
# RSCWriter class for creating Symbian OS compiled resource files (RSC)
##############################################################################

class RSCWriter(object):
    '''A Symbian OS compiled resource file (RSC) file generator

    Limitations:

    - Output format is always "Compressed Unicode resource format".
    - Despite the format name, nothing is compressed.'''

    def __init__(self, uid2, uid3 = None, offset = None):
        self.resources = []

        if ((uid3 == None and offset == None) or
            (uid3 != None and offset != None)):
            raise AttributeError("one of uid3 or offset required, not both")

        self.flags = 0x00
        if offset != None:
            try:
                uid3 = makeuidfromoffset(offset)
            except:
                raise ValueError("invalid offset '%s'" % offset)
            self.flags = 0x01

        self.uid2 = uid2
        self.uid3 = uid3

    def addresource(self, resource):
        self.addrawresource(resource.tostring())

    def addrawresource(self, string):
        self.resources.append(string)

    def tostring(self):
        # UIDs (UID1 always 0x101f4a6b)
        fields = [symbianutil.uidstostring(0x101f4a6bL, self.uid2, self.uid3)]

        # Flags
        fields.append(struct.pack("<B", self.flags))

        # Longest resource (to be updated)
        fields.append("\0\0")

        # Unicode compression bitmap (no compression)
        fields.append("\0" * ((len(self.resources) + 7) / 8))

        # Resource contents
        offsets = []
        foffset = len("".join(fields))
        maxrlen = 0
        for res in self.resources:
            # Find longest resource.
            rlen = len(res)
            if rlen > maxrlen:
                maxrlen = rlen
            offsets.append(foffset)
            fields.append(res)
            foffset += rlen
        offsets.append(foffset)

        # Update longest resource.
        fields[2] = struct.pack("<H", maxrlen)

        # Resource index
        for off in offsets:
            fields.append(struct.pack("<H", off))

        # TODO: Ineffiecient. Improve.
        return "".join(fields)
