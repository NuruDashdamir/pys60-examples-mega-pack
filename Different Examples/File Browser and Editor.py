SYMBIANUID=0x01E53698
# File Browser and Editor Version 0.2
# This software is under GPL
# All Nokia components have Copyright (c)  by Nokia 2004
# Some parts of the code are from Nokia's filebrowser.py and 
# from discussions on Nokia developer forum

import os
import appuifw
import e32
import sys
import codecs
from key_codes import *    
import keyword

defvalues = ((0,0,0),u"LatinBold12",(0,0,255),(0,192,0),'normal')
cocolor = (0,255,0)
bookcolor = (0,0,127)

charset = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

editorpath = "e:\\system\\apps\\ppeditor\\"

class myeditor:
    def __init__(self):
        self.mainmenu = [(u'> File',self.filemenu), (u'> Find',self.find_em),(u'Position',self.position),(u'> Python',self.python),(u'> Go to',self.goto),(u'> PPEditor',self.ppmenu)]
        self.script_lock = e32.Ao_lock()
        self.bound = True
        self.dir_stack = []
        self.dirpath="<root>"
        self.last_find=""
        loader = fileloader()
        loader.setfile(editorpath+"editor.dat")
        self.textcolor,self.textfont,self.highcolor,self.opercolor, self.screen = loader.load()
        loader = None 

    def ppmenu(self):
     ppmenu = [u'> Settings',u'> Help',u'About']
     i = appuifw.popup_menu(ppmenu)
     help = pphelp()
     if i == 0:
      settings = ppsettings(self)
      settings.set_values(self.textcolor,self.textfont,self.highcolor,self.opercolor,self.screen)
      settings.showdialog()
     elif i == 1:
      help.help(LANG_ENG)
     elif i == 2:
      help.showabout(LANG_ENG)
     help = None

    def filemenu(self):
     filemenu = [u"Save",u"> New/Open",u"Quit"]
     i = appuifw.popup_menu(filemenu)
     if i == 0:
      self.save()
     elif i == 1:
      self.quit()
      appuifw.app.exit_key_handler = self.exit_key_handler
     elif i == 2:
      self.exit_key_handler()

    def find_em(self):
     findmenu = [u"Find (case insensitive)",u"Find (case sensitive)",u"Replace all"]
     i = appuifw.popup_menu(findmenu)
     if i == 0:
      self.find(False)
     elif i == 1:
      self.find(True)
