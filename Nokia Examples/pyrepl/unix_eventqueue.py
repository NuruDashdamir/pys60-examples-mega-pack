#
# Slightly modified unix_eventqueue.py.
#
# Portions Copyright (c) 2005 Nokia Corporation 
#
#   Copyright 2000-2004 Michael Hudson mwh@python.net
#
#                        All Rights Reserved
#
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose is hereby granted without fee,
# provided that the above copyright notice appear in all copies and
# that both that copyright notice and this permission notice appear in
# supporting documentation.
#
# THE AUTHOR MICHAEL HUDSON DISCLAIMS ALL WARRANTIES WITH REGARD TO
# THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
# RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
# CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Bah, this would be easier to test if curses/terminfo didn't have so
# much non-introspectable global state.

from pyrepl import keymap
from pyrepl.console import Event
import dumbcurses as curses
import sys

_keynames = {
    "delete" : "kdch1",
    "down" : "kcud1",
    "end" : "kend",
    "enter" : "kent",
    "f1"  : "kf1",    "f2"  : "kf2",    "f3"  : "kf3",    "f4"  : "kf4",
    "f5"  : "kf5",    "f6"  : "kf6",    "f7"  : "kf7",    "f8"  : "kf8",
    "f9"  : "kf9",    "f10" : "kf10",   "f11" : "kf11",   "f12" : "kf12",
    "f13" : "kf13",   "f14" : "kf14",   "f15" : "kf15",   "f16" : "kf16",
    "f17" : "kf17",   "f18" : "kf18",   "f19" : "kf19",   "f20" : "kf20",
    "home" : "khome",
    "insert" : "kich1",
    "left" : "kcub1",
    "page down" : "knp",
    "page up"   : "kpp",
    "right" : "kcuf1",
    "up" : "kcuu1",
    }

class EventQueue(object):
    def __init__(self):
        our_keycodes = {}
        for key, tiname in _keynames.items():
            keycode = curses.tigetstr(tiname)
            if keycode:
                our_keycodes[keycode] = unicode(key)
        our_keycodes['\177'] = u'backspace'
#        our_keycodes[tcgetattr(fd)[6][VERASE]] = u'backspace'
        self.k = self.ck = keymap.compile_keymap(our_keycodes)
        self.events = []
        self.buf = []
    def get(self):
        if self.events:
            return self.events.pop(0)
        else:
            return None
    def empty(self):
        return not self.events
    def insert(self, event):
        self.events.append(event)
    def push(self, char):
#        print "Handling char %r"%char
#        print >>sys.stderr,"Handling char %r"%char
        if char in self.k:
            k = self.k[char]
            if isinstance(k, dict):
#                print >>sys.stderr,"In multi-key sequence chr "+char+" dict "+str(k)
                self.buf.append(char)
                self.k = k
            else:
#                print >>sys.stderr,"Finished multi-key sequence:"+str(self.buf)
                self.events.append(Event('key', k, ''.join(self.buf) + char))
                self.buf = []
                self.k = self.ck
        elif self.buf:
#            print >>sys.stderr,"Aborted multi-key sequence %r chr %r dict %r"%(self.buf,char,self.k)
#            print >>sys.stderr,"%r %r %r %r %r %r %r %r %r"%(char,'0',char=='0',self.k.has_key('0'),self.k.has_key(char),len(char),char[0],ord(char),ord('0'))
        
            self.events.extend([Event('key', c, c) for c in self.buf])
            self.buf = []
            self.k = self.ck
            self.push(char)
        else:
            self.events.append(Event('key', char, char))
