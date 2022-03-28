#
# View MBM - Look inside MBM and MIF files
#
# Copyright (c) 2009 Jouni Miettunen
# http://jouni.miettunen.googlepages.com/
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
#
# ### Tip for Windows:
# How to find MBM files and count how many picteres they contain:
# for %%a in (C:\Symbian\9.2\S60_3rd_FP1\Epoc32\release\winscw\udeb\z\resource\apps\*.mbm) do bmconv /v %%a
#
# Better readability if you do:
# scan_mbm.bat | grep containing > results.txt

DEBUG = False
#DEBUG = True

'''
1.30 2009-05-30 integrated Marcelo Barros MIF file format analysis
     http://discussion.forum.nokia.com/forum/showthread.php?t=168938
     FIX: MIF index different PyS60 1.4.5 vs. 1.9.5
1.20 2009-05-28
     NEW: Support MIF files
     New: Title shows filename and item count
     New: Updated routine to detect used PyS60 version
1.10 2009-05-26
     NEW: Dynamic MBM file scanning in z:\resource\apps directory
     NEW: Dynamic count of graphics items inside MBM file
     FIX: Better error handling
1.00 2009-03-30 Initial release
'''

VERSION = "1.30"

import os
import e32
import appuifw

lb = None
my_files = []
my_list = []

# TODO: some MBM files generate error, check file format:
# http://www.newlc.com/article.php3?id_article=59

# === How to Count Number of Bitmaps in a MBM File
# http://wiki.forum.nokia.com/index.php/How_to_count_number_of_bitmaps_in_a_mbm_file
# quote start
from struct import unpack
def readL(f, pos=None):
    if pos is not None:
        f.seek(pos)
    return unpack('L', f.read(4))[0]

# the real counting function
def mbm_count(mbm_file):
    f = open(mbm_file, 'rb')
    mbm_type = readL(f)
    if mbm_type == 0x10000041:  # mbm on ROM (Z:)
        return readL(f)
    elif mbm_type == 0x10000037L:  # mbm on file (normal)
        return readL(f, readL(f, 16)) # read at trailer
    else:       # what type is it?
        return None
# quote end

def mif_count(a_file):
    ''' Count how many items inside MIF file '''
    f = open(a_file, 'rb')
    # 42 23 23 34 02 - own MIF file type 2
    # 42 23 23 34 03 - avkon2.mif type 3
    # Indexing: Look inside file and MBG, thanx to wizard_hu_ for tips
    f.seek(12)
    return unpack('<L',f.read(4))[0]

def scan_icons(a_dir):
    ''' Search MBM and MIF files in given folder '''
    # TODO: scan any given filetypes, use dictionary?
    global my_files
    my_files = [os.path.join(a_dir, f) for f in os.listdir(a_dir) if f.endswith(".mbm") or f.endswith(".mif")]

    if e32.pys60_version_info > (1,9):
        # PyS60 1.9.x and above
        my_files.sort(key=str.lower)
    else:
        # Pys60 1.4.x or below
        my_files.sort(lambda x, y: cmp(x.lower(), y.lower()))

    #if DEBUG:
    #    b = 3

    global my_list
    my_list = []
    for i in my_files:
        dummy, name = os.path.split(i)
        my_list.append(unicode(name))

        # DEBUG
        #if b:
        #    b -= 1
        #else:
        #    break

    global lb
    lb = appuifw.Listbox(my_list, cb_select)
    menu_init()

def cb_select():
    ''' Callback for listbox item selection event '''
    index = lb.current()
    f_path = my_files[index]
    dummy, f_name = os.path.split(f_path)
    show_icons(unicode(f_name), unicode(f_path))

