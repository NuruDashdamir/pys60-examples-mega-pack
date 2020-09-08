import os
import e32
import appuifw
aa = appuifw.app

def ru(t):
    return t.decode('utf-8')



def ur(t):
    return t.encode('utf-8')


appuifw.app.screen = 'normal'
class FileMan:
    __module__ = __name__
    __module__ = __name__
    __module__ = __name__
    __module__ = __name__

    def __init__(s, ext = ''):
        (s.PATHHISTORY, s.PATHACTIVE, s.ALLFILES, s.SELECTFILES, s.LISTBOX,) = ([['',
           0]],
         '',
         [],
         [],
         [u''])
        if (len(ext) != 0):
            s.MASK = ext
            s.list_dir = s.listdir
        else:
            s.list_dir = os.listdir



    def run(s):
        s.OLDSTATE = [aa.screen,
         aa.menu,
         aa.body,
         aa.exit_key_handler]
        (aa.screen, aa.exit_key_handler,) = ('normal',
         s.exit)
        s.BODY = aa.body = appuifw.Listbox(s.LISTBOX, s.exchange)
        aa.menu = [(ru('Select Drive'),
          s.reset),
         (ru('Mark'),
          ((ru('Mark all'),
            lambda :s.exchange(1)
),
           (ru('Unmark all'),
            lambda :s.exchange(2)
),
           (ru('Invert selected'),
            lambda :s.exchange(3)
))),
         (ru('Done'),
          s.exit)]
        s.BODY.bind(63495, s.back)
        s.BODY.bind(63496, s.forward)
        s.BODY.bind(63499, s.exchange)
        s.BODY.bind(49, lambda :s.exchange(1)
)
        s.BODY.bind(50, lambda :s.exchange(2)
)
        s.BODY.bind(51, lambda :s.exchange(3)
)
        s.back()



    def reset(s):
        s.__init__()
        s.back()



    def exit(s):
        s.PATHHISTORY.append([s.PATHACTIVE,
         s.BODY.current()])
        (aa.screen, aa.menu, aa.body, aa.exit_key_handler,) = s.OLDSTATE
        app.text(ru(('->File to compile: ' + str(len(s.SELECTFILES)))))



    def forward(s):
        pa = ((s.PATHACTIVE + s.ALLFILES[s.BODY.current()]) + '/')
        if (not os.path.isdir(pa)):
            return 
        af = s.list_dir(pa)
        if (len(af) == 0):
            return 
        s.PATHHISTORY.append([s.PATHACTIVE,
         s.BODY.current()])
        (s.PATHACTIVE, s.ALLFILES,) = (pa,
         af)
        s.set_list()



    def back(s):
        if (len(s.PATHHISTORY) == 0):
            return 
        ph = s.PATHHISTORY.pop()
        s.PATHACTIVE = ph[0]
        if (s.PATHACTIVE == ''):
            s.ALLFILES = ['c:',
             'e:']
        else:
            s.ALLFILES = s.list_dir(s.PATHACTIVE)
        s.set_list(ph[1])



    def set_list(s, c = 0):
        s.LISTBOX = []
        for i in s.ALLFILES:
            if ((s.PATHACTIVE + i) in s.SELECTFILES):
                s.LISTBOX.append((u'+' + ru(i)))
            else:
                s.LISTBOX.append((u' ' + ru(i)))

        s.BODY.set_list(s.LISTBOX, c)



    def listdir(s, DIR):
        LIST = []
        for i in os.listdir(DIR):
            if (os.path.isdir(((DIR + '/') + i)) | i.endswith(s.MASK)):
                LIST.append(i)

        return LIST



    def exchange(s, n = 0):
        if (n == 0):
            f = (s.PATHACTIVE + s.ALLFILES[s.BODY.current()])
            if os.path.isfile(f):
                if (f in s.SELECTFILES):
                    del s.SELECTFILES[s.SELECTFILES.index(f)]
                else:
                    s.SELECTFILES.append(f)
        else:
            for i in s.ALLFILES:
                f = (s.PATHACTIVE + i)
                if os.path.isfile(f):
                    if (n == 1):
                        if (f not in s.SELECTFILES):
                            s.SELECTFILES.append(f)
                    if (n == 2):
                        if (f in s.SELECTFILES):
                            del s.SELECTFILES[s.SELECTFILES.index(f)]
                    if (n == 3):
                        if (f in s.SELECTFILES):
                            del s.SELECTFILES[s.SELECTFILES.index(f)]
                        else:
                            s.SELECTFILES.append(f)

        s.set_list(s.BODY.current())



