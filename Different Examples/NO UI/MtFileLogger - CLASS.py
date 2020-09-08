#
# MtFileLogger.py
# 
# Copyright 2004 Helsinki Institute for Information Technology (HIIT)
# and the authors.  All rights reserved.
# 
# Authors: Tero Hasu <tero.hasu@hut.fi>
#
# A logger module that supports multiple threads, and is efficient
# in the sense that it keeps the log files open between writes.
#

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import thread
import time


class FloggerSubst:
    """
    Implements the Symbian-specific ``aosocketnativenew.AoFlogger``
    class in purer Python.
    """
    def __init__(self):
        self.file = None
    
    def connect(self):
        pass

    def close(self):
        if self.file:
            self.file.close()
            self.file = None
            
    def create_log(self, dirname, filename):
        pathname = "c:\\logs\\" + dirname + "\\" + filename
        try:
            self.file = open(pathname, "w")
        except IOError:
            self.file = None

    def write(self, text):
        """
        Unlike with ``Flogger``, this version of ``write`` does
        not truncate lines, which is useful at least when inspecting
        stack traces.
        """
        if self.file:
            # using CRLF for Notepad support
            self.file.write(time.asctime() + ": " + text + "\r\n")
            self.file.flush()


class MtFileLogger:
    """
    Logging to one file per thread.

    This class keeps each log file open between writes, which
    makes this implementation more efficient than if one was
    using closing the file after every write, and then reopening
    and seeking before the next write. However, when using
    this one has to be very careful to close the log file
    for *every* thread that has done any logging.

    This class internally creates one Flogger object per thread.
    Could use just one if ``RFileLogger`` were to support that
    sort of thing, but we know not whether it does.
    """

    def __init__(self, dirname, basename):
        self.dirname = dirname
        self.basename = basename + "-" + time.strftime("%H%M%S")
        self.mutex = thread.allocate_lock()
        self.map = {}
        self.count = 0

    def write(self, text):
        tid = thread.get_ident()

        self.mutex.acquire()
        try:
            if self.map.has_key(tid):
                logger = self.map[tid]
            else:
                flogger = FloggerSubst()
                flogger.connect()
                flogger.create_log(self.dirname,
                                   self.basename + "-%d.txt" % tid)
                logger = self.map[tid] = flogger
            count = self.count
            self.count += 1
        finally:
            self.mutex.release()
        
        if logger:
            logger.write("(%04d) %s" % (count, text))

    def close(self):
        """
        This method does nothing but complains if logging has
        not already been closed separately for each thread.
        """
        self.mutex.acquire()
        try:
            for v in self.map.itervalues():
                if v != None:
                    print str(self.map)
                    assert False
        finally:
            self.mutex.release()

    def close_for_thread(self):
        """
        This method _only_ closes the logger for the current
        thread, if there is one. This is because it may not be safe
        to mess with other threads' file handles, and because
        it might not be a good idea for one thread to prematurely
        cause the other threads to stop logging.
        """
        tid = thread.get_ident()
        self.mutex.acquire()
        try:
            self.__close_for_thread(tid)
        finally:
            self.mutex.release()

    def __close_for_thread(self, tid):
        """
        Must hold mutex.
        """
        if self.map.has_key(tid):
            # ``None`` indicates that the logger has been closed,
            # and that a new logger should not be created upon
            # calling ``write``.
            if self.map[tid]:
                self.map[tid].close()
                self.map[tid] = None
        