#     elif i == 2:
#      self.replace(False)
     elif i == 2:
      self.replace(True)

    def estimate(self,bytes):
     if bytes <= 1000:
      koef = 50
     elif 5000 >= bytes > 1000:
      koef = 65
     elif 10000 >= bytes > 5000:
      koef = 80
     elif 17000 >= bytes > 10000:
      koef = 95
     else:
      koef = 115
     return int(round(float(koef) * (float(bytes)/1024.0)))

    def highlight(self):
     if appuifw.query(u'This operation isn\'t optimised. Estimated time is %ds. Continue?'%(self.estimate(self.text.len())),'query'):
      hl = highlighter(self) 
      set = hl.pythonkeywords()
      opset = hl.pythonoperators()
      hl.highlightmemo(self.text,set,opset,self.textcolor,self.highcolor,self.opercolor)

    def python(self):
     pythonmenu = [u'Highlight',u'Run Adv_Console',u'> Bookmarks',u'Execute PY',u'> Insert',u'> Search for']
     i = appuifw.popup_menu(pythonmenu)
     if i == 0:
      self.highlight()
     elif i == 1:
      #e32.start_exe("z:\\system\\programs\\apprun.exe","e:\\system\\apps\\python\\python.app")
      execfile("c:\\Python\\adv_i_console5.py", globals())
      self.refresh()

     elif i == 2:
      self.bookmarks()
     elif i == 3:
      self.runpy()
     elif i == 4:
      self.showmenu()
     elif i == 5:
      self.searchfor()

    def searchfor(self):
     searchformenu = [u'> Overview',u'> Imported modules',u'> Classes',u'> Defs',u'> Global constants']
     i = appuifw.popup_menu(searchformenu)
     if i != None:
      an = pyanalyzer(self)
      if i == 0:
       an.analyze(appuifw.app.body.get())
      elif i == 1:
       an.imports(appuifw.app.body.get())
      elif i == 2:
       an.classes(appuifw.app.body.get())
      elif i == 3:
       an.defs(appuifw.app.body.get())
      elif i == 4:
       an.constants(appuifw.app.body.get())
      an = None
  
    def cd(self,iter,dir,up=True):
     list=iter.list_repr()
     list=self.first(list)
     if up==True:
      list=self.upperlist(list)
      dir=dir.upper().strip()
 #    if list.find(dir)!=-1:  
     iter.add(list.index(dir))
     return iter

    def findth(self,str,chr,pos):
     pos -= 1
     d=0
     for i in range(len(str)):
      if str[i:i+len(chr)] == chr:
       d+=1
      if d == pos:
       return i

  
    def bookmarks(self):
     i=appuifw.popup_menu([u"Go to bookmark 1",u"Go to bookmark 2",u"Go to bookmark 3",u"Set bookmark 1",u"Set bookmark 2",u"Set bookmark 3",u"Clear bookmarks"])
     if i in [3,4,5]:
      pos=appuifw.app.body.get_pos()
      i -= 2 
      self.clearb(i)
      text = appuifw.app.body.get(pos,appuifw.app.body.len())
      appuifw.app.body.set(appuifw.app.body.get(0,pos))
      appuifw.app.body.color=bookcolor
      appuifw.app.body.add(u" #<%d># "%i)
      appuifw.app.body.color=self.textcolor
      appuifw.app.body.add(text)
      appuifw.app.body.set_pos(pos)
     elif i in [0,1,2]:
      i += 1
      txt=appuifw.app.body.get()
      p = txt.find("#<%d>#"%i)
      if p == -1:
       appuifw.note(u"Bookmark %d not set"%i,'info')
      else:
       appuifw.app.body.set_pos(p+3)
     elif i == 6:
      self.clearb(1)
      self.clearb(2)
      self.clearb(3)

    def clearb(self,num):
     i = appuifw.app.body.get_pos()
     txt = appuifw.app.body.get()
     if txt.find("#<%d>#"%num) != -1:
      txt = txt.replace(" #<%d># "%num,"")
      appuifw.app.body.set(txt)
      appuifw.app.body.set_pos(i)

    def goto(self):
     i=appuifw.popup_menu([u"Begin",u"> Line",u"> Percentage",u"> Char",u"End"])
     if i == 0:
      self.begin()
     elif i == 1:
      line=appuifw.query(u"Line (max %d):"%(appuifw.app.body.get().count(u"\u2029")+1),'number')
      if line != None:
       appuifw.app.body.set_pos(self.findth(appuifw.app.body.get(),u"\u2029",line)+1)
     elif i == 2:
      percentage=appuifw.query(u"Percentage:",'number')
      if percentage != None:
       chr=int(round(float(appuifw.app.body.len())*(float(percentage)/100.0)))
       appuifw.app.body.set_pos(chr)
     elif i == 3:
      chr = appuifw.query(u"Char pos (max %d):"%(appuifw.app.body.len()+1),'number')
      if chr != None:
       appuifw.app.body.set_pos(chr)
     elif i == 4:
      appuifw.app.body.set_pos(appuifw.app.body.len())
 
    def begin(self):
     appuifw.app.body.set_pos(0)

    def replace(self,all):
     repby=appuifw.multi_query(u"Replace",u"by")
     if repby != None:
      rep,by = repby
      text1 = appuifw.app.body.get(0,appuifw.app.body.get_pos())
      text2 = appuifw.app.body.get(appuifw.app.body.get_pos(),appuifw.app.body.len())
      if not all:
       if text2.find(rep) == -1:
        if appuifw.query(u"Not found. Search from the begin?",'query'):
         if text1.find(rep) == -1:
          appuifw.note(u"Not found.",'info')
         else:
          pos = text1.find(rep)+len(rep)
          text1 = text1.replace(rep,by)
          appuifw.app.body.set(text1+text2)
          appuifw.app.body.set_pos(pos)
          appuifw.note(u"Replaced succesfully",'conf')
       else:
        pos = text2.find(rep)+len(rep)
        text2 = text2.replace(rep,by)
        appuifw.app.body.set(text1+text2)
        appuifw.app.body.set_pos(pos)
        appuifw.note(u"Replaced succesfully",'conf')
      else:
       if text2.find(rep) == -1:
        if appuifw.query(u"Not found. Search from the begin?",'query'):
         if text1.find(rep) == -1:
          appuifw.query(u"Not found.",'info')
         else:
          c = text1.count(rep)
          text1 = text1.replace(rep,by)
          pos = text1.rfind(rep)+len(rep)
          appuifw.app.body.set(text1+text2)    
          appuifw.app.body.set_pos(pos)
          appuifw.note(u"Replaced %d times"%c,'conf')
       else:
        c = text2.count(rep) 
        pos = text2.rfind(rep)+len(rep)
        text2 = text2.replace(rep,by)
        appuifw.app.body.set(text1+text2)
        appuifw.app.body.set_pos(pos)
        if appuifw.query(u"Replaced %d times. Search from the begin?"%c,'query'):
         c = text1.count(rep) 
         pos = text1.rfind(rep)+len(rep)
         text1 = text1.replace(rep,by)
         appuifw.app.body.set(text1+text2)
         appuifw.app.body.set_pos(pos)
         appuifw.note(u"Replaced %d times"%c,'conf')    

    def find(self,sensitive,text=""):
     t=appuifw.app.body.get()[appuifw.app.body.get_pos()+3:]
     if not sensitive:
      t = t.upper()
     if text=="": 
      f=appuifw.query(u"Find text:",'text',self.last_find)
      if f != None:
       if not sensitive:
        f = f.upper()
     else:
      if self.last_find != None:
       if not sensitive:
        f=self.last_find.upper()
       else:
        f=self.last_find
     if f != None:
      self.last_find=f
      if not sensitive:
       self.last_find=self.last_find.lower()
      p=t.find(f)+appuifw.app.body.get_pos()
      if p == -1 + appuifw.app.body.get_pos():
       if appuifw.query(u"Not found. Search from the begin?",'query'):
        appuifw.app.body.set_pos(0)
        self.find(sensitive,f)
      else:
       appuifw.app.body.set_pos(p+3)

    def upperlist(self,list):
      newlist=[]
      for i in range(0, len(list)):
       if list[i] != None:
        newlist.append(list[i].upper())
      return newlist 

    def first(self,tup):
     a=[]
     for i in range(0,len(tup)):
      a.append(tup[i][0])
     return a

    def lower(self,arr):
     for i in range(len(arr)):
      arr[i]=arr[i].lower()
     return arr
 
    def go(self):
     self.dirpath="e:\\system\\apps\\python\\my\\"
     self.backuplist = self.unic(self.listdir(self.dirpath)) 
     self.lb.set_list(self.backuplist)
     self.dir_stack=[0,0,0,0]

    def showmenu(self):
     m=[u"def declaration",u"class declaration",u"for cycle",u"for i in range cycle",u"main function",u"import",u"import all"]
     i=appuifw.popup_menu(m)
     if i!=None:
      pos=appuifw.app.body.get_pos()
      text1 = appuifw.app.body.get(0,appuifw.app.body.get_pos())
      if i == 0:
       text2 = "def ():\n   \n   "
       pos += 4
      elif i == 1:
       text2="class :\n def __init__(self):\n  \n  "
       pos += 6
      elif i == 2:
       text2 = "for in :\n \n "
       pos += 4
      elif i == 3:
       text2 = "for i in range(, ):\n \n"
       pos += 15
      elif i == 4:
       text2 = "if __name__ == \"__main__\":\n main()"
       pos += len(text2)
      elif i == 5:
       text2 = "import "
       pos += 7
      elif i == 6:
       text2 = "from  import *"
       pos += 5
      text3 = appuifw.app.body.get(appuifw.app.body.get_pos())
      appuifw.app.body.set(text1+text2+text3)
      appuifw.app.body.set_pos(pos)

    def position(self):
     percentage = float(appuifw.app.body.get_pos())/float(appuifw.app.body.len())*100
     char,chars=appuifw.app.body.get_pos()+1,appuifw.app.body.len()+1
     line=appuifw.app.body.get(0,char).count(u"\u2029")+1
     lines=appuifw.app.body.get().count(u"\u2029")+1
     name=self.filename[self.filename.rindex("\\")+1:]
     s=u"%s\n%.2f%%\nLine %d of %d\nChar %d of %d"%(name,percentage,line,lines,char,chars)
     appuifw.note(s,'info')

    def runpy(self):
     ch=appuifw.Content_handler()
     #ch.open_standalone(self.path.replace("/","\\"))  
     execfile(self.path.replace("/","\\"), globals())
     self.refresh()

    def cycle(self):
     if appuifw.app.body.current() == 0:
      e32.ao_yield() 
      appuifw.app.body.set_list(self.entries,len(self.entries)+10)

    def debind(self):
    # self.backup_handler = appuifw.app.exit_key_handler
   #  appuifw.app.exit_key_handler = self.emptyhandler
     self.bound = False

    def emptyhandler(self):
     pass
 
    def rebind(self):
   #  appuifw.app.exit_key_handler = self.backup_handler
     self.bound = True

    def run(self):
        self.oldscreen=appuifw.app.screen
        appuifw.app.screen = self.screen
        if self.dirpath=="<root>":
         entries=e32.drive_list()
        else:
         entries = self.listdir(self.dirpath)
        if not self.dirpath=="<root>":
            entries.insert(0, u"..")
        self.entries=entries
        self.lb = appuifw.Listbox(entries, self.observe)
        self.lb.bind(EKeyLeftArrow, lambda: self.observe(-1))
        self.lb.bind(EKeyRightArrow, self.observe)
        self.lb.bind(EKeyYes, self.go)
        self.lb.bind(EKeyUpArrow, self.cycle)
        old_title = appuifw.app.title
        self.refresh()
        self.script_lock.wait()
        appuifw.app.title = old_title
        appuifw.app.body = None
        appuifw.app.screen=self.oldscreen
        self.lb = None

    def refresh(self):
        appuifw.app.title = u"PPEditor"
        appuifw.app.menu = []
        appuifw.app.exit_key_handler = self.exit_key_handler
        appuifw.app.body = self.lb

    def do_exit(self):
        self.exit_key_handler()

    def exit_key_handler(self):
        appuifw.app.exit_key_handler = None
        self.script_lock.signal()
        if appuifw.app.full_name()[-10:] != "Python.app":
         appuifw.app.set_exit()
 
    def fonts(self):
     f = appuifw.available_fonts()
     i = appuifw.popup_menu(f)
     if i != None:
      appuifw.app.body.font = f[i]
      pos = appuifw.app.body.get_pos()
      appuifw.app.body.set(appuifw.app.body.get())
      appuifw.app.body.set_pos(pos)

    def observe(self, ind = None):
        if (ind == -1) and (self.dirpath == "<root>"):
         return
        if not ind == None:
            index = ind
        else:
            index = self.lb.current()
        if self.dirpath != "<root>":
          dalist = self.unic(self.listdir(self.dirpath))
        focused_item = 0
        if self.dirpath=="<root>":
            self.dir_stack.append(index)
            self.dirpath=e32.drive_list()[index]
        elif index == -1:
         if self.dir_stack != []:
          if self.dirpath != "<root>":
            focused_item = self.dir_stack.pop()
            self.popdir()
            self.backuplist = dalist
            self.lb.set_list(self.backuplist)
        elif os.path.isdir(self.dirpath+"\\"+self.backuplist[index].replace('> ','')):
            self.dir_stack.append(index)
            self.dirpath+="\\"+self.backuplist[index].replace('> ','')
        elif os.path.isfile(self.dirpath+"\\"+self.backuplist[index]):
            self.item = os.path.join(self.dirpath,self.backuplist[index])
            path=unicode(os.path.splitext(self.item)[0]+(os.path.splitext(self.item)[1]))
            if path.find("\\") == -1:
             path=path[:2]+u"\\"+path[2:]      
            self.path=path
            self.debind()
            i = appuifw.popup_menu([u"Edit (UTF-8)", u"Delete", u"New", u"Exit"])
            self.rebind()
            if i == 0:
                self.text=appuifw.Text()
                self.text.color = self.textcolor
                self.text.font = unicode(self.textfont)
               # appuifw.app.body = self.text
                appuifw.app.body.bind(EKeyYes,self.fonts) 
                (encoding,decoding,reader,writer) = codecs.lookup('UTF-8')
                input = reader(open(path,'rb'))
                self.filename=path.replace("/","\\")
                try:
                 ex=False
                 s=input.read()
                except UnicodeError:
                 ex=True
                 appuifw.note(u'Failed to decode UTF-8','error')
                if not ex:  
                 appuifw.app.body = self.text
                 appuifw.app.body.set(s)
                 appuifw.app.body.set_pos(0)
                 appuifw.app.menu = self.mainmenu
                 appuifw.app.exit_key_handler = self.filemenu
            elif i == 1:
                if appuifw.query(u"Really delete entry?",'query'):
                    os.remove(self.item)
                    focused_item = index
                else:
                    pass
            elif i == 2:
             fn=appuifw.query(u"Filename:",'text')
             if fn != None:
              fn = (path[:path.rfind("\\")]+"\\"+fn).replace('/','\\')
              debug(fn) 
              self.text=appuifw.Text()
              self.text.color = self.textcolor
              self.text.font = self.textfont
              appuifw.app.body = self.text
              appuifw.app.body.color=self.textcolor
              appuifw.app.body.bind(EKeyYes,self.fonts) 
              self.filename=fn
              appuifw.app.body.set_pos(0)
              appuifw.app.menu = self.mainmenu
            else:
                if not self.bound:
                 if appuifw.query(u"Really exit?",'query'):
                    self.do_exit() 
        if self.dirpath=="<root>":
         entries=e32.drive_list()
        else:
         entries = self.listdir(self.dirpath) 
        entries=self.unic(entries)
        self.backuplist = entries
        self.lb.set_list(entries, focused_item)
        self.entries,self.cur=entries,self.lb.current()==0    
    def unic(self,arr):
     for i in range(len(arr)):
      arr[i]=unicode(arr[i])
     return arr

    def listdir(self,dirpath):
     if dirpath=="<root>":
      return e32.drive_list()
     else:
      dir=os.listdir(dirpath)
      dir=self.sortdir(dir,dirpath)
      if dir==[]:
       dir=[u"<empty>"]
      return dir

    def sortdir(self,arr,path):
     dirs = files = []
     for i in range(len(arr)):
      if os.path.isdir(os.path.join(path,arr[i])): 
        dirs.append(u'> '+arr[i])
      elif os.path.isfile(os.path.join(path,arr[i])):
       if not files.__contains__(arr[i]):
        files.append(arr[i])
     dirs.sort(self.sortcallback)
     files.sort(self.sortcallback)
