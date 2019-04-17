#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# defaultcert.py - Ensymble default certificate and its private key
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

import zlib


##############################################################################
# Default certificate, totally insecure, for testing only!
# Base-64-encoded, zlib-compressed PEM data (which is itself base-64 encoded...)
##############################################################################

cert = '''
    eJxtksuSokAURPd8xeyNDqAF1GW9Ggqo0oICgZ0vEFAR0UH4+tFezGKm7zIjIzLuyfz4eB0kNuW/
    EAkk/aIISPIWPxRGKbIxQiC1C9BTCArqAq8c3GU9VtS9MKDZKGztkG6nWBAIRQQYZE8iwQoWPFYg
    YBKR+LGbnu7p+Xli0EiwBJ8M1wOXxGAV6flX89LYv1pPRhIoDMxtoEcEPBkN1uZ4WOvl1o76Ipv3
    WKSu12T0+HvHwXc6wEWqAUZtFzQ2BB6fKbp/5r43LPPTxjQfzdbaZwJi/rhd9XEsZ7rFh/CpNRPs
    r7XJdbNi5RXZQuNJN9w0PMkV3Ur9Mstb7QHvy3uzOJTVmH8hXF3CaUV970bbeuHLRItMWZ4RaYO6
    mx93k9bTsjYyVko3CYw8S6HlDL2705l/aERYJZE6DJ65N8r5thIgNU1QMAiAXe0xHBjU3m/vcSHW
    CoRhwTfUmoqz4djHY+HWVuuceFJJFY0Qv0k7ISMrDKziB6/y12yR5Aqjb7I/g10jJFDTlfLKjAFl
    46vNd41OwAiUAAPhqD91DowXbXr7LLoGW8DsuvosO6xHahao8WYeKtVCvfOmc2jF9suWWe0tflza
    0bhdzu0jr/noGury5GSpSeGB8Xho05TlexRNpU3UHisnvaF4pu/IvNNEfU1Gui1Xvdt4QmhqF+3l
    /f6ZlUd0rXHdGmxHb+q2y4Ju9lvGT9OaK1SPD7UeL1auZomdGyjfCycc/7/6P+Pc9Q0='''
cert = zlib.decompress(cert.decode("base-64"))


##############################################################################
# Default certificate private key, totally insecure, for testing only!
# Base-64-encoded, zlib-compressed PEM data (which is itself base-64 encoded...)
##############################################################################

privkey = '''
    eJxtk7eSo0AABXO+YnPVFoxAmGADnBB+ECAQGd4jvPv627v4On1Z1+vv7184UZKNr6fNfsGn/GId
    8UsV33+Hb0SXZd7PZY5lVS63+Cpl7FtlH1PV3bwljQbp0nkua53RQCYxTSxMWsX1lKgwP8AMBw+p
    TnmwitoQXpQ+MCzaMWnLE61PzloeOWMI/c+HxncrJ27YTBz8MRxqD20MMHfTJfocKdQ60KDsw6Gc
    pbAxBQrW6ePqsWlBT7xvODw+iOIHAEhP5eKn8ioRGCuZqSULrMVyCPuROFZWRsOOgve4MaSWOWKN
    65f5fCSaQikUnhtDN1Jg8Bu/JA/cKaiYssOgzPuamRHHfknyrb3od4HOMI9+vpX32z0Tuc0acr37
    vMJCahtsLVwkYlwfNYAlLfmbIWQuWm0kUpifh98eRe7yDgY2OQG5TVYo7PggXC1mltY9PwRsUW7B
    6at0z9Yie336tRgoii5SGsK+b0aS7UG9T60WnccaeBdrZcCW35l9rE82vUe5G54HB+xJNh1cA53m
    9XHkeF4EAYXsRrRYh6e4m8KxuqDKTEOmkdRCRZMyPvjcnkMubabJVUuoEdDx5GoUxAIvVQFToDUj
    hydhgn4PNLW/+qUwVC/afd1D3WhK87qeWEzovCUtVOehKvNi1suamBPdAyom0GqNRoRsFgEzn95l
    w+WdJM+8rqy2dJ5oSF7hQB/4S7XRBygC3I3glmVAKrM4jJVHUvOWxR8I0On45fz+ryUBYPKChHMs
    gAzt+JCiV8XyS3N4FLdlqTT1OuD6tG3H6TbdpBeA2cIeqdOGe9syWZSe4Ipc2Tyo/a/pgffQiNwn
    Zgjf84I5GbFXdRK7fZ7xBDZWfsJ+UjA6CC6+ijLTZsrQ0O7ELh43yg46RdCVoPUQrY/Y0K6395/2
    NlP5zw/yLyHREP6f1h9R+B6O'''
privkey = zlib.decompress(privkey.decode("base-64"))
