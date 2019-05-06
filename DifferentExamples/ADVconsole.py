#
# adv_i_console.py
#
# An implementation of a  interactive Python console based on interactive_console.py for
# Series 60 Python environment. Based on 'code' module and
# 'series60_console'.
#     
# Copyright (c) 2004 Nokia. All rights reserved.
# version 5
from __future__ import generators
import os
import appuifw
from key_codes import EKeyDevice3,EKeyYes
import sys
import types
import re
import keyword

r_endword = re.compile(r'[A-Za-z0-9_]+$')
r_startword = re.compile(r'^[A-Za-z0-9_]+')

class Py_console:
    def __init__(self, console):
        self.co = console
        self.co.control.bind(EKeyYes, self.eval_cmd)
        self.co.control.bind(EKeyDevice3, self.menu_joy)
        self.history = []
        self.history_item = 4
        self.import_path = u'E:\\system\\libs\\'
        self.app_name= u'aiCON\n'
        self.app_ver= u'v alpha 5'
        self.run_by = u''
        self.run_by_mode = u''
        self.old_exit_key_handler = appuifw.app.exit_key_handler
        self.mod_builtin =list(sys.builtin_module_names)
        # self.mod_builtin =[u'binascii',u'cStringIO',u'errno',u'exceptions',u'imp',u'marshal',u'math',u'md5',u'struct',u'sys',u'thread',u'time',u'xreadlines']
        self.unique_id = self.genid()
        self.init_t9()
        self.dic_t9 = {u'a':u'abcABC',u'd':u'defDEF',u'g':u'ghiGHI',u'j':u'jklJKL',u'm':u'mnoMNO',u'p':u'pqrsPQRS',u't':u'tuv',u'w':u'wxyzWXYZ'}
        self.dic_t2chars = {u'b':u'aa',u'c':u'aaa',u'e':u'dd',u'f':u'ddd',u'h':u'gg',u'i':u'ggg',u'k':u'jj',u'l':u'jjj',u'n':u'mm',u'o':u'mmm',u'q':u'pp',u'r':u'ppp',u's':u'pppp',u'u':u'tt',u'v':u'ttt',u'x':u'ww',u'y':u'www',u'z':u'wwww',u'a':u'a',u'd':u'd',u'g':u'g',u'j':u'j',u'm':u'm',u'p':u'p',u't':u't',u'w':u'w'}
        self.reset_ps()


    def getword(self, input, pos):
        """From Sean B. Palmer, http://inamidst.com/sbp/"""
        try: eword = r_endword.search(input[:pos]).group(0)
        except AttributeError: eword = '' 
        try: sword = r_startword.match(input[pos:]).group(0)
        except AttributeError: sword = ''
        if not (eword or sword): return None
        return eword + sword

    def is_module(self,obj):
      return isinstance(obj,types.ModuleType)

    def init_t9(self):
       s=''     
       for i in range(0,255+1):
         s=s+chr(i)
       self.t9=s[:64+1]+'aaadddgggjjjmmmpppptttwwww'+s[91:96+1]+'aaadddgggjjjmmmpppptttwwww'+s[123:]  

    def genid(self,iv=1):    
      id = iv
      while 1:
       yield id
       id+=1    
      
    def import_sel(self):
       filelist = os.listdir(self.import_path)
       ll = []
       for file in filelist:
         base,ext = os.path.splitext(file)
         if ext == u'.py':
           ll.append(unicode(base))
       ll.sort()
       ind = appuifw.selection_list(ll)
       if ind is not None:
         n = ll[ind]  
         self.co.write(u'import '+n)
         self.eval_cmd()   
         
    def import_all_sel(self):
       filelist = os.listdir(self.import_path)
       ll = []
       for file in filelist:
         base,ext = os.path.splitext(file)
         if ext == u'.py':
           ll.append(unicode(base))
       ll.sort()
       ind = appuifw.selection_list(ll)
       if ind is not None:
         n = ll[ind]  
         self.co.write(u'from '+n+u' import *')
         self.eval_cmd()

    def modfn_sel(self):
       filelist = dir(self)
       # filelist = [u'sysa',u'types']
       ll = []
       # self.is_module(eval(file))
       for file in filelist:
        try:
         eval(file)
        except:
         pass
        else:
         if self.is_module(eval(file)):
           ll.append(unicode(file))
       ll.sort()
       ind = appuifw.selection_list(ll)
       if ind is not None:
         n0 = ll[ind]  
         self.co.write(u''+n0)
         filelist = eval(u'dir('+n0+ u')')
         ll = []
         for file in filelist:
           if 1:
            ll.append(unicode(file))
         ll.sort()
         ind = appuifw.selection_list(ll)
         if ind is not None:
          n1 = ll[ind]  
          self.co.write(u'.'+n1)
          filelist = eval(u'dir('+n0+u'.'+n1+ u')')
          ll = []
          for file in filelist:
            if 1:
             ll.append(unicode(file))
          ll.sort()
          ind = appuifw.selection_list(ll)
          if ind is not None:
           n2 = ll[ind]  
           self.co.write(u'.'+n2)

    def keyw_sel(self):
       filelist = keyword.kwlist
       ll = []
       for file in filelist:
           ll.append(unicode(file))
       ll.sort()
       ind = appuifw.selection_list(ll)
       if ind is not None:
         n0 = ll[ind]  
         self.co.write(u''+n0)

    def menu_joy(self):
       list1 = [u'Symbol',u'Python Keyword',u'Import ...',u'Module.Function',u'Introspection ...',u'Info Tech ...'] 
       ind1 = appuifw.popup_menu(list1)
       if ind1 >= 0:
          if ind1 == 0:
            self.popsymb()
          elif ind1 == 1:
            self.keyw_sel()
          elif ind1 == 2:
            self.popimport()
          elif ind1 == 3:
            self.modfn_sel()
          elif ind1 == 4:
            self.popintros()
          elif ind1 == 5:
            self.poptech()
       else:
          appuifw.note(u'Cancel','conf')

    def poptech(self):
       list1 = [u'Is Module ...',u'T9 ...'] 
       ind1 = appuifw.popup_menu(list1)
       if ind1 >= 0:
          if ind1 == 0:
            self.popismod()
          elif ind1 == 1:
            self.popt9()
       else:
          appuifw.note(u'Cancel','conf')

    def popsymb(self):
       list1 = [u'__',u'()',u'[]',u'{}',u"''"] 
       ind1 = appuifw.popup_menu(list1)
       if ind1 >= 0:
          if ind1 == 0:
            self.symbol__()
          elif ind1 == 1:
            self.symbolpar()
          elif ind1 == 2:
            self.symbolbra()
          elif ind1 == 3:
            self.symbolaco()
          elif ind1 == 4:
            self.symbolquotes()
       else:
          appuifw.note(u'Cancel','conf')

    def popimport(self):
       list1 = [u'import _',u'from _ import all',u'import _ select',u'from _ import all select'] 
       ind1 = appuifw.popup_menu(list1)
       if ind1 >= 0:
          if ind1 == 0:
            self.import_s()
          elif ind1 == 1:
            self.import_all()
          elif ind1 == 2:
            self.import_sel()
          elif ind1 == 3:
            self.import_all_sel()
       else:
          appuifw.note(u'Cancel','conf')
          
    def poplocal(self):
       b = locals()
       ll = []
       ll = map(unicode,b)
       ll.sort()
       ind = appuifw.selection_list(ll)
       if ind is not None:
         n0 = ll[ind]  
         self.co.write(u''+n0)
         filelist = eval(u'dir('+n0+ u')')
         ll = []
         for file in filelist:
           if 1:
            ll.append(unicode(file))
         ll.sort()
         ind = appuifw.selection_list(ll)
         if ind is not None:
          n1 = ll[ind]  
          self.co.write(u'.'+n1)
          filelist = eval(u'dir('+n0+u'.'+n1+ u')')
          ll = []
          for file in filelist:
            if 1:
             ll.append(unicode(file))
          ll.sort()
          ind = appuifw.selection_list(ll)
          if ind is not None:
           n2 = ll[ind]  
           self.co.write(u'.'+n2)

    def popglobal(self):
       b = globals()
       ll = []
       ll = map(unicode,b)
       ll.sort()
       ind = appuifw.selection_list(ll)
       if ind is not None:
         n0 = ll[ind]  
         self.co.write(u''+n0)
         filelist = eval(u'dir('+n0+ u')')
         ll = []
         for file in filelist:
           if 1:
            ll.append(unicode(file))
         ll.sort()
         ind = appuifw.selection_list(ll)
         if ind is not None:
          n1 = ll[ind]  
          self.co.write(u'.'+n1)
          filelist = eval(u'dir('+n0+u'.'+n1+ u')')
          ll = []
          for file in filelist:
            if 1:
             ll.append(unicode(file))
          ll.sort()
          ind = appuifw.selection_list(ll)
          if ind is not None:
           n2 = ll[ind]  
           self.co.write(u'.'+n2)

    def popintros(self):
       list1 = [u'dir()',u'dir ...',u'Local',u'Global'] 
       ind1 = appuifw.popup_menu(list1)
       if ind1 >= 0:
          if ind1 == 0:
            self.dircns()
          elif ind1 == 1:
            self.diro()
          elif ind1 == 2:
            self.poplocal()
          elif ind1 == 3:
            self.popglobal()
       else:
          appuifw.note(u'Cancel','conf')


    def pophistory(self):
       list1 = [u"Command history",u'Clear history'] 
       ind1 = appuifw.popup_menu(list1)
       if ind1 >= 0:
          if ind1 == 0:
            self.cmd_history()
          elif ind1 == 1:
            self.clear_history()
       else:
          appuifw.note(u'Cancel','conf')

    def reset_ps(self):
        sys.ps1 = u'0 >'
        sys.ps2 = u'...  ' 

    def eval_cmd(self):
        self.co.write(u'\n')
        id = unicode(self.unique_id.next())
        sys.ps1 = id+u' >'
        sys.ps2 = id+u'...' 
        self.co.input_wait_lock.signal()

    def readfunc(self, prompt):
        self.co.write(unicode(prompt))
        user_input = self.co.readline()
        self.history.append(user_input)
        # self.history.pop(0)
        # self.history_item = 4
        return user_input

    def cmd_history(self):
       # return self.history
       ll = []
       for file in self.history:
         ll.append(unicode(file))
       ind = appuifw.selection_list(ll)
       if ind is not None:
         n = ll[ind]  
         self.co.write(u''+n)

    def diro(self):
        n = appuifw.query(u'Enter name :','text')
        self.co.write(u'dir('+n+u')')
        self.eval_cmd()

    def dircns(self):
        self.co.write(u'dir()')
        self.eval_cmd()

    def symbol__(self):
        self.co.write(u'__')

    def symbolpar(self):
        self.co.write(u'()')

    def symbolbra(self):
        self.co.write(u'[]')

    def symbolaco(self):
        self.co.write(u'{}')

    def symbolquotes(self):
        self.co.write(u'\'\'')

    def import_s(self):
        n = appuifw.query(u'Enter name :','text')
        self.co.write(u'import '+n)
        self.eval_cmd()

    def popismod(self):
        n = appuifw.query(u'Enter module :','text')
        if self.is_module(eval(n)):
           appuifw.note(u'Module !','conf')
        else:    
           appuifw.note(u'not a module !','conf')

    def popt9(self):
        n = str(appuifw.query(u'Enter exact :','text'))
        appuifw.note(u''+n+u' : '+n.translate(self.t9),'conf')

    def curword(self):
       txt = appuifw.app.body.get()
       cpos = appuifw.app.body.get_pos()
       w = self.getword(txt,cpos)
       if w:     
        appuifw.note(u'Word :'+w,'conf')

    def ret_curword(self):
       txt = appuifw.app.body.get()
       cpos = appuifw.app.body.get_pos()
       w = self.getword(txt,cpos)
       if w:
         r=w
       else:   
         r=u''
       # appuifw.note(u'Word :'+r+u':','conf')
       return r

    def import_all(self):
        n = appuifw.query(u'Enter name :','text')
        self.co.write(u'from '+n+u' import *')
        self.eval_cmd()

    def clear_history(self):
        self.history = []
        self.history_item = -1
        self.reset_ps()



    def clear_screen(self):
        self.co.clear()
        self.co.input_wait_lock.signal()

    def goto_screen(self):
        pass

    def previous_input(self):
        if self.history_item == -1:
            return
        elif self.history_item == 4:
            self.line_beg = self.co.control.len()
        else:
            self.co.control.delete(self.line_beg,
                                   self.line_beg+\
                                   len(self.history[self.history_item]))
        self.co.control.set_pos(self.line_beg)
        self.co.write(self.history[self.history_item])
        self.history_item -= 1

    def get_run_by(self):
       self.run_by = appuifw.app.full_name()
       if self.run_by[-10:] == u'Python.app':
        self.run_by_mode = u'Python Interpreter'
       elif self.run_by[-10:] == u'appmgr.app':
        self.run_by_mode = u'Python Installer'
       else: 
        self.run_by_mode = u'Unknown ...'

    def about(self):
       appuifw.note(u'aiCON alpha 5'+u'\n'+u'Nokia license 2005'+u'\nby Nokia & cyke64','info')

    def set_exit_if_standalone(self):
       if self.run_by_mode == u'Python Installer':
          appuifw.app.set_exit()

    def fquit(self):
       pass
       
    def quit(self):
       appuifw.app.exit_key_handler = self.old_exit_key_handler
       self.set_exit_if_standalone()

    def orgquit(self):
       appuifw.app.exit_key_handler = None
       self.script_lock.signal()

    def interactive_loop(self, scope = locals()):
        import code
        appuifw.app.menu = [(u"History ...", self.pophistory),(u"Clear Screen ...", self.clear_screen),(u'About aiCON !',self.about),(u"Quit Console", self.quit)]
        old_title = appuifw.app.title
        old_menu = appuifw.app.menu
        appuifw.app.title = self.app_name+self.app_ver
        appuifw.app.exit_key_handler = self.fquit
        
        self.get_run_by()
        self.co.clear()
        code.interact(None, self.readfunc, scope)
        self.co.control.bind(EKeyDevice3, None)
        self.history = []
        self.co.clear()
        appuifw.app.menu = old_menu
        appuifw.app.title = old_title 

if __name__ == '__main__':
    try:
        console = my_console
    except NameError:
        import series60_console
        console = series60_console.Console()
    appuifw.app.body = console.control
    Py_console(console).interactive_loop()