#     return dirs + files
     return files

    def sortcallback(self,a,b):
     arr = [a.upper(),b.upper()]
     arr.sort()
     if arr[0] == a.upper():
      return -1
     return 1

    def gc(self,dir):
     y=0
     for i in range(len(dir)):
      if os.path.isdir(self.dirpath+"\\"+dir[i]):
       y+=1
     return y

    def move(self,arr,fr,to):
     text=arr[fr]
     arr.remove(text)
     arr.insert(to,text)
     return arr 

    def popdir(self):
     if len(self.dirpath)<4:
      self.dirpath="<root>"
     elif self.dirpath[-1:] != "\\":
      self.dirpath=self.dirpath[:self.dirpath.rfind("\\")]
     elif self.dirpath=="<root>":
      pass
     else:
      self.dirpath=self.dirpath[:self.dirpath.rfind("\\")]
      self.dirpath=self.dirpath[:self.dirpath.rfind("\\")]

    def splitfile(self,text):
     a=[]
     c=0
     s=""
     for i in range(len(text)):
      c += 1
      s += text[i]
      if c == 20:
       a.append(s)
       s = ""
       c = 0
      elif i == (len(text)-1):
       a.append(s)
     return a

    def save(self):
        path = self.filename
#        path=unicode(os.path.splitext(self.item)[0]+os.path.splitext(self.item)[1])
        text=appuifw.app.body.get().encode('utf8')
        text=text.replace("\xE2\x80\xA9","\x0D\x0A")
        open(path,'wb').write(text)


    def quit(self):
        self.refresh()
        pass

    def chartoline(self,char):
     return appuifw.app.body.get(0,char).count(u"\u2029") + 1

    def refreshset(self,textcolor,textfont,highcolor,opercolor,screen):
     self.textcolor,self.textfont,self.highcolor,self.opercolor,self.screen=textcolor,textfont,highcolor,opercolor,screen
     txt = self.text.get()
     pos = self.text.get_pos()
     self.text.font = unicode(textfont)
     self.text.color = textcolor
     self.text.set(txt)
     self.text.set_pos(pos)
     appuifw.app.screen = screen


