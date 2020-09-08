#
# rescleanup.py v0.2
#
# A script to cleanup drives from unneeded application resource and help files
# on Series 60.
#      
# Copyright (c) 2008 ph77
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

import os
import appuifw
import e32
import re
import shutil
import globalui

_byteconv = [
    (1<<20L, " MB"), 
    (1<<10L, " KB"),
    (1, " bytes")
]

def bytestr(size, precision=1):
    """Return a string representing the bytes"""
    if size==1:
        return u"1 byte"
    for factor, suffix in _byteconv:
        if size >= factor:
            break
    float_string_split = `size/float(factor)`.split('.')
    integer_part = float_string_split[0]
    decimal_part = float_string_split[1]
    if int(decimal_part[0:precision]):
        float_string = '.'.join([integer_part, decimal_part[0:precision]])
    else:
        float_string = integer_part
    return unicode(float_string + suffix)

# A menu driven Application class
class Py7App:

    class Py7Scr:
        def __init__(self, type, item, parent=None, callback=None, menu=None, help=None):
            self.parent=parent
            if type=="list":
                self.uicontrol=appuifw.Listbox(item, callback)
            elif type=="text":
                self.uicontrol=appuifw.Text(item)
            else:
                self.uicontrol=None
            self.menu=menu
            self.help=help

    def __init__(self, title, about):
        self.script_lock = e32.Ao_lock()
        self.title=title
        self.about=about
        self.screen=None
        self.screens=[]

    def run(self):
        old_title = appuifw.app.title
        appuifw.app.title = self.title
        appuifw.app.exit_key_handler = self.onExit
        self.showScreen(0)
        self.script_lock.wait()
        appuifw.app.title = old_title
        appuifw.app.body = None
        for index in range(0, len(self.screens)):
            self.screens[index].uicontrol = None

    def showScreen(self, index):
        self.screen=index
        appuifw.app.body = self.screens[index].uicontrol
        if self.screens[index].menu:
            appuifw.app.menu = self.screens[index].menu
        else:
            appuifw.app.menu = []

    def addScreen(self, type, item, parent=None, callback=None, menu=None, help=None):
        from key_codes import EKeyLeftArrow, EKeyRightArrow
        screen=Py7App.Py7Scr(type, item, parent, callback, menu, help)
        if screen.uicontrol:
            if parent is not None:
                screen.uicontrol.bind(EKeyLeftArrow, self.onExit)
            if callback:
                screen.uicontrol.bind(EKeyRightArrow, callback)
            self.screens.append(screen)
            return len(self.screens)-1
        return -1

    def currentControl(self):
        return self.screens[self.screen].uicontrol
        
    def currentChoice(self):
        return self.currentControl().current()

    def onAbout(self):
        self.info(self.about)

    def onHelp(self):
        if self.screens[self.screen].help:
            self.info(self.screens[self.screen].help)

    def onExit(self):
        if self.screens[self.screen].parent is not None:
            self.showScreen(self.screens[self.screen].parent)
        else:
            appuifw.app.exit_key_handler = None
            self.script_lock.signal()

    def info(self, s):
        appuifw.note(s, "info")

    def error(self, s):
        appuifw.note(s, "error")

    def question(self, s):
        return appuifw.query(s, "query")



