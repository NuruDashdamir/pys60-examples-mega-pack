#
# This is a simple console class, which tries to handle a VT100-workalike
# terminal at the other end of a given socket connection.
#
# Limitations:
#  - currently the remote screen size is assumed to be 80x25
#  - sockets are assumed to be blocking (since the platform in mind didn't
#    have nonblocking sockets)
#
# Portions Copyright (c) 2005 Nokia Corporation 
#
# The code is derived from unix_console.py, which contained the
# following copyright notice:
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

import sys
from pyrepl.console import Console, Event
from pyrepl import unix_eventqueue
import dumbcurses as curses
import socket

def _my_getstr(cap, optional=0):
    r = curses.tigetstr(cap)
    if not optional and r is None:
        raise RuntimeError, \
              "terminal doesn't have the required '%s' capability"%cap
    return r

class SocketConsole(Console):
    MAX_READ=16
    def __init__(self, socket, encoding=None):
#        if encoding is None:
#            encoding = sys.getdefaultencoding()
            
#        self.encoding = encoding
        #print >>sys.stderr,"Encoding "+encoding
        self.encoding='latin-1'

        self._socket=socket

        self.__buffer = []
        
        self._bel   = _my_getstr("bel")
        self._civis = _my_getstr("civis", optional=1)
        self._clear = _my_getstr("clear")
        self._cnorm = _my_getstr("cnorm", optional=1)
        self._cub   = _my_getstr("cub",   optional=1)
        self._cub1  = _my_getstr("cub1",  1)
        self._cud   = _my_getstr("cud",   1)
        self._cud1  = _my_getstr("cud1",  1)
        self._cuf   = _my_getstr("cuf",   1)
        self._cuf1  = _my_getstr("cuf1",  1)
        self._cup   = _my_getstr("cup")
        self._cuu   = _my_getstr("cuu",   1)
        self._cuu1  = _my_getstr("cuu1",  1)
        self._dch1  = _my_getstr("dch1",  1)
        self._dch   = _my_getstr("dch",   1)
        self._el    = _my_getstr("el")
        self._hpa   = _my_getstr("hpa",   1)
        self._ich   = _my_getstr("ich",   1)
        self._ich1  = _my_getstr("ich1",  1)
        self._ind   = _my_getstr("ind",   1)
        self._pad   = _my_getstr("pad",   1)
        self._ri    = _my_getstr("ri",    1)
        self._rmkx  = _my_getstr("rmkx",  1)
        self._smkx  = _my_getstr("smkx",  1)
        
        ## work out how we're going to sling the cursor around
        if 0 and self._hpa: # hpa don't work in windows telnet :-(
            self.__move_x = self.__move_x_hpa
        elif self._cub and self._cuf:
            self.__move_x = self.__move_x_cub_cuf
        elif self._cub1 and self._cuf1:
            self.__move_x = self.__move_x_cub1_cuf1
        else:
            raise RuntimeError, "insufficient terminal (horizontal)"

        if self._cuu and self._cud:
            self.__move_y = self.__move_y_cuu_cud
        elif self._cuu1 and self._cud1:
            self.__move_y = self.__move_y_cuu1_cud1
        else:
            raise RuntimeError, "insufficient terminal (vertical)"

        if self._dch1:
            self.dch1 = self._dch1
        elif self._dch:
            self.dch1 = curses.tparm(self._dch, 1)
        else:
            self.dch1 = None

        if self._ich1:
            self.ich1 = self._ich1
        elif self._ich:
            self.ich1 = curses.tparm(self._ich, 1)
        else:
            self.ich1 = None

        self.__move = self.__move_short

        self.event_queue = unix_eventqueue.EventQueue()
        self.busy=False

    def _oswrite(self,str):
        try:
            self._socket.send(str)
        except socket.error:
            raise IOError("Socket error: %s %s"%(sys.exc_info()[0:2]))

    def _osread(self,n=1):
        try:
            out=self._socket.recv(n)
        except socket.error:
            raise EOFError("Socket error: %s %s"%(sys.exc_info()[0:2]))
        return out

    def write(self,str):
        self._oswrite(str.replace('\n','\n\r'))

    def flush(self):
        self.flushoutput()
        
    def read(self,n=1):        
        return self._osread(n)

    def readline(self,n=None):
        line=[]
        while 1:
            ch=self.read(1)
            line.append(ch)
            self.write(ch)
            if ch == '\n':
                break
            if n and len(line)>=n:
                break
        return ''.join(line)

    # No readlines() because reading until EOF doesn't make sense
    # for the console.
    
    def isatty(self):
        return True

    def writelines(self,seq):
        for k in seq:
            self.write(k)

    def change_encoding(self, encoding):
        self.encoding = encoding
    
    def refresh(self, screen, (cx, cy)):
        # this function is still too long (over 90 lines)
        self.__maybe_write_code(self._civis)

        if not self.__gone_tall:
            while len(self.screen) < min(len(screen), self.height):
                self.__move(0, len(self.screen) - 1)
                self.__write("\n")
                self.__posxy = 0, len(self.screen)
                self.screen.append("")
        else:
            while len(self.screen) < len(screen):
                self.screen.append("")            

        if len(screen) > self.height:
            self.__gone_tall = 1
            self.__move = self.__move_tall

        px, py = self.__posxy
        old_offset = offset = self.__offset
        height = self.height

        # we make sure the cursor is on the screen, and that we're
        # using all of the screen if we can
        if cy < offset:
            offset = cy
        elif cy >= offset + height:
            offset = cy - height + 1
        elif offset > 0 and len(screen) < offset + height:
            offset = max(len(screen) - height, 0)
            screen.append([])

        oldscr = self.screen[old_offset:old_offset + height]
        newscr = screen[offset:offset + height]

        # use hardware scrolling if we have it.
        if old_offset > offset and self._ri:
            self.__write_code(self._cup, 0, 0)
            self.__posxy = 0, old_offset
            for i in range(old_offset - offset):
                self.__write_code(self._ri)
                oldscr.pop(-1)
                oldscr.insert(0, "")
        elif old_offset < offset and self._ind:
            self.__write_code(self._cup, self.height - 1, 0)
            self.__posxy = 0, old_offset + self.height - 1
            for i in range(offset - old_offset):
                self.__write_code(self._ind)
                oldscr.pop(0)
                oldscr.append("")

        self.__offset = offset

        for y, oldline, newline, in zip(range(offset, offset + height),
                                        oldscr,
                                        newscr):
            if oldline != newline:
                self.write_changed_line(y, oldline, newline, px)
                
        y = len(newscr)
        while y < len(oldscr):
            self.__move(0, y)
            self.__posxy = 0, y
            self.__write_code(self._el)
            y += 1

        self.__maybe_write_code(self._cnorm)
        
        #self.flushoutput()
        self.screen = screen
        self.move_cursor(cx, cy) # this does self.flushoutput()

    def write_changed_line(self, y, oldline, newline, px):
        # this is frustrating; there's no reason to test (say)
        # self.dch1 inside the loop -- but alternative ways of
        # structuring this function are equally painful (I'm trying to
        # avoid writing code generators these days...)
        x = 0
        minlen = min(len(oldline), len(newline))
        while x < minlen and oldline[x] == newline[x]:
            x += 1
        if oldline[x:] == newline[x+1:] and self.ich1:
            if ( y == self.__posxy[1] and x > self.__posxy[0]
                 and oldline[px:x] == newline[px+1:x+1] ):
                x = px
            self.__move(x, y)
            self.__write_code(self.ich1)
            self.__write(newline[x])
            self.__posxy = x + 1, y
        elif x < minlen and oldline[x + 1:] == newline[x + 1:]:
            self.__move(x, y)
            self.__write(newline[x])
            self.__posxy = x + 1, y
        elif (self.dch1 and self.ich1 and len(newline) == self.width
              and x < len(newline) - 2
              and newline[x+1:-1] == oldline[x:-2]):
            self.__move(self.width - 2, y)
            self.__posxy = self.width - 2, y
            self.__write_code(self.dch1)
            self.__move(x, y)
            self.__write_code(self.ich1)
            self.__write(newline[x])
            self.__posxy = x + 1, y
        else:
            self.__move(x, y)
            if len(oldline) > len(newline):
                self.__write_code(self._el)
            self.__write(newline[x:])
            self.__posxy = len(newline), y
        #self.flushoutput() # removed for efficiency

    def __write(self, text):
        self.__buffer.append((text, 0))

    def __write_code(self, fmt, *args):
        self.__buffer.append((curses.tparm(fmt, *args), 1))

    def __maybe_write_code(self, fmt, *args):
        if fmt:
            self.__write_code(fmt, *args)

    def __move_y_cuu1_cud1(self, y):
        dy = y - self.__posxy[1]
        if dy > 0:
            self.__write_code(dy*self._cud1)
        elif dy < 0:
            self.__write_code((-dy)*self._cuu1)

    def __move_y_cuu_cud(self, y):
        dy = y - self.__posxy[1]
        if dy > 0:
            self.__write_code(self._cud, dy)
        elif dy < 0:
            self.__write_code(self._cuu, -dy)

    def __move_x_hpa(self, x):
        if x != self.__posxy[0]:
            self.__write_code(self._hpa, x)

    def __move_x_cub1_cuf1(self, x):
        dx = x - self.__posxy[0]
        if dx > 0:
            self.__write_code(self._cuf1*dx)
        elif dx < 0:
            self.__write_code(self._cub1*(-dx))

    def __move_x_cub_cuf(self, x):
        dx = x - self.__posxy[0]
        if dx > 0:
            self.__write_code(self._cuf, dx)
        elif dx < 0:
            self.__write_code(self._cub, -dx)

    def __move_short(self, x, y):
        self.__move_x(x)
        self.__move_y(y)

    def __move_tall(self, x, y):
        assert 0 <= y - self.__offset < self.height, y - self.__offset
        self.__write_code(self._cup, y - self.__offset, x)

    def move_cursor(self, x, y):
        if y < self.__offset or y >= self.__offset + self.height:
            self.event_queue.insert(Event('scroll', None))
        else:
            self.__move(x, y)
            self.__posxy = x, y
            if not self.isbusy():
                self.flushoutput()

    def prepare(self):
        self.screen = []
        self.height, self.width = self.getheightwidth()

        self.__buffer = []
        
        self.__posxy = 0, 0
        self.__gone_tall = 0
        self.__move = self.__move_short
        self.__offset = 0

        self.__maybe_write_code(self._rmkx) # Turn off application cursor mode.

    def restore(self):
        # We never put the cursor keys in application mode, so this
        # is redundant now:
        #self.__maybe_write_code(self._rmkx) 
        self.flushoutput()

    def __sigwinch(self, signum, frame):
        self.height, self.width = self.getheightwidth()
        self.event_queue.insert(Event('resize', None))

    def isbusy(self):
        return self.busy

    def get_event(self, block=1):        
        while self.event_queue.empty():
            chars = self._osread(self.MAX_READ)