class pyanalyzer:
 def __init__(self,editor):
  self.box=appuifw.Listbox([u"."],self.event)
  self.editor=editor

 def up(self):
  appuifw.app.exit_key_handler = self.old_handler
  appuifw.app.body = self.old_body
  appuifw.app.menu = self.old_menu

 def constants(self,text):
  arr = text.split(u"\u2029")
  ar2 = []
  for i in range(len(arr)):
   if len(arr[i]) == len(arr[i].strip()):
    if (arr[i].find("#") == -1 == arr[i].find("def") == arr[i].find("==")) and (arr[i].find("=") != -1):
     ar2.append((i+1,u"%d: %s"%(i+1,arr[i])))
  if ar2 == []:
   appuifw.note(u"No global constants found",'info')
   return
  self.items=ar2
  items=self.second(ar2)
  self.box.set_list(items)
  self.old_body = appuifw.app.body
  self.old_handler = appuifw.app.exit_key_handler
  self.old_menu = appuifw.app.menu
  appuifw.app.menu = []
  appuifw.app.body = self.box
  appuifw.app.exit_key_handler = self.up
     

 def classes(self,text):
  arr=[]
  orig=text
  word="class "
  le=len(word)
  for i in range(1,text.count(word)+1):
   x=text.find(word)
   text2=text[:x]
   text2=text[text2.rfind(u"\u2029")+1:x+text[x:].find(u"\u2029")].strip()
   text=text[x+le:]
   if (text2[text2.find(word)+len(word):].find(':') != -1) and (orig[orig.find(text2)-1] in [u"\u2029","\n"," "]) and (text2[0:5] == "class"):
    line=self.editor.chartoline(orig.find(text2))   
    arr.append((line,u"%d: %s"%(line,text2)))
  arr.sort()
  self.items=arr
  items=self.second(arr)
  if items == []:
   appuifw.note(u'No classes found','info')
  else:
   self.box.set_list(items)
   self.old_body = appuifw.app.body
   self.old_handler = appuifw.app.exit_key_handler
   self.old_menu = appuifw.app.menu
   appuifw.app.menu = []
   appuifw.app.body = self.box
   appuifw.app.exit_key_handler = self.up

 def analyze(self,text):
  arr=[]
  orig=text
  ar2 = text.split(u"\u2029")
  for i in range(len(ar2)):
   if len(ar2[i]) == len(ar2[i].strip()):
    if (ar2[i].find("#") == -1 == ar2[i].find("def") == ar2[i].find("==")) and (ar2[i].find("=") != -1):
     arr.append((i+1,u"%d: %s"%(i+1,ar2[i])))
  word="#<"
  le=len(word)
  if text.find(word) != -1:
   x=text.find(word)
   text2=text[:x]
   text2=text[text2.rfind(u"\u2029")+1:x+text[x:].find(u"\u2029")].strip()
   if text2 in ["#<1>#","#<2>#","#<3>#"]:
    p = {"#<1>#":"Bookmark 1","#<2>#":"Bookmark 2","#<3>#":"Bookmark 3"}
    line=self.editor.chartoline(orig.find(text2))   
    arr.append((line,u"%d: %s"%(line,p[text2])))
  text=orig 
  word="def "
  le=len(word)
  for i in range(1,text.count(word)+1):
   x=text.find(word)
   text2=text[:x]
   text2=text[text2.rfind(u"\u2029")+1:x+text[x:].find(u"\u2029")].strip()
   text=text[x+le:]
   if (text2[text2.find(word)+len(word):].find("(") != -1) and (text2[text2.find("(")+1:].find("):") != -1) and (text2[0:3] == "def"):
    line=self.editor.chartoline(orig.find(text2))   
    arr.append((line,u"%d: %s"%(line,text2)))
  text=orig
  word="class "
  le=len(word)
  for i in range(1,text.count(word)+1):
   x=text.find(word)
   text2=text[:x]
   text2=text[text2.rfind(u"\u2029")+1:x+text[x:].find(u"\u2029")].strip()
   text=text[x+le:]
   if (text2[text2.find(word)+len(word):].find(':') != -1) and (orig[orig.find(text2)-1] in [u"\u2029","\n"," "]) and (text2[0:5] == "class"):
    line=self.editor.chartoline(orig.find(text2))   
    arr.append((line,u"%d: %s"%(line,text2)))
  text=orig
  word,word2="import ","from "
  le,le2=len(word),len(word2)
  for i in range(1,text.count(word)+1):
   x=text.find(word)
   text2=text[:x]
   text2=text[text2.rfind(u"\u2029")+1:x+text[x:].find(u"\u2029")].strip()
   text=text[x+le:]
   if (text2[:7] == "import ") or (text2[:5] == "from "):
    line=self.editor.chartoline(orig.find(text2))   
    arr.append((line,u"%d: %s"%(line,text2)))
  arr.sort()
  self.items=arr
  items=self.second(arr)
  if items == []:
   appuifw.note(u'Nothing interesting found','info')
  else:
   self.box.set_list(items)
   self.old_body = appuifw.app.body
   self.old_handler = appuifw.app.exit_key_handler
   self.old_menu = appuifw.app.menu
   appuifw.app.menu = []
   appuifw.app.body = self.box
   appuifw.app.exit_key_handler = self.up

 def defs(self,text):
  arr=[]
  orig=text
  word="def "
  le=len(word)
  for i in range(1,text.count(word)+1):
   x=text.find(word)
   text2=text[:x]
   text2=text[text2.rfind(u"\u2029")+1:x+text[x:].find(u"\u2029")].strip()
   text=text[x+le:]
   if (text2[text2.find(word)+len(word):].find("(") != -1) and (text2[text2.find("(")+1:].find("):") != -1) and (text2[0:3] == "def"):
    line=self.editor.chartoline(orig.find(text2))   
    if not arr.__contains__((line,u"%d: %s"%(line,text2))):
     arr.append((line,u"%d: %s"%(line,text2)))
  arr.sort()
  self.items=arr
  items=self.second(arr)
  if items == []:
   appuifw.note(u'No defs found','info')
  else:
   self.box.set_list(items)
   self.old_body = appuifw.app.body
   self.old_handler = appuifw.app.exit_key_handler
   self.old_menu = appuifw.app.menu
   appuifw.app.menu = []
   appuifw.app.body = self.box
   appuifw.app.exit_key_handler = self.up

 def imports(self,text):
  arr=[]
  orig=text
  word,word2="import ","from "
  le,le2=len(word),len(word2)
  for i in range(1,text.count(word)+1):
   x=text.find(word)
   text2=text[:x]
   text2=text[text2.rfind(u"\u2029")+1:x+text[x:].find(u"\u2029")].strip()
   text=text[x+le:]
   if (text2[:7] == "import ") or (text2[:5] == "from "):
    line=self.editor.chartoline(orig.find(text2))   
    arr.append((line,u"%d: %s"%(line,text2)))
  arr.sort()
  self.items=arr
  items=self.second(arr)
  if items == []:
   appuifw.note(u'No imported modules found','info')
  else:
   self.box.set_list(items)
   self.old_body = appuifw.app.body
   self.old_handler = appuifw.app.exit_key_handler
   self.old_menu = appuifw.app.menu
   appuifw.app.menu = []
   appuifw.app.body = self.box
   appuifw.app.exit_key_handler = self.up
 
 def event(self):
  line=self.items[self.box.current()][0]
  self.up()
  appuifw.app.body.set_pos(self.editor.findth(appuifw.app.body.get(),u"\u2029",line)+1)

 def second(self,arr):
  a=[]
  for i in range(len(arr)):
   a.append(arr[i][1])
  return a