# The Main App
class ResCleanup(Py7App):
    S_TITLE     = u"Resource cleanup"
    S_ABOUT     = u"Resource cleanup by ph77@SymbianFreak\nversion 0.2\n"
    S_BACKUP    = u"Keep backup"
    S_NOBACKUP  = u"Don't keep backup"
    S_CLEANUP   = u"Cleaning... Please wait\n"
    S_RESTORE   = u"Restoring from backup... Please wait\n"
    S_CLEANUP_DONE = u"Done!\nRemoved %d files,\ntotal size %s\n"
    S_RESTORE_DONE = u"Done!\nRestored %d files,\ntotal size %s\n"
    
    S_HELP_INIT = u"This script deletes application resource & help files of unneeded languages. "+\
                  u"You need to have a hacked phone and disabled capabilities before you start. "+\
                  u"Use it VERY carefully or some applications wiil fail to start. "+\
                  u"Make sure to use the backup option. You can restore the files later or move them to the pc. "+\
                  u"Note that several applications use only English (UK) resources so it is recommended to keep that language.\n"+\
                  u"http://ph7lab.googlepages.com/s60resourcecleanup"
    S_HELP_LANGUAGES = u"Select the languages which you want to keep."
    S_HELP_DRIVES    = u"Select the drives on which you want to perform cleanup."
    S_HELP_BACKUP    = u"Enable/disable the backup option. It will placed in e:\\ResourceBackup and you can restore it later."

    S_CONFIRM_CLEANUP_WBACKUP  = u"Are you sure that you want to perform the cleanup with the current settings? A backup will be created."
    S_CONFIRM_CLEANUP_NOBACKUP = u"Are you sure that you want to perform the cleanup with the current settings? NO BACKUP WILL BE CREATED!"
    S_CONFIRM_STOP             = u"Work is in progress. Do you want to stop it?"
    
    S_ERROR_NO_LANGUAGES            = u"No languages selected!\nAborting.\n"
    S_ERROR_NO_DRIVES               = u"No drives selected!\nAborting.\n"
    S_ERROR_NO_BACKUP               = u"No backup option selected!\nAborting.\n"
    S_ERROR_FAILED_TO_CREATE_DIR    = u"Failed to create directory '%s'.\nAborting.\n"
    S_ERROR_FAILED_TO_COPY_FILE     = u"Failed to copy file from '%s' to '%s'.\nAborting.\n"
    S_ERROR_FAILED_TO_DELETE_FILE   = u"Failed to delete file '%s'.\nAborting.\n"
    S_ERROR_BACKUP_DIR_NOT_FOUND    = u"Backup directory '%s' not found. Unable to restore files!\n"

    LANGUAGES=(
        ("English (UK)",	        1),
        ("French",	                2),
        ("German",	                3),
        ("Spanish",	                4),
        ("Italian",	                5),
        ("Swedish",	                6),
        ("Danish",	                7),
        ("Norwegian",	            8),
        ("Finnish",	                9),
        ("English (American)",	    10),
        ("Swiss French",	        11),
        ("Swiss German",	        12),
        ("Portuguese",	            13),
        ("Turkish",	                14),
        ("Icelandic",	            15),
        ("Russian",	                16),
        ("Hungarian",	            17),
        ("Dutch",	                18),
        ("Belgian Flemish",	        19),
        ("English (Australian)",	20),
        ("Belgian French",	        21),
        ("German (Austrian)",	    22),
        ("English (New Zealand)",	23),
        ("French (International)",	24),
        ("Czech",	                25),
        ("Slovak",	                26),
        ("Polish",	                27),
        ("Slovenian",	            28),
        ("Chinese (Taiwan)",	    29),
        ("Chinese (Hong Kong)",	    30),
        ("Chinese (China)",	        31),
        ("Japanese",	            32),
        ("Thai",	                33),
        ("Afrikaans",	            34),
        ("Albanian",	            35),
        ("Amharic",		            36),
        ("Arabic",		            37),
        ("Armenian",	            38),
        ("Tagalog",	                39),
        ("Belarussian",		        40),
        ("Bengali",                 41),
        ("Bulgarian",	            42),
        ("Burmese",	                43),
        ("Catalan",	                44),
        ("Croatian",	            45),
        ("English (Canadian)",	    46),
        ("English (International)",	47),
        ("English (South African)",	48),
        ("Estonian",	            49),
        ("Farsi",	                50),
        ("French (Canadian)",	    51),
        ("Gaelic",	                52),
        ("Georgian",	            53),
        ("Greek",	                54),
        ("Greek (Cyprus)",	        55),
        ("Gujarati",	            56),
        ("Hebrew",	                57),
        ("Hindi",	                58),
        ("Indonesian",	            59),
        ("Irish",	                60),
        ("Swiss Italian",	        61),
        ("Kannada",	                62),
        ("Kazakh",	                63),
        ("Khmer",	                64),
        ("Korean",	                65),
        ("Laothian",	            66),
        ("Latvian",	                67),
        ("Lithuanian",	            68),
        ("Macedonian",	            69),
        ("Malay",	                70),
        ("Malayalam",	            71),
        ("Marathi",	                72),
        ("Moldovian",	            73),
        ("Mongolian",	            74),
        ("Norwegian Nynorsk",	    75),
        ("Brazilian Portuguese",	76),
        ("Punjabi",	                77),
        ("Romanian",	            78),
        ("Serbian",	                79),
        ("Sinhalese",	            80),
        ("Somali",	                81),
        ("Spanish (International)",	82),
        ("Spanish (Latin American)",83),
        ("Swahili",	                84),
        ("Swedish (Finland)",	    85),
        ("Tamil",	                87),
        ("Telugu",	                88),
        ("Tibetan",	                89),
        ("Tigrinya",	            90),
        ("Turkish (Cyprus)",	    91),
        ("Turkmen",	                92),
        ("Ukrainian",	            93),
        ("Urdu",	                94),
        ("Vietnamese",	            96),
        ("Welsh",	                97),
        ("Zulu",	                98),
    )

    def __init__(self):
        # init app
        Py7App.__init__(self, self.S_TITLE, self.S_ABOUT)

        # prepare init choices
        MBM_AVKON=u"z:\\resource\\apps\\avkon2.mbm"
        if os.path.isfile(MBM_AVKON):
            self.initChoices= [
                (u"Help",    u"read me",     appuifw.Icon(MBM_AVKON, 16574, 16575)), 
                (u"Cleanup", u"wizard",      appuifw.Icon(MBM_AVKON, 16570, 16571)),
                (u"Restore", u"from backup", appuifw.Icon(MBM_AVKON, 16592, 16593))
            ]
        else:
            self.initChoices= [
                (u"Help",    u"read me"), 
                (u"Cleanup", u"wizard"),
                (u"Restore", u"from backup")
            ]
        
        # prepare languages list
        self.langlist=[]
        self.langindex2code={}
        for lang, code in self.LANGUAGES:
            index=len(self.langlist)
            self.langindex2code[index]=code
            self.langlist.append(unicode("%02d %s" % (code, lang)))

        self.reres=re.compile("\.[rh](\d{2})\d?")

        # prepare drives list
        self.drivelist=[]
        for item in (u"C:",u"E:"):
            if os.path.isdir(item+"\\Resource"):
                self.drivelist.append(unicode(item))

        # prepare backup list
        self.backupdir="e:\\ResourceBackup"
        self.backuplist=[self.S_BACKUP,self.S_NOBACKUP]

        # set menus
        menuInit = [
                (u"Cleanup wizard", self.doCleanup),
                (u"Restore from backup", self.doRestore),
                (u"Help", lambda: self.showScreen(self.SCREEN_HELP)),
                (u"About", self.onAbout),
                (u"Exit", self.onExit),
        ]
        menuBare = [
                (u"About", self.onAbout),
                (u"Exit", self.onExit),
        ]

        # set UI elements   
        self.SCREEN_INIT     =self.addScreen("list", self.initChoices,      None,                 self.onChoice, menuInit,  None)
        self.SCREEN_HELP     =self.addScreen("text", self.S_HELP_INIT,      self.SCREEN_INIT,     None,          menuBare,  None)
        self.SCREEN_CLEANUP  =self.addScreen("text", self.S_CLEANUP,        self.SCREEN_INIT,     None,          menuBare,  None)
        self.SCREEN_RESTORE  =self.addScreen("text", self.S_RESTORE,        self.SCREEN_INIT,     None,          menuBare,  None)
        self.working=False
        self.abort=False

    def onChoice(self):
        if self.screen==self.SCREEN_INIT:
            index = self.currentChoice()
            if index==0:
                self.showScreen(self.SCREEN_HELP)
            elif index==1:
                self.doCleanup()
            elif index==2:
                self.doRestore()

    def doCleanup(self):
        self.info(self.S_HELP_LANGUAGES)
        result=appuifw.multi_selection_list(self.langlist, search_field=1)
        languages=[]
        for index in result:
            languages.append(self.langindex2code[index])
        if len(languages)==0:
            self.error(self.S_ERROR_NO_LANGUAGES)
            return

        self.info(self.S_HELP_DRIVES)
        result=appuifw.multi_selection_list(self.drivelist)
        drives=[]
        for index in result:
            drives.append(self.drivelist[index])
        if len(drives)==0:
            self.error(self.S_ERROR_NO_DRIVES)
            return

        self.info(self.S_HELP_BACKUP)
        result=appuifw.selection_list(self.backuplist)
        if result is None:
            self.error(self.S_ERROR_NO_BACKUP)
            return
            
        self.backupEnabled=(result==0)
        if self.backupEnabled:
            squestion=self.S_CONFIRM_CLEANUP_WBACKUP
        else:
            squestion=self.S_CONFIRM_CLEANUP_NOBACKUP

        if True!=self.question(squestion):
            return
        
        if self.backupEnabled:
            if not self.makedir(self.backupdir):
                return
        
        txt=self.screens[self.SCREEN_CLEANUP].uicontrol
        txt.clear()
        txt.add(self.S_CLEANUP)
        self.showScreen(self.SCREEN_CLEANUP)
        self.working=True
        self.abort=False
        data=[0,0]
        for drive in drives:
            e32.ao_yield()
            if self.abort:
                break
            if self.backupEnabled:
                newdir=self.backupdir+"\\"+drive[0]+"\\Resource"
                if not self.makedir(newdir):
                    txt.add(self.S_ERROR_FAILED_TO_CREATE_DIR % (unicode(newdir)))
                    break
            if not self.cleanupFolder(drive+"\\Resource", languages, data, txt):
                break
        inf=unicode(self.S_CLEANUP_DONE % (data[0], bytestr(data[1])))
        txt.add(inf)
        self.info(inf)
        self.working=False

    def cleanupFolder(self, folder, languages, data, txt):
        items=os.listdir(folder)
        for item in items:
            e32.ao_yield()
            if self.abort:
                return False
            path=folder+"\\"+item
            if os.path.isdir(path):
                if not self.cleanupFolder(path, languages, data, txt):
                    return False
            elif os.path.isfile(path):
                ext=os.path.splitext(item)[1].lower()
                m = self.reres.match(ext)
                if m is not None:
                    langid = int(m.groups()[0])
                    if langid not in languages:
                        txt.add(unicode(path+"\n"))
                        filesize=os.path.getsize(path)
                        if self.backupEnabled:
                            newdir=os.path.join(self.backupdir,folder[0],folder[3:])
                            if not self.makedir(newdir):
                                txt.add(self.S_ERROR_FAILED_TO_CREATE_DIR % (unicode(newdir)))
                                return False
                            path2=os.path.join(self.backupdir,path[0],path[3:])
                            if not self.copyfile(path, path2):
                                txt.add(self.S_ERROR_FAILED_TO_COPY_FILE % (unicode(path), unicode(path2)))
                                return False
                        if not self.delfile(path):
                            txt.add(self.S_ERROR_FAILED_TO_DELETE_FILE % (unicode(path)))
                            return False
                        data[0]+=1
                        data[1]+=filesize

        return True

    def doRestore(self):
        if not os.path.isdir(self.backupdir):
            self.error(self.S_ERROR_BACKUP_DIR_NOT_FOUND % (unicode(self.backupdir)))
            return
        txt=self.screens[self.SCREEN_RESTORE].uicontrol
        txt.clear()
        txt.add(self.S_RESTORE)
        self.showScreen(self.SCREEN_RESTORE)
        self.working=True
        self.abort=False
        e32.ao_yield()
        data=[0,0]
        self.restoreFolder(self.backupdir, data, txt)
        inf=unicode(self.S_RESTORE_DONE % (data[0], bytestr(data[1])))
        txt.add(inf)
        self.info(inf)
        self.working=False
        
    def restoreFolder(self, folder, data, txt):
        items=os.listdir(folder)
        for item in items:
            e32.ao_yield()
            if self.abort:
                return False
            path=folder+"\\"+item
            if os.path.isdir(path):
                if not self.restoreFolder(path, data, txt):
                    return False
            elif os.path.isfile(path):
                filesize=os.path.getsize(path)
                path2=path[len(self.backupdir)+1:]
                path2=path2[0]+":"+path2[1:]
                txt.add(unicode(path2+"\n"))
                if not self.copyfile(path, path2):
                    txt.add(self.S_ERROR_FAILED_TO_COPY_FILE % (unicode(path), unicode(path2)))
                    return False
                if not self.delfile(path):
                    txt.add(self.S_ERROR_FAILED_TO_DELETE_FILE % (unicode(path)))
                    return False
                data[0]+=1
                data[1]+=filesize
        return True
    
    def onExit(self):
        if self.working:
            if True==self.question(self.S_CONFIRM_STOP):
                self.abort=True
                self.working=False
            return
        Py7App.onExit(self)
    
    def makedir(self, path):
        if not os.path.isdir(path):
            try: os.makedirs(path)
            except:
                self.error(self.S_ERROR_FAILED_TO_CREATE_DIR % (unicode(path)))
                return False
        return True

    def copyfile(self, path, path2):
        try: shutil.copyfile(path, path2)
        except:
            self.error(self.S_ERROR_FAILED_TO_COPY_FILE % (unicode(path), unicode(path2)))
            return False
        return True

    def delfile(self, path):
        try: os.remove(path)
        except:
            self.error(self.S_ERROR_FAILED_TO_DELETE_FILE % (unicode(path)))
            return False
        return True

if __name__ == "__main__":
    ResCleanup().run()