def show_icons(a_title, a_file, maskfunc=lambda x:x):
    ''' Create new Listbox with given parameters '''
    # a_title: change application title, show list name
    # a_file: get icons from this file, with full path
    # id_list: icon id numbers to show,  must be list ### REMOVED
    # maskfunc: define icon mask number algorithm
    #     show_icons(range(0,100,2), lambda x:x+1)
    #     icon number: 0, 2, 4, 6, 8, 10 etc.
    #     mask number: icon number + 1

    # http://snippets.dzone.com/posts/show/1482
    # You can define more complex mask algoriths
    #     if type(id_list) == int:
    #         id_list = [id_list] # one item
    #     if type(maskfunc) == dict:  # allow dict as a func
    #         func = lambda id: maskfunc.get(id,id)
    #     else:
    #         func = maskfunc

    # S60 3.1 emulator with PyS60 1.4.5
    # operatoranimation.mif
    # splashscreen.mif
    # S60 1.4.5 S60 5.0 emulator:
    # apn.mbm
    # webkit.mbm
    # Trustboots.mbm
    # S60 5.0 device with PyS60 1.9.5
    # browserbitmaps.mbm
    # default_app_icon.mbm
    # enhancedsoftkeybitmap...
    # GSTvoutStandbyFigure.m...

    # Defect: browserbitmaps.mbm
    # N82 PyS60 1.4.5: ok
    # N82 PyS60 1.9.5: error

    # Get all icons from given file.mbm
    entries = []
    try:
        start = 0
        count = 0
        skip = 1
        if a_file.endswith(".mbm"):
            count = mbm_count(a_file)
            a_title = unicode(str("%s (%d)" % (a_title, count)))

        elif a_file.endswith(".mif"):
            # Todo: how to calculate items inside MIF
            count = mif_count(a_file)
            a_title = unicode(str("%s (%d)" % (a_title, count/2)))
            # PyS60 1.9.5 in S60 3.1 emulator:
            # AknIcon 5 panic
            # index greater than the range of TInt16 (that is, above 32767)
            #start = 16384
            if e32.pys60_version_info > (1,9):
                start = 0
            else:
                start = 16384
            count += start
            skip = 2

        for i in range(start, count, skip):
            # 2-row listbox item to show bigger icon
            row1 = u"Icon: %s" % i
            row2 = u"Mask: %s" % maskfunc(i)
            # Problem: returns "valid" icon even with invalid data
            icon = appuifw.Icon(a_file, i, maskfunc(i))
            entries.append((row1, row2, icon))

    finally:
        # Hox: if you try to "see" more icons that file contains
        # SymbianError: [Errno -25] KErrEof

        try:
            # Make the new listbox visible
            if len(entries):
                appuifw.app.body = appuifw.Listbox(entries)
                appuifw.app.exit_key_handler=menu_init
                appuifw.app.menu = [
                    (u"Back", menu_init),
                    (u"About", menu_about),
                    (u"Exit", cb_quit)
                ]
                appuifw.app.title = a_title
        except:
            # Todo: debug why appuifw.Listbox() fails with some files
            s = str("Failed to show %d icons (%d)" % (len(entries), (count-start)/skip))
            appuifw.note(unicode(s))
            menu_init()

def menu_init():
    ''' Go to startup state '''
    appuifw.app.title = u"View MBM"
    appuifw.app.exit_key_handler=cb_quit
    appuifw.app.menu = [
        (u"View", cb_select),
        (u"About", menu_about),
        (u"Exit", cb_quit)
    ]
    appuifw.app.body = lb
    e32.ao_yield()

def menu_about():
    ''' Callback for menu item About '''
    appuifw.note(u'View MBM v' + VERSION + u'\n' +\
        u'jouni.miettunen.googlepages.com\n\u00a92009 Jouni Miettunen')

def cb_quit():
    ''' Cleanup before exit '''
    app_lock.signal()

# Initialize application UI
lb = appuifw.Listbox([u"Please wait,", u"...searching for", u"...icons files"])
menu_init()

# Search for potential icon files
scan_icons("z:\\resource\\apps\\")
#scan_icons("e:\\data\\python\\")
#scan_icons("c:\\python\\")

# Wait for user to do anything
app_lock = e32.Ao_lock()
app_lock.wait()
