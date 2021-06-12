
# Stub unicodedata module. Covers only the Latin-1 range.

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


_latin1_categories={u'\x00': 'Cc', u'\x83': 'Cc', u'\x04': 'Cc', u'\x87': 'Cc', u'\x08':
'Cc', u'\x8b': 'Cc', u'\x0c': 'Cc', u'\x8f': 'Cc', u'\x10': 'Cc',
u'\x93': 'Cc', u'\x14': 'Cc', u'\x97': 'Cc', u'\x18': 'Cc', u'\x9b':
'Cc', u'\x1c': 'Cc', u'\x9f': 'Cc', u' ': 'Zs', u'\xa3': 'Sc', u'$':
'Sc', u'\xa7': 'So', u'(': 'Ps', u'\xab': 'Pi', u',': 'Po', u'\xaf':
'Sk', u'0': 'Nd', u'\xb3': 'No', u'4': 'Nd', u'\xb7': 'Po', u'8':
'Nd', u'\xbb': 'Pf', u'<': 'Sm', u'\xbf': 'Po', u'@': 'Po', u'\xc3':
'Lu', u'D': 'Lu', u'\xc7': 'Lu', u'H': 'Lu', u'\xcb': 'Lu', u'L':
'Lu', u'\xcf': 'Lu', u'P': 'Lu', u'\xd3': 'Lu', u'T': 'Lu', u'\xd7':
'Sm', u'X': 'Lu', u'\xdb': 'Lu', u'\\': 'Po', u'\xdf': 'Ll', u'`':
'Sk', u'\xe3': 'Ll', u'd': 'Ll', u'\xe7': 'Ll', u'h': 'Ll', u'\xeb':
'Ll', u'l': 'Ll', u'\xef': 'Ll', u'p': 'Ll', u'\xf3': 'Ll', u't':
'Ll', u'\xf7': 'Sm', u'x': 'Ll', u'\xfb': 'Ll', u'|': 'Sm', u'\xff':
'Ll', u'\x80': 'Cc', u'\x03': 'Cc', u'\x84': 'Cc', u'\x07': 'Cc',
u'\x88': 'Cc', u'\x0b': 'Cc', u'\x8c': 'Cc', u'\x0f': 'Cc', u'\x90':
'Cc', u'\x13': 'Cc', u'\x94': 'Cc', u'\x17': 'Cc', u'\x98': 'Cc',
u'\x1b': 'Cc', u'\x9c': 'Cc', u'\x1f': 'Cc', u'\xa0': 'Zs', u'#':
'Po', u'\xa4': 'Sc', u"'": 'Po', u'\xa8': 'Sk', u'+': 'Sm', u'\xac':
'Sm', u'/': 'Po', u'\xb0': 'So', u'3': 'Nd', u'\xb4': 'Sk', u'7':
'Nd', u'\xb8': 'Sk', u';': 'Po', u'\xbc': 'No', u'?': 'Po', u'\xc0':
'Lu', u'C': 'Lu', u'\xc4': 'Lu', u'G': 'Lu', u'\xc8': 'Lu', u'K':
'Lu', u'\xcc': 'Lu', u'O': 'Lu', u'\xd0': 'Lu', u'S': 'Lu', u'\xd4':
'Lu', u'W': 'Lu', u'\xd8': 'Lu', u'[': 'Ps', u'\xdc': 'Lu', u'_':
'Pc', u'\xe0': 'Ll', u'c': 'Ll', u'\xe4': 'Ll', u'g': 'Ll', u'\xe8':
'Ll', u'k': 'Ll', u'\xec': 'Ll', u'o': 'Ll', u'\xf0': 'Ll', u's':
'Ll', u'\xf4': 'Ll', u'w': 'Ll', u'\xf8': 'Ll', u'{': 'Ps', u'\xfc':
'Ll', u'\x7f': 'Cc', u'\x81': 'Cc', u'\x02': 'Cc', u'\x85': 'Cc',
u'\x06': 'Cc', u'\x89': 'Cc', u'\n': 'Cc', u'\x8d': 'Cc', u'\x0e':
'Cc', u'\x91': 'Cc', u'\x12': 'Cc', u'\x95': 'Cc', u'\x16': 'Cc',
u'\x99': 'Cc', u'\x1a': 'Cc', u'\x9d': 'Cc', u'\x1e': 'Cc', u'\xa1':
'Po', u'"': 'Po', u'\xa5': 'Sc', u'&': 'Po', u'\xa9': 'So', u'*':
'Po', u'\xad': 'Pd', u'.': 'Po', u'\xb1': 'Sm', u'2': 'Nd', u'\xb5':
'Ll', u'6': 'Nd', u'\xb9': 'No', u':': 'Po', u'\xbd': 'No', u'>':
'Sm', u'\xc1': 'Lu', u'B': 'Lu', u'\xc5': 'Lu', u'F': 'Lu', u'\xc9':
'Lu', u'J': 'Lu', u'\xcd': 'Lu', u'N': 'Lu', u'\xd1': 'Lu', u'R':
'Lu', u'\xd5': 'Lu', u'V': 'Lu', u'\xd9': 'Lu', u'Z': 'Lu', u'\xdd':
'Lu', u'^': 'Sk', u'\xe1': 'Ll', u'b': 'Ll', u'\xe5': 'Ll', u'f':
'Ll', u'\xe9': 'Ll', u'j': 'Ll', u'\xed': 'Ll', u'n': 'Ll', u'\xf1':
'Ll', u'r': 'Ll', u'\xf5': 'Ll', u'v': 'Ll', u'\xf9': 'Ll', u'z':
'Ll', u'\xfd': 'Ll', u'~': 'Sm', u'\x01': 'Cc', u'\x82': 'Cc',
u'\x05': 'Cc', u'\x86': 'Cc', u'\t': 'Cc', u'\x8a': 'Cc', u'\r': 'Cc',
u'\x8e': 'Cc', u'\x11': 'Cc', u'\x92': 'Cc', u'\x15': 'Cc', u'\x96':
'Cc', u'\x19': 'Cc', u'\x9a': 'Cc', u'\x1d': 'Cc', u'\x9e': 'Cc',
u'!': 'Po', u'\xa2': 'Sc', u'%': 'Po', u'\xa6': 'So', u')': 'Pe',
u'\xaa': 'Ll', u'-': 'Pd', u'\xae': 'So', u'1': 'Nd', u'\xb2': 'No',
u'5': 'Nd', u'\xb6': 'So', u'9': 'Nd', u'\xba': 'Ll', u'=': 'Sm',
u'\xbe': 'No', u'A': 'Lu', u'\xc2': 'Lu', u'E': 'Lu', u'\xc6': 'Lu',
u'I': 'Lu', u'\xca': 'Lu', u'M': 'Lu', u'\xce': 'Lu', u'Q': 'Lu',
u'\xd2': 'Lu', u'U': 'Lu', u'\xd6': 'Lu', u'Y': 'Lu', u'\xda': 'Lu',
u']': 'Pe', u'\xde': 'Lu', u'a': 'Ll', u'\xe2': 'Ll', u'e': 'Ll',
u'\xe6': 'Ll', u'i': 'Ll', u'\xea': 'Ll', u'm': 'Ll', u'\xee': 'Ll',
u'q': 'Ll', u'\xf2': 'Ll', u'u': 'Ll', u'\xf6': 'Ll', u'y': 'Ll',
u'\xfa': 'Ll', u'}': 'Pe', u'\xfe': 'Ll'}

def category(c):
    return _latin1_categories.get(c)
