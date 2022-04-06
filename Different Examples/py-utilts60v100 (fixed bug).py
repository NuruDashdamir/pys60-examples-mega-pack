#Copyright (c) 2008 Smart Python
#Small Utilties

import time,e32,appuifw,os.path
from graphics import *

canvas = None
nerr = 0
ner=0


class PyUtilS60:
    def __init__(self):
        appuifw.app.body=canvas=appuifw.Canvas(event_callback=self.handle_event)
        canvas.clear(0x0099cc)
        canvas.text((57,20),u'PyUtilS60',font=(u'Nokia Sans S60',20,1),fill=0x000000)

    def handle_event(self,event):
        code=event['scancode']
        if event['type'] == 2:
            self.displayTxt(u'')

    def displayTxt(self,txt):
        appuifw.app.body=canvas=appuifw.Canvas(event_callback=self.handle_event)
        canvas.clear(0x0099cc)
        canvas.text((57,20),u'PyUtilS60 v1.00',font=(u'Nokia Sans S60',20,1),fill=0x000000)
        canvas.text((20,40),u'Utility Program for Symbian Phones',font=(u'Nokia Sans S60',12,1),fill=0x000069)   
        canvas.text((35,220),u'http://s60python.blogspot.com',font=(u'Nokia Sans S60',12,1),fill=0x00ff0ff)
        if nerr == 0:
            canvas.text((50,100),u'Capps Off Enabled',font=(u'Nokia Sans S60',14,1),fill=0x33ff33)
        else:
            canvas.text((50,100),u'Please enable Capps Off',font=(u'Nokia Sans S60',14,1),fill=0xff3366)

    def utilities(self):
        self.displayTxt(u'')
        self.showWarn()
        ap = [(u"Clean Real player history"),(u"Clean Startup applications"),(u"Remove Stucked installation files"),(u"Theme Remover")]
        o = appuifw.popup_menu(ap,u'Select Option')
        if o==None:
            print u''
        elif o ==0:
            self.cleanUtil(u'Real player history')
        elif o ==1:
            self.displayTxt(u'')
            oa=appuifw.query(u"Are you sure to clear startup . This will clear all applications from startup ","query")
            if oa==1:             
                self.cleanUtil(u'Startup applications')
            else:
                print u''
        elif o ==2:
            self.cleanUtil(u'Stucked installation files')
        elif o ==3:
            self.themeRemover()
        else:
            print u''

    def themeRemover(self):
        self.displayTxt(u'')
        appuifw.note(u"Fetching themes    Please wait ...","info")
        dname=u"c:\\sys\\install\\sisregistry\\a00000eb\\"
        nbk=0
        themeName = []
        dirName = []
        tFName = []

        try:
            for entry in os.listdir(dname):
                nbk=nbk+1
                if os.path.splitext(entry)[1] == '.reg' and nbk>3:
                    fname=dname+entry
                    try:
                        fp = open(fname,"r")
                        f =fp.read()
                        fp.close()
                        nt = f.find("8Unknown")
                        if nt ==-1:
                            nt =20
                        np = f.find(":\private")
                        ntd = f.find("import")
                        dname = f[np-1]
                        tname = f[5:nt]
                        tdname = f[ntd+7:ntd+23]
                        themeName.append(u''+tname+u'')
                        tFName.append(entry)
                        dirName.append(dname+tdname)
                    except Exception,e:
                        print u''
        except Exception,e:
            print u""
        ad=str(themeName)    
        
        if  ad != u'[]':
            self.displayTxt(u'')
            o = appuifw.popup_menu(themeName,u'Select theme for remove')
            if o==None:
                print u''
            else:
                self.remThemefiles(themeName[o],dirName[o],tFName[o])
        else:
            appuifw.note(u"No Theme found.  Check whether the caps off enabled","info")
        self.displayTxt(u'')

    def remThemefiles(self,tnm,tdir,tfn):
        self.displayTxt(u'')
        drName=tdir[0]
        drtName=tdir[1:len(tdir)]
        dname1=drName+u":\\PRIVATE\\10207114\\import\\"+drtName+"\\"
        dname2=drName+u":\\resource\\skins\\"+drtName+"\\"
        dname3=u":\\sys\\install\\sisregistry\\a00000eb\\"
        fname5=u":\\PRIVATE\\10202dce\\a00000eb.sis"
        fname1=u'themepackage.mbm'
        fname2=u'themepackage.mif'
        fname3=u'themepackage.skn'
        ntfn=tfn.find(".reg")
        fname4=tfn[0:ntfn]+u'_0000.ctl'
        self.displayTxt(u'')
        oa=appuifw.query(u"Are you sure to remove theme "+tnm,"query")
        if oa==1: 
            self.displayTxt(u'')
            appuifw.note(u"Uninstalling theme "+tnm,"info")
            chk = self.remFile(dname1+fname3)
            if chk == 0:
                self.remFile(dname1+drtName+u'.ini') 
                self.remFile(u'c'+dname3+tfn)
                self.remFile(u'c'+dname3+fname4)
                self.remFile(u'e'+dname3+fname4)
                self.remFile(u'c'+fname5)
                self.remFile(u'e'+fname5)
                self.remFile(dname2+fname1)
                self.remFile(dname2+fname2)
                self.remFile(dname1+fname1)
                self.remFile(dname1+fname2)
                try:
                    os.rmdir(dname1)
                except Exception,e:
                    print u''
                try:
                    os.rmdir(dname2)
                except Exception,e:
                    print u''
                self.displayTxt(u'')
                appuifw.note(u"Theme deleted successfully","conf")
            else :
                appuifw.note(u"Unable to delete. theme already in use","error")
                    
        self.displayTxt(u'')

    def remFile(self,fname):
        if 1:
        
            try:
                f = file(fname,"r")
                f.close()
                os.remove(fname)
                return 0
            except Exception,e:
                return 1

    def cleanUtil(self,choice):
        if choice == 'Real player history':
            fname=u"c:\\PRIVATE\\10005A3E\\mediaplayer.dat"
        elif choice == 'Startup applications':
            fname=u"c:\\PRIVATE\\100059c9\\start.dat"
        elif choice == 'Stucked installation files':
            dcname=u"c:\\PRIVATE\\10202dce\\"
            dename=u"e:\\PRIVATE\\10202dce\\"
            try:
                for entry in os.listdir(dename):
                    if os.path.splitext(entry)[1] == '.sis':
                        os.remove(dename+entry)
                for centry in os.listdir(dcname):
                    if os.path.splitext(centry)[1] == '.sis' or os.path.splitext(centry)[1] == '.sisx':
                        os.remove(dcname+centry)
                appuifw.note(u"%s cleared"%choice,"conf")    
            except Exception,e:
                appuifw.note(u"Please enable Caps Off","info")
        if choice != 'Stucked installation files':
            try:
                f = file(fname,"r")
                f.close()
                os.remove(fname)
                appuifw.note(u"%s cleared"%choice,"conf")
            except Exception,e:
                print u''
                ea = str(e)
                ec = ea.find('Errno 2')
                if ec == -1 :
                    appuifw.note(u"Please enable Caps Off","info")
                else:
                    appuifw.note(u"%s already cleared"%choice,"conf")    
        self.displayTxt(u'')

    def showWarn(self):
        global nerr
        global ner
        fname=u"z:\\sys\\bin\\installserver.exe"
        try:
            fp = open(fname,"r")
            f =fp.read()
            fp.close()
            nerr=0
        except Exception,e:
            if ner==0:
                appuifw.note(u"caps off not enabled","info")
                ner=1
            nerr=1
        self.displayTxt(u'')

    def quit(self):
        print u"PyUtilS60 v1.00  from Sujesh"
        print u"SSSLC   A Smart Python Project"
        print u"http://s60python.blogspot.com"
        lock.signal()

    def about(self):
        self.displayTxt(u'')
        appuifw.note(u"PyUtilS60 v1.00\nfrom Sujesh\nssslc A Smart Python Project")    
        self.displayTxt(u'')

sw = PyUtilS60()
lock = e32.Ao_lock()
def menu(s):
    appmenu = [(u"Utilities",sw.utilities),(u"About",sw.about),(u"Exit",sw.quit)]
    appuifw.app.menu = appmenu
    
appuifw.app.screen='normal'     
appuifw.app.exit_key_handler = sw.quit
sw.displayTxt(u'')
menu(0)
sw.showWarn()
sw.displayTxt(u'')
lock.wait()