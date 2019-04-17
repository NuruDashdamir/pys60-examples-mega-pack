#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# miffile.py - Symbian OS multi-image format (MIF) utilities
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


##############################################################################
# MIFWriter class for grouping SVG-T items into MIF files
##############################################################################

class MIFWriter(object):
    '''A MIF file generator

    Limitations:

    - MBM file linkage is not supported.
    - Flags and other unknown fields are filled with guessed values.'''

    def __init__(self):
        self.fileinfo       = []
        self.filedata       = []

    def addfile(self, contents, animate = False):
        self.filedata.append(contents)
        self.fileinfo.append((animate and 1) or 0)

    def tostring(self):
        # Generate header.
        strdata = ["B##4", struct.pack("<LLL", 2, 16, len(self.filedata) * 2)]

        # Generate indexes.
        offset = 16 + 16 * len(self.filedata)
        for n in xrange(len(self.filedata)):
            clen = len(self.filedata[n]) + 32   # Including header length
            strdata.append(struct.pack("<LLLL", offset, clen, offset, clen))
            offset += clen

        # Generate contents.
        for n in xrange(len(self.filedata)):
            clen = len(self.filedata[n])        # Not including header length
            strdata.append("C##4")
            strdata.append(struct.pack("<LLLLLLL", 1, 32, clen,
                                       1, 0, self.fileinfo[n], 0))
            strdata.append(self.filedata[n])

        # TODO: Ineffiecient. Improve.
        return "".join(strdata)
