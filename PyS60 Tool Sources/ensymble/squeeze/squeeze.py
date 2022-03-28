#!/usr/bin/env python
#
# SQUEEZE
# $Id$
#
# squeeze a python program
#
# installation:
# - use this script as is, or squeeze it using the following command:
#
# python squeezeTool.py -1su -o squeeze -b squeezeTool squeezeTool.py
#
# notes:
# - this is pretty messy.  make sure to test everything carefully
#   if you change anything
#
# - the name "squeeze" is taken from an ABC800 utility which did
#   about the same thing with Basic II bytecodes.
#
# history:
# 1.0 1997-04-22 fl   Created
# 1.1 1997-05-25 fl   Added base64 embedding option (-1)
#     1997-05-25 fl   Check for broken package file
# 1.2 1997-05-26 fl   Support uncompressed packages (-u)
# 1.3 1997-05-27 fl   Check byte code magic, eliminated StringIO, etc.
# 1.4 1997-06-04 fl   Removed last bits of white space, removed try/except
# 1.5 1997-06-17 fl   Added squeeze archive capabilities (-x)
# 1.6 1998-05-04 fl   Minor fixes in preparation for public source release
#
# reviews:
#       "Fredrik Lundh is a friggin genius"
#       -- Aaron Watters, author of 'Internet Programming with Python'
#
#       "I agree ... this is a friggin Good Thing"
#       -- Paul Everitt, Digital Creations
#
# Copyright (c) 1997 by Fredrik Lundh.
# Copyright (c) 1997-1998 by Secret Labs AB
#
# info@pythonware.com
# http://www.pythonware.com
#
# --------------------------------------------------------------------
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted.  This software is provided as is.
# --------------------------------------------------------------------

VERSION = "1.6/1998-05-04"
MAGIC   = "[SQUEEZE]"

import base64, imp, marshal, os, string, sys, md5

# --------------------------------------------------------------------
# usage

def usage():
    print
    print "SQUEEZE", VERSION, "(c) 1997-1998 by Secret Labs AB"
    print """\
Convert a Python application to a compressed module package.

Usage: squeeze [-1ux] -o app [-b start] modules... [-d files...]

This utility creates a compressed package file named "app.pyz", which
contains the given module files.  It also creates a bootstrap script
named "app.py", which loads the package and imports the given "start"
module to get things going.  Example:

        squeeze -o app -b appMain app*.py

The -1 option tells squeeze to put the package file inside the boot-
strap script using base64 encoding.  The result is a single text file
containing the full application.

The -u option disables compression.  Otherwise, the package will be
compressed using zlib, and the user needs zlib to run the resulting
application.

The -d option can be used to put additional files in the package file.
You can access these files via "__main__.open(filename)" (returns a
StringIO file object).

The -x option can be used with -d to create a self-extracting archive,
instead of a package.  When the resulting script is executed, the
data files are extracted.  Omit the -b option in this case.
"""
    sys.exit(1)


# --------------------------------------------------------------------
# squeezer -- collect squeezed modules

class Squeezer:

    def __init__(self):

        self.rawbytes = self.bytes = 0
        self.modules = {}

    def addmodule(self, file):

        if file[-1] == "c":
            file = file[:-1]

        m = os.path.splitext(os.path.split(file)[1])[0]

        # read sourcefile
        f = open(file)
        codestring = f.read()
        f.close()

        # dump to file
        self.modules[m] = compile(codestring, file, "exec")

    def adddata(self, file):

        self.modules["+"+file] = open(file, "rb").read()

    def getarchive(self):

        # marshal our module dictionary
        data = marshal.dumps(self.modules)
        self.rawbytes = len(data)

        # return (compressed) dictionary
        if zlib:
            data = zlib.compress(data, 9)
        self.bytes = len(data)

        return data

    def getstatus(self):
        return self.bytes, self.rawbytes


# --------------------------------------------------------------------
# loader (used in bootstrap code)

loader = """
import ihooks

PYZ_MODULE = 64

class Loader(ihooks.ModuleLoader):

    def __init__(self, modules):
        self.__modules = modules
        return ihooks.ModuleLoader.__init__(self)

    def find_module(self, name, path = None):
        try:
            self.__modules[name]
            return None, None, (None, None, PYZ_MODULE)
        except KeyError:
            return ihooks.ModuleLoader.find_module(self, name, path)

    def load_module(self, name, stuff):
        file, filename, (suff, mode, type) = stuff
        if type != PYZ_MODULE:
            return ihooks.ModuleLoader.load_module(self, name, stuff)
        #print "PYZ:", "import", name
        code = self.__modules[name]
        del self.__modules[name] # no need to keep this one around
        m = self.hooks.add_module(name)
        m.__file__ = filename
        exec code in m.__dict__
        return m

def boot(name, fp, size, offset = 0):

    global data

    try:
        import %(modules)s
    except ImportError:
        #print "PYZ:", "failed to load marshal and zlib libraries"
        return # cannot boot from PYZ file
    #print "PYZ:", "boot from", name+".PYZ"

    # load archive and install import hook
    if offset:
        data = fp[offset:]
    else:
        data = fp.read(size)
        fp.close()

    if len(data) != size:
        raise IOError, "package is truncated"

    data = marshal.loads(%(data)s)

    ihooks.install(ihooks.ModuleImporter(Loader(data)))
"""