fileman = FileMan('.py')
class Compile:
    __module__ = __name__
    __module__ = __name__
    __module__ = __name__
    __module__ = __name__

    def start(s):
        app.text(ru('Processing...'))
        I = 0
        for i in fileman.SELECTFILES[:]:
            try:
                s.com(i)
                del fileman.SELECTFILES[fileman.SELECTFILES.index(i)]
                I += 1
                app.text(ru(('Processed: ' + str(I))))
            except:
                pass

        app.text(ru((((('>Successfully compiled: ' + str(I)) + '.\n>Unable to compiled: ') + str(len(fileman.SELECTFILES))) + '.')))



    def com(s, file, cfile = None, dfile = None):
        import os
        import imp
        import marshal
        import __builtin__
        f = open(file)
        try:
            timestamp = long(os.fstat(f.fileno())[8])
        except AttributeError:
            timestamp = long(os.stat(file)[8])
        codestring = f.read()
        codestring = codestring.replace('\r\n', '\n')
        codestring = codestring.replace('\r', '\n')
        f.close()
        if (codestring and (codestring[-1] != '\n')):
            codestring = (codestring + '\n')
        try:
            codeobject = __builtin__.compile(codestring, (dfile or file), 'exec')
        except SyntaxError, detail:
            import traceback
            import sys
            lines = traceback.format_exception_only(SyntaxError, detail)
            for line in lines:
                sys.stderr.write(line.replace('File "<string>"', ('File "%s"' % (dfile or file))))

            return 
        if (not cfile):
            cfile = (file + ((__debug__ and 'c') or 'o'))
        fc = open(cfile, 'wb')
        fc.write('\x00\x00\x00\x00')
        fc.write(chr((timestamp & 255)))
        fc.write(chr(((timestamp >> 8) & 255)))
        fc.write(chr(((timestamp >> 16) & 255)))
        fc.write(chr(((timestamp >> 24) & 255)))
        marshal.dump(codeobject, fc)
        fc.flush()
        fc.seek(0, 0)
        fc.write(imp.get_magic())
        fc.close()
        if (os.name == 'mac'):
            import macfs
            macfs.FSSpec(cfile).SetCreatorType('Pyth', 'PYC ')



compile = Compile()
class Exit:
    __module__ = __name__
    __module__ = __name__
    __module__ = __name__
    __module__ = __name__

    def __init__(s):
        s.AOLOCK = e32.Ao_lock()



    def wait(s):
        s.AOLOCK.wait()



    def call(s):
        s.AOLOCK.signal()
        aa.set_exit()



exit = Exit()
class App:
    __module__ = __name__
    __module__ = __name__
    __module__ = __name__
    __module__ = __name__

    def __init__(s):
        (aa.screen, aa.exit_key_handler,) = ('normal',
         exit.call)
        aa.menu = [(ru('Select file'),
          fileman.run),
         (ru('Compile'),
          compile.start)]
        aa.body = appuifw.Text()
        aa.body.color = (0,
         0,
         0)
        s.text(ru('by -=[n0f3a6]=-\n\n@\n\nwww.ipmart-forum.com\n\n\n\n\n\nthnx to maNseries'))



    def text(s, t):
        aa.body.set(t)
        aa.body.set_pos(0)
        aa.body.focus = False
        e32.ao_sleep(0.001)



app = App()
exit.wait()

def aExit():
    x = appuifw.query(ru('Are you sure?'), 'query')
    if (x == 1):
        os.abort()



