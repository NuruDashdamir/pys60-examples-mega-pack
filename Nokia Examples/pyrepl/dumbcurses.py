#
# Curses stub to provide minimal functions required by SocketConsole.
#
# Copyright (c) 2005 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Grabbed from vt100. The original codes had delay expressions ($<xx>)
# in them, which have been removed.
_capabilities={ 
    'bel': '\x07',
    'civis': None,
    'clear': '\x1b[H\x1b[J',
    'cnorm': None,
    'cub': '\x1b[%dD',
    'cub1': '\x08',
    'cud': '\x1b[%dB',
    'cud1': '\n',
    'cuf': '\x1b[%dC',
    'cuf1': '\x1b[C',
    'cup': '\x1b[%d;%dH',
    'cuu': '\x1b[%dA',
    'cuu1': '\x1b[A',
    'dch': None,
    'dch1': None,
    'el': '\x1b[K',
    'hpa': None,
    'ich': None,
    'ich1': None,
    'ind': '\n',
    'pad': None,
    'kcuu1': '\x1b[A',
    'kcud1': '\x1b[B',
    'kcuf1': '\x1b[C',
    'kcub1': '\x1b[D',
    'kdch1': '\x1b[3~',
    'knp': '\x1b[6~',
    'kpp': '\x1b[5~',
    'ri': '\x1bM',
    'rmkx': '\x1b[?1l\x1b>',
    'smkx': '\x1b[?1h\x1b='}

def tigetstr(cap):
    '''Return terminal capability string for given capability'''
    if _capabilities.has_key(cap):
        return _capabilities[cap]
    else:
        return None

def tparm(str,*args):
    return str%(args)