class highlighter:
 def __init__(self,editor):
  self.editor = editor

 def highlightmemo(self,memo,set,opset,origcolor,highcolor,opcolor):
  text = memo.get()
  pos = memo.get_pos()
  set += opset
  hav = self.firstfound(text,set)
  inittext = text[:text.find(hav)]
  memo.set(inittext)
  while hav != None:
   p = text.find(hav)
   text1 = text[:p]
   text2 = text[p+len(hav):]
   if hav in opset:
    memo.color = opcolor
   else:
    if not (text2[0] in charset): 
     memo.color = highcolor
   memo.add(unicode(hav))
   memo.color = origcolor
   text = text1 + self.empty(len(hav)) + text2
   hav = self.firstfound(text,set)
   if hav != None:
    i3 = text2.find(hav)
   text3 = text2[:i3]
   memo.add(text3)
  memo.set_pos(pos)
 
 def empty(self,count):
  a = ""
  for i in range(count):
   a += " "
  return unicode(a)

 def firstfound(self,text,set):
  r = []
  for i in range(len(set)):
   idx=text.find(set[i])
   if idx == -1:
    idx = len(text)
   r.append((idx,i,set[i]))
  n = self.first(r).index(min(self.first(r)))
  if r[n][0] == len(text):
   return None
  return r[n][2]

 def lastfound(self,text,set):
  r = []
  for i in range(len(set)):
   idx=text.rfind(set[i])
   r.append((idx,i,set[i]))
  n = self.first(r).index(max(self.first(r)))
  if r[n][0] == -1:
   return None
  return r[n][2]
 
 def first(self,arr):
  x = []
  for i in range(len(arr)):
   x.append(arr[i][0])
  return x

 def pythonkeywords(self):
  return keyword.kwlist + ["self","__init__"]

 def pythonoperators(self):
  return ['+','-','*','/','=','!=','>','<','(',')','[',']',',','{','}',':']