loaderopen = """
def open(name):
    import StringIO
    try:
        return StringIO.StringIO(data["+"+name])
    except KeyError:
        raise IOError, (0, "no such file")
"""

loaderexplode = """

def explode():
    for k, v in data.items():
        if k[0] == "+":
            try:
                open(k[1:], "wb").write(v)
                print k[1:], "extracted ok"
            except IOError, v:
                print k[1:], "failed:", "IOError", v

"""

def getloader(data, zlib, package):

    s = loader

    if data:
        if explode:
            s = s + loaderexplode
        else:
            s = s + loaderopen

    if zlib:
        dict = {
            "modules": "marshal, zlib",
            "data":    "zlib.decompress(data)",
            }
    else:
        dict = {
            "modules": "marshal",
            "data":    "data",
            }

    s = s % dict

    return marshal.dumps(compile(s, "<package>", "exec"))


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

#
# parse options

import getopt, glob, sys

try:
    opt, arg = getopt.getopt(sys.argv[1:], "1b:o:suzxd")
except: usage()

app = ""
start = ""
embed = 0
zlib = 1
explode = 0

data = None

for i, v in opt:
    if i == "-o":
        app = v
    elif i == "-b":
        start = "import " + v
    elif i == "-d":
        data = 0
    elif i == "-1":
        embed = 1
    elif i == "-z":
        zlib = 1
    elif i == "-u":
        zlib = 0
    elif i == "-x":
        explode = 1
        start = "explode()"

print app, start

if not app or not start:
    usage()

bootstrap = app + ".py"
archive   = app + ".pyz"

archiveid = app
if explode:
    archiveid = "this is a self-extracting archive. run the script to unpack"
elif embed:
    archiveid = "this is an embedded package"
elif zlib:
    archiveid = "this is a bootstrap script for a compressed package"
else:
    archiveid = "this is a bootstrap script for an uncompressed package"

#
# import compression library (as necessary)

if zlib:
    try:
        import zlib
    except ImportError:
        print "You must have the zlib module to generate compressed archives."
        print "Squeeze will create an uncompressed archive."
        zlib = None

#
# avoid overwriting files not generated by squeeze

try:
    fp = open(bootstrap)
    s = fp.readline()
    s = fp.readline()
    string.index(s, MAGIC)
except IOError:
    pass
except ValueError:
    print bootstrap, "was not created by squeeze.  You have to manually"
    print "remove the file to proceed."
    sys.exit(1)

#
# collect modules

sq = Squeezer()
for patt in arg:
    if patt == "-d":
        data = 0
    else:
        for file in glob.glob(patt):
            if file != bootstrap:
                if data is not None:
                    print file, "(data)"
                    sq.adddata(file)
                    data = data + 1
                else:
                    print file
                    sq.addmodule(file)

package = sq.getarchive()
size = len(package)

#
# get loader

loader = getloader(data, zlib, package)

if zlib:
    zbegin, zend = "zlib.decompress(", ")"
    zimport = 'try:import zlib\n'\
        'except:raise RuntimeError,"requires zlib"\n'
    loader = zlib.compress(loader, 9)
else:
    zbegin = zend = zimport = ""

loaderlen = len(loader)

magic = repr(imp.get_magic())
version = string.split(sys.version)[0]

magictest = 'import imp\n'\
    's="requires python %s or bytecode compatible"\n'\
    'if imp.get_magic()!=%s:raise RuntimeError,s' % (version, magic)

#
# generate script and package files

if embed:

    # embedded archive
    data = base64.encodestring(loader + package)

    fp = open(bootstrap, "w")
    fp.write('''\
#!/usr/bin/env python
#%(MAGIC)s %(archiveid)s
%(magictest)s
%(zimport)simport base64,marshal
s=base64.decodestring("""
%(data)s""")
exec marshal.loads(%(zbegin)ss[:%(loaderlen)d]%(zend)s)
boot("%(app)s",s,%(size)d,%(loaderlen)d)
%(start)s
''' % locals())
    bytes = fp.tell()

else:

    # separate archive file

    fp = open(archive, "wb")

    fp.write(loader)
    fp.write(package)

    bytes = fp.tell()

    #
    # create bootstrap code

    fp = open(bootstrap, "w")
    fp.write("""\
#!/usr/bin/env python
#%(MAGIC)s %(archiveid)s
%(magictest)s
%(zimport)simport marshal,sys,os
for p in filter(os.path.exists,map(lambda p:os.path.join(p,"%(archive)s"),sys.path)):
 f=open(p,"rb")
 exec marshal.loads(%(zbegin)sf.read(%(loaderlen)d)%(zend)s)
 boot("%(app)s",f,%(size)d)
 break
%(start)s # failed to load package
""" % locals())
    bytes = bytes + fp.tell()

#
# show statistics

dummy, rawbytes = sq.getstatus()

print "squeezed", rawbytes, "to", bytes, "bytes",
print "(%d%%)" % (bytes * 100 / rawbytes)
