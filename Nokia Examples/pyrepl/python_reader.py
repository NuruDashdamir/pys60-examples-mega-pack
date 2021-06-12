#   Copyright 2000-2004 Michael Hudson mwh@python.net
#
#                        All Rights Reserved
#
# Portions Copyright (c) 2005 Nokia Corporation 
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

# one impressive collections of imports:
from pyrepl.completing_reader import CompletingReader
from pyrepl.historical_reader import HistoricalReader
from pyrepl import completing_reader, reader
from pyrepl import commands, completer
from pyrepl import module_lister
import sys, os, re, code, atexit
import warnings

HISTORYFILE=u"c:\\pythonhistory.txt"

try:
    import cPickle as pickle
except ImportError:
    try:
        import pickle
    except ImportError:
        try:
            import dumbpickle as pickle
        except ImportError:
            print "No pickle module -> command history will not be saved."
            pickle=None

CommandCompiler = code.CommandCompiler

def eat_it(*args):
    """this function eats warnings, if you were wondering"""
    pass

class maybe_accept(commands.Command):
    def do(self):
        r = self.reader
        text = r.get_unicode()
        try:
            # ooh, look at the hack:
            code = r.compiler("#coding:utf-8\n"+text.encode('utf-8'))
        except (OverflowError, SyntaxError, ValueError):
            self.finish = 1
        else:
            if code is None:
                r.insert("\n")
            else:
                self.finish = 1

from_line_prog = re.compile(
    "^from\s+(?P<mod>[A-Za-z_.0-9]*)\s+import\s+(?P<name>[A-Za-z_.0-9]*)")
import_line_prog = re.compile(
    "^(?:import|from)\s+(?P<mod>[A-Za-z_.0-9]*)\s*$")

def mk_saver(reader):
    def saver(reader=reader):
        try:
            file = open(HISTORYFILE, "w")
        except IOError:
            pass
        else:
            pickle.dump(reader.history, file)
            file.close()
    return saver

def prhelp():
    print '''
This is pyrepl, a simple multiline editor with command history, tab
completion and emacs-like key bindings.

Most useful commands:
(C-x means Control-x, M-x means Alt-x or Esc x)

    C-p, C-n     previous/next history item
    C-o          accept line and take next line from history
                 (handy for repeating sequences of commands)
    M-r          restore line to what it was when retrieved
                 from history
    C-r, C-s     incremental search back/forward
    C-a, C-e     beginning/end of line
    M-f, M-b     next/previous word
    C-k          cut to end of line
    C-w, M-d     cut word to left/right of cursor
    C-y          paste
    M-y          paste older (use after C-y)
    M-return     insert literal Return
    C-d          delete character/quit interpreter
    C-xC-s       save history to file (also saved on graceful exit)
    tab          complete item (attribute, method, variable...)
'''

class PythonicReader(CompletingReader, HistoricalReader):
    def collect_keymap(self):
        return super(PythonicReader, self).collect_keymap() + (
            (r'\r', 'maybe-accept'),
            (r'\M-\r', 'insert-nl'),
            (r'\n', 'maybe-accept'),
            (r'\M-\n', 'insert-nl'))
    
    def __init__(self, console, locals,
                 compiler=None):
        super(PythonicReader, self).__init__(console)
        self.completer = completer.Completer(locals)
        st = self.syntax_table
        for c in "._0123456789":
            st[c] = reader.SYNTAX_WORD
        self.locals = locals
        self.locals['prhelp']=prhelp
        if compiler is None:
            self.compiler = CommandCompiler()
        else:
            self.compiler = compiler
        try:
            file = open(HISTORYFILE)
        except IOError:
            pass
        else:
            try:
                self.history = pickle.load(file)
            except:
                self.history = []
            self.historyi = len(self.history)
            file.close()
        self.save_history=mk_saver(self)
        atexit.register(self.save_history)
        for c in [maybe_accept]:
            self.commands[c.__name__] = c
            self.commands[c.__name__.replace('_', '-')] = c        
    
    def get_completions(self, stem):
        b = self.get_unicode()
        m = import_line_prog.match(b)
        if m:
            mod = m.group("mod")
            try:
                return module_lister.find_modules(mod)
            except ImportError:
                pass
        m = from_line_prog.match(b)
        if m:
            mod, name = m.group("mod", "name")
            try:
                l = module_lister._packages[mod]
            except KeyError:
                try:
                    mod = __import__(mod, self.locals, self.locals, [''])
                    return [x for x in dir(mod) if x.startswith(name)]
                except ImportError:
                    pass
            else:
                return [x[len(mod) + 1:]
                        for x in l if x.startswith(mod + '.' + name)]
        try:
            l = completing_reader.uniqify(self.completer.complete(stem))
            return l
        except (NameError, AttributeError):
            return []

class ReaderConsole(code.InteractiveInterpreter):
    II_init = code.InteractiveInterpreter.__init__
    def __init__(self, console, locals=None):
        self.II_init(locals)
        self.compiler = CommandCompiler()
        self.compile = self.compiler.compiler
        self.reader = PythonicReader(console, locals, self.compiler)
        self.locals['Reader'] = self.reader

    def run_user_init_file(self):
        for key in "PYREPLSTARTUP", "PYTHONSTARTUP":
            initfile = os.environ.get(key)
            if initfile is not None and os.path.exists(initfile):
                break
        else:
            return
        try:
            execfile(initfile, self.locals, self.locals)
        except:
            etype, value, tb = sys.exc_info()
            import traceback
            traceback.print_exception(etype, value, tb.tb_next)

    def execute(self, text):
        try:
            # ooh, look at the hack:            
            code = self.compile("# coding:utf8\n"+text.encode('utf-8'),
                                '<input>', 'single')
        except (OverflowError, SyntaxError, ValueError):
            self.showsyntaxerror("<input>")
        else:
            self.runcode(code)
            sys.stdout.flush()

    def interact(self):
        while 1:
            try:
                try: # catches EOFError's and KeyboardInterrupts during execution
                    try: # catches KeyboardInterrupts during editing
                        try: # warning saver
                            # can't have warnings spewed onto terminal
                            sv = warnings.showwarning
                            warnings.showwarning = eat_it
                            l = unicode(self.reader.readline(), 'utf-8')
                        finally:
                            warnings.showwarning = sv
                    except KeyboardInterrupt:
                        print "KeyboardInterrupt"
                    else:
                        if l:
                            self.execute(l)
                except EOFError:
                    break
                except KeyboardInterrupt:
                    continue
            finally:
                self.reader.save_history()

    def prepare(self):
        self.sv_sw = warnings.showwarning
        warnings.showwarning = eat_it
        self.reader.prepare()
        self.reader.refresh() # we want :after methods...

    def restore(self):
        self.reader.restore()
        warnings.showwarning = self.sv_sw

    def handle1(self, block=1):
        try:
            r = 1
            r = self.reader.handle1(block)
        except KeyboardInterrupt:
            self.restore()
            print "KeyboardInterrupt"
            self.prepare()
        else:
            if self.reader.finished:
                text = self.reader.get_unicode()
                self.restore()
                if text:
                    self.execute(text)
                self.prepare()
        return r