LANG_ENG = 0
LANG_CZE = 1

lang_defs = {LANG_ENG : 'eng', LANG_CZE : 'cze'}

class pphelp:
 def __init__(self):
  self.text = appuifw.Text()

 def bakscr(self):
  self.scr, self.tit = appuifw.app.screen, appuifw.app.title
  
 def restscr(self):
  appuifw.app.screen, appuifw.app.title = self.scr, self.tit 

 def help(self,lang):
  self.bakscr()
  appuifw.app.screen = 'normal'
  appuifw.app.title = u'PPEditor help'
  fn = editorpath+"help\\"+lang_defs[lang]+".hlp"
  if not os.path.isfile(fn):
   appuifw.note(u'Help file for current language not found.','info')
   self.restscr()
   return
  f = open(fn,'r')
  li = f.readlines()
  f.close()
  for i in range(len(li)):
   li[i] = unicode(li[i].replace('\n','').replace('\r',''))
#   print li[i][len(li[i])-1]
  index = appuifw.selection_list(li)
  if index == None:
   self.restscr()
   return
  fn = editorpath+"help\\"+lang_defs[lang]+"_%.2d"%index+".hlp"
  f = open(fn, 'r')
  li = f.readlines()
  f.close()
  if li[0].replace('\r','').replace('\n','') == '[text]':
   self.disptext(unicode(li[1]))
  elif li[0].replace('\r','').replace('\n','') == '[list]':
   li.remove(li[0])
   for i in range(len(li)):
    li[i] = unicode(li[i].replace('\n','').replace('\r',''))
   ind = appuifw.selection_list(li)
   if ind == None:
    self.restscr()
    return
   fn = editorpath+"help\\"+lang_defs[lang]+"_%.2d_%.2d"%(index,ind)+".hlp"
   f = open(fn, 'r')
   li = f.readlines()
   f.close()
   if li[0].replace('\r','').replace('\n','') == '[text]':
    self.disptext(unicode(li[1]))