#            try:
#            except EOFError:
#                raise
#            except:
#                print >>sys.stderr,"Exception!"
#                import traceback
#                traceback.print_exc()
#                raise
            for c in chars:
                self.event_queue.push(c)
            if not block:
                break
        self.busy=len(self.event_queue.events)>1
        return self.event_queue.get()

    def wait(self):
        pass 
    #self.pollob.poll()

    def set_cursor_vis(self, vis):
        if vis:
            self.__maybe_write_code(self._cnorm)
        else:
            self.__maybe_write_code(self._civis)

    def repaint_prep(self):
        if not self.__gone_tall:
            self.__posxy = 0, self.__posxy[1]
            self.__write("\r")
            ns = len(self.screen)*['\000'*self.width]
            self.screen = ns
        else:
            self.__posxy = 0, self.__offset
            self.__move(0, self.__offset)
            ns = self.height*['\000'*self.width]
            self.screen = ns

    def getheightwidth(self):
        return 25, 80

    def forgetinput(self):
        pass

    def flushoutput(self):
        if not self.event_queue.empty():
            return
        if len(self.__buffer)==0:
            return 
        outbuf=[]
        for text, iscode in self.__buffer:
            if iscode:
                outbuf.append(text)
                # we don't use delays here, so we don't need tputs
                # processing.                
                # outbuf.append(self.__tputs(text))
            else:
                outbuf.append(text.encode(self.encoding))
 
        self._oswrite(''.join(outbuf))
        del self.__buffer[:]

    def finish(self):
        y = len(self.screen) - 1
        while y >= 0 and not self.screen[y]:
            y -= 1
        self.__move(0, min(y, self.height + self.__offset - 1))
        self.__write("\n\r")
        self.flushoutput()

    def beep(self):
        self.__maybe_write_code(self._bel)
        self.flushoutput()

    def getpending(self):
        e = Event('key', '', '')
        
        while not self.event_queue.empty():
            e2 = self.event_queue.get()
            e.data += e2.data
            e.raw += e2.raw

        amount = 1000
        raw = unicode(self._osread(amount), self.encoding, 'replace')
        e.data += raw
        e.raw += raw
        return e

    def clear(self):
        self.__write_code(self._clear)
        self.__gone_tall = 1
        self.__move = self.__move_tall
        self.__posxy = 0, 0
        self.screen = []

