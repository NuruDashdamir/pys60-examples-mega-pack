#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# cmd_version.py - Ensymble command line tool, version query command
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


##############################################################################
# Help texts
##############################################################################

shorthelp = "Print Ensymble version"
longhelp  = '''version

Print Ensymble version.
'''


##############################################################################
# Public module-level functions
##############################################################################

def run(pgmname, argv):
    print "Ensymble v0.28 2009-01-30"