#  self.restscr()
  
 #<1># 

 def disptext(self,text):
  self.menu_, self.body_,self.hand_ = appuifw.app.menu,appuifw.app.body,appuifw.app.exit_key_handler
  tx = appuifw.Text()
  tx.font = u'LatinBold12'
  tx.color = (0,0,0)
  tx.set(text)
  tx.set_pos(0)
  appuifw.app.body = tx
  appuifw.app.menu = [(u"Back", self.retup)]
  appuifw.app.exit_key_handler = self.retup
  
 def retup(self):
  appuifw.app.menu, appuifw.app.body, appuifw.app.exit_key_handler = self.menu_,self.body_,self.hand_
  self.restscr()

 def up(self):
  (appuifw.app.body,appuifw.app.menu,appuifw.app.exit_key_handler) = self.olds

 def showabout(self,lang):
  self.text.color = (0,0,0)
  self.text.set(self.about(lang))
  self.olds = (appuifw.app.body,appuifw.app.menu,appuifw.app.exit_key_handler)
  appuifw.app.body = self.text
  self.text.set_pos(0)
  appuifw.app.exit_key_handler = self.up
  appuifw.app.menu = []

 def about(self,lang):
  strs = [u"PPEditor 1.0 - Python Programmer's Editor\n\nCreated by Zen - (c) 2005\nBased on \"myeditor.py\"\nGNU/GPL license\n\nhttp://www.gigahosting.cz/zen/\nYou can report your bugs or wishes to z-en@seznam.cz or icq 200430161."]
  return strs[lang]
 
class fileloader:
 def __init__(self):
  self.file = ""

 def setfile(self,file):
  self.file = file

 def translatecolor(self,ct):
  (r,g,b) = ct
  return (r << 16) | (g << 8) | b

 def mergecolor(self,mc):
  r = mc >> 16
  g = mc - ((mc >> 16) << 16) >> 8
  b = mc - ((mc >> 16) << 16) - ((mc - ((mc >> 16) << 16) >> 8) << 8)
  return r,g,b

 def save(self,textcolor,textfont,highcolor,opercolor,screen):
  assert self.file != ""
  f = open(self.file,'w')
  c = self.translatecolor(textcolor)
  f.write("settings file\n")
  f.write(str(c)+"\n")
  f.write(textfont+"\n")
  c = self.translatecolor(highcolor)
  f.write(str(c)+"\n")
  c = self.translatecolor(opercolor)
  f.write(str(c)+"\n")
  f.write(screen)
  f.close()
  
 def load(self):
  assert self.file != ""
  if not os.path.isfile(self.file):
   return defvalues
  f = open(self.file,'r')
  lines = f.readlines()
  if lines[0].find("settings") == -1:
   appuifw.note(u"Corrupted settings file",'error')
   return defvalues
  textcolor=self.mergecolor(int(lines[1]))
  textfont=unicode(lines[2])
  if textfont.find("\n") != -1:
   textfont = textfont[:-1]
  highcolor=self.mergecolor(int(lines[3]))
  opercolor=self.mergecolor(int(lines[4]))
  screen=lines[5]
  f.close()
  return textcolor,textfont,highcolor,opercolor,screen

settingslist=[u"Text color: ",u"Font: ",u"Highlight: ",u"Oper. color: ",u"Screen: "]

colors={(0,0,0) : u"Black",(255,255,255) : u"White",(255,0,0) : u"Red", (0,255,0) : u"Green", (0,0,255) : u"Blue", (0xC0,0xC0,0xC0): u"Silver"}

screens={'full' : u"Full screen", 'normal' : u"Normal screen"}

class ppsettings:
 def __init__(self,editor):
  self.editor = editor
  self.box = appuifw.Listbox([u"."],self.event)
  self.items = settingslist
  self.textcolor,self.textfont,self.highcolor,self.opercolor,self.screen = (0,0,0),u"",(0,0,0),(0,0,0),'normal'

 def backit(self):
  settingslist=[u"Text color: ",u"Font: ",u"Highlight: ",u"Oper. color: ",u"Screen: "]

 def set_values(self,textcolor,textfont,highcolor,opercolor,screen):
  self.textcolor = textcolor
  self.textfont = textfont
  self.highcolor = highcolor
  self.opercolor = opercolor
  self.screen = screen

 def lbrefresh(self,index = 0):
  self.box.set_list(self.items,index)

 def showdialog(self):
  global settingslist
  self.lbrefresh(0)
  self.items = settingslist
  if self.textcolor in colors.keys():
   self.items[0] += colors[self.textcolor]
  else:
   self.items[0] += str(self.textcolor).replace(" ","")
  self.items[1] += self.textfont 
  if self.highcolor in colors.keys():
   self.items[2] += colors[self.highcolor]
  else:
   self.items[2] += str(self.highcolor).replace(" ","")
  if self.opercolor in colors.keys():
   self.items[3] += colors[self.opercolor]
  else:
   self.items[3] += str(self.opercolor).replace(" ","")
  if self.screen in screens.keys():
   self.items[4] += screens[self.screen]
  else:
   self.items[4] += self.screen
  self.olds = (appuifw.app.body,appuifw.app.menu,appuifw.app.exit_key_handler)
  self.box.set_list(self.items)
  appuifw.app.body = self.box
  appuifw.app.menu = []
  appuifw.app.exit_key_handler = self.up

 def up(self):
  loader = fileloader()
  loader.setfile(editorpath+"editor.dat")
  loader.save(self.textcolor,self.textfont,self.highcolor,self.opercolor,self.screen)
  (appuifw.app.body,appuifw.app.menu,appuifw.app.exit_key_handler) = self.olds
  self.editor.refreshset(self.textcolor,self.textfont,self.highcolor,self.opercolor,self.screen)
  loader = None  

 def colorselect(self,d):
  i = appuifw.popup_menu(colors.values()+[u"> Custom"])
  if i == len(colors.values()):
   r = appuifw.query(u'Red (0-255)','number')
   if r in range(0,256):
    g = appuifw.query(u'Green (0-255)','number')
    if g in range(0,256):
     b = appuifw.query(u'Blue (0-255)','number')
     if b in range(0,256):
      return self.bintostr((r,g,b)).replace(" ","")
     else:
      appuifw.note(u'Incorrect value','error')
      return d
    else:
     appuifw.note(u'Incorrect value','error')
     return d
   else:
    appuifw.note(u'Incorrect value','error')
    return d
  elif i != None:
   return colors.values()[i]
  else:
   return d

 def strtobin(self,str):
  if colors.values().__contains__(str):
   i = colors.values().index(str)
   return colors.keys()[i]
  else:
   str = str.replace("(","").replace(")","")
   r,g,b = str.split(",")
   return (int(r),int(g),int(b))

 def bintostr(self,bin):
  if colors.keys().__contains__(bin):
   return colors[bin]
  else:
   return str(bin).replace(" ","")

 def event(self):
  i = self.box.current()
  global settingslist
  settingslist=[u"Text color: ",u"Font: ",u"Highlight: ",u"Oper. color: ",u"Screen: "]
  if i == 0:
   color = self.colorselect(self.bintostr(self.textcolor))
   self.items[0] = settingslist[0]+color
   self.textcolor=self.strtobin(color)
   self.lbrefresh(0)
  elif i == 1:
   fonts = appuifw.available_fonts()
   font = appuifw.popup_menu(fonts)
   if font != None:
    self.textfont = fonts[font]
    self.items[1] = settingslist[1] + self.textfont
    self.lbrefresh(1)
  elif i == 2:
   color = self.colorselect(self.bintostr(self.highcolor))
   self.items[2] = settingslist[2]+color
   self.highcolor=self.strtobin(color)
   self.lbrefresh(2)
  elif i == 3:
   color = self.colorselect(self.bintostr(self.opercolor))
   self.items[3] = settingslist[3]+color
   self.opercolor=self.strtobin(color)
   self.lbrefresh(3)
  elif i == 4:
   scr = appuifw.popup_menu(screens.values())
   if scr != None:
    self.screen = screens.keys()[scr]
    self.items[4] = settingslist[4] + screens.values()[scr]
    self.lbrefresh(4)


def debug(a=u"debug"):
 appuifw.note(unicode(a),'info')

if __name__ == '__main__':
    myeditor().run()
