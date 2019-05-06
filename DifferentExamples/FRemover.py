#FRemover VER 0.7
#Gavrishev Alexandr (anod)
#mailto: alex.gavrishev@gmail.com
#SYMBIANUID=0x10201520
#
# -*- coding: utf-8 -*-

import os,appuifw,e32,string,codecs

hmain = None
class Fremover:
	def __init__(self):
		self.script_lock = e32.Ao_lock()
		self.entries = []
		self.errlog=u'c:\\frm.log'
		scriptshell_dir = os.path.split(appuifw.app.full_name())[0]
		self.cfg = scriptshell_dir+os.sep+u'cfg.lst'
		if e32.in_emulator():	self.cfg = u'c:\\cfg.lst'
		self.rm	= os.path.join(scriptshell_dir,u'readme.txt')
		self.cindx = 0
		self.lb = None
		self.q = None
		self.get_list()
		if len(self.entries)<=0:
			self.entries.append((u'Please, add items...',u''))
		self.lb = appuifw.Listbox(self.entries, self.lbox_observe)
		#EKeyBackspace = 0x0008
		self.lb.bind(0x0008,lambda:self.del_item())
		self.refresh()
		self.script_lock.wait()
	def refresh(self):
		appuifw.app.title = u'FRemover v0.7'
		lmenu=(u'List',((u'Browse for items',lambda:self.browse_item()),(u'Add item',lambda:self.add_item()),(u'Edit item',lambda:self.edit_item()),(u'Delete item (c)',lambda:self.del_item())))
		abouts=u'FRemover v0.7\n   by anod\nalex.gavrishev@gmail.com'
		hmenu=(u'Help',((u'ReadMe',lambda:self.readme()),(u'About...',lambda:appuifw.query(abouts,'query'))))
		appuifw.app.menu = [(u'Remove file',lambda:self.del_file()),(u'View Log',lambda:self.view_log()),lmenu,hmenu]
		appuifw.app.exit_key_handler = self.exit_key_handler
		appuifw.app.body = self.lb
		if not e32.in_emulator():	self.script_lock.signal()
	def save_list(self):
		F=codecs.open(self.cfg,'w','utf-8')
		for name,path in self.entries:
			F.write(name+'|'+path+'\n')
		F.close()
		if (self.lb!=None):
			self.lb.set_list(self.entries, 0)
	def get_list(self):
		if os.path.exists(self.cfg)==1:
			F=codecs.open(self.cfg,'r','utf-8')
			while 1:
				line=F.readline()
				if line=='':
					break
				line=line[:-1]
				[name,path]=string.split(line,'|')
				self.entries.append((unicode(name),unicode(path)))
			F.close()
		else:
			self.entries=[]
			self.entries.append((u'MSearch',u'e:\\system\\apps\\mobilesearch\\msearch.cfg'))
			self.entries.append((u'Netfront 3.2',u'c:\\system\\shareddata\\101fed88.ini'))
			self.entries.append((u'N-Gage Libs',u'e:\\system\\libs\\::ecom.dll;ecomserver.exe;http.dll;httptcphnd.dll;inetprotutil.dll;loaderclings.dll;loadersrvngs.exe;ncuibrowser.dll;ncuiutil.dll;ncuibrowserngs.dll;rbinterpreterngs.dll;securesocket.dll;ssl70.dll;ssladaptor.dll'))
			self.entries.append((u'_PAlbTN',u'search_for::_PAlbTN'))
			self.entries.append((u'ProfiMail',u'c:\\system\\data\\audiofmt.bix;c:\\system\\data\\gsm_sell.inf;c:\\system\\data\\multihome.dat;c:\\system\\data\\Trackftp.idx;c:\\system\\system.ini;c:\\system\\shareddata\\101f76a7.ini'))
			self.entries.append((u'Proviewer',u'c:\\system\\data\\cbsq.isf;c:\\system\\data\\cbsq.dat;c:\\system\\libs\\0010343.tas;e:\\system\\data\\0010343.tas'))
			self.entries.append((u'stIcq',u'C:\\System\\Data\\bt00010217.dat;c:\\stICQlog.txt'))
			self.entries.append((u'Trm',u'e:\\trm\\'))
			self.save_list()
	def browse_item(self):
		self.FileBrowser = Filebrowser(self)
		self.FileBrowser.run()
	def view_log(self):
		if os.path.exists(self.errlog)==1:
			self.q = TextField(self,'log')
			self.q.run()
		else:
			appuifw.note(u'Log '+self.errlog+u' file not found')
	def add_br_items(self,path):
		name = None
		name=appuifw.query(u'Name','text',u'')
		if (name!=None):
			if (unicode(self.entries[0][0]) == unicode('Please, add items...')):
				del self.entries[0]
				if len(self.entries)<=0:
					self.entries=[]
			path = unicode(path,encoding='utf-8', errors='replace')
			self.entries.append((name,path))
			self.save_list()
	def add_item(self):
		self.q = TextField(self,'add_item')
		self.q.run()
	def readme(self):
		if os.path.exists(self.rm)==1:
			self.q = TextField(self,'readme')
			self.q.run()
		else:
			appuifw.note(u'ReadMe file not found')	
	def edit_item(self):
		self.cindx=self.lb.current()
		if (unicode(self.entries[self.cindx][0]) != unicode('Please, add items...')):
			self.q = TextField(self,'edit_item')
			self.q.run()
	def del_item(self):
		self.cindx=self.lb.current()
		if appuifw.query(u'Do you want to delete this entry?','query'):
			del self.entries[self.cindx]
			if len(self.entries)<=0:
				self.entries.append((u'Please, add items...',u''))
			self.save_list()
	def print_exception_trace(self): 
		import sys, traceback 
		logfile=codecs.open(self.errlog,'a','utf-8') 
		try: 
			type, value, tb = sys.exc_info() 
			sys.last_type = type 
			sys.last_value = value 
			sys.last_traceback = tb 
			tblist = traceback.extract_tb(tb) 
			del tblist[:1] 
			list = traceback.format_list(tblist) 
			if list: 
				list.insert(0, u"Traceback (most recent call last):\n") 
			list[len(list):] = traceback.format_exception_only(type, value) 
			list.append(u"----------------\n")
		finally: 
			tblist = tb = None 
		map(logfile.write, list) 
		logfile.close() 
	def del_file(self):
		def del_files(list,dir=u''):
			fnames=string.split(list,';')
			err_count=0
			for fname in fnames:
				fname = fname.encode('utf-8')
				if os.path.isdir(fname)and(dir==''):
					err_count+=del_folder(fname)
				else:
					try:
						if dir==u'':
							os.remove(fname)
						else:
							dir=dir.encode('utf-8')
							os.remove(os.path.join(str(dir),fname))
					except:
						err_count+=1
						self.print_exception_trace()
			if err_count==0:
				appuifw.note(u'Items was deleted')
			else:
				appuifw.note(u'Failed! See log...:-)');
		def del_folder(path):
			err_count=0
			for file in os.listdir(str(path)):
				new_path=os.path.join(str(path), file)
				if os.path.isdir(new_path):
					del_folder(new_path)
				else:
					os.remove(new_path)
			if os.path.isdir(path):
				try:
					os.rmdir(path)
				except:
					self.print_exception_trace()
					err_count+=1
			return err_count
		def search_for(path,sname,c):
			counter = c
			for file in os.listdir(str(path)):
				new_path=os.path.join(str(path), file)
				if string.lower(file) == sname:
					counter +=1
					appuifw.note(u'Deleting... '+unicode(new_path))
					if os.path.isdir(new_path):
						del_folder(new_path)
					else:
						try:
							os.remove(new_path)
						except:
							self.print_exception_trace()
							appuifw.note('Failed! See log...:-)');
				if os.path.isdir(new_path):
					counter = search_for(new_path,sname,counter)
			return counter
		if (unicode(self.entries[self.cindx][0]) != unicode('Please, add items...')):
			if string.find(self.entries[self.cindx][1], '::') < 0:
				search=u''
			else:
				search,fname = string.split(self.entries[self.cindx][1],'::',1)
			if unicode(search) != u'':
				if search == u'search_for':
					if appuifw.query(u'Do you want to search and delete files?','query'):
						c=0
						fnames=string.split(fname,';')
						for fname in fnames:
							appuifw.note(u'Searching for...\n['+unicode(fname)+u']')
							fname = fname.encode('utf-8')
							c=search_for('c:\\',string.lower(fname),c)
							c=search_for('e:\\',string.lower(fname),c)
							e32.ao_yield()
						if c==0:
							appuifw.note(u'Files or Folders not found...')
						else:
							appuifw.note(unicode(c)+u' Files or Folders was deleted...')
				else:
					if os.path.isdir(search):
						if appuifw.query(u'Do you want to remove this folders/files?','query'):
							del_files(fname,search)
					else:
						appuifw.note(u"Folder not found...")
			else:
				if appuifw.query(u'Do you want to remove this folders/files?','query'):
					del_files(self.entries[self.cindx][1])
	def exit_key_handler(self):
		appuifw.app.exit_key_handler = None
		self.script_lock.signal()
		appuifw.app.set_exit()
	def lbox_observe(self):        
		self.cindx=self.lb.current()
		self.del_file()
		self.lb.set_list(self.entries, 0)
class TextField:
	def __init__(self, hmain,act):
		self.hmain = hmain
		self.t = appuifw.Text()
		self.log = self.hmain.errlog.encode('utf-8')
		self.cindx = 0
		self.act=act
		self.name=u''
		self.data = u''
		self.log = self.hmain.errlog.encode('utf-8')
	def run(self):
		if self.act==u'add_item':
			appuifw.app.menu = [(u'Enter',lambda:self.add_item()),(u'Cancel',lambda:self.exit_key_handler())]
			appuifw.app.title = u"Enter Path:"
			self.name=appuifw.query(u'Name','text',u'')
		if self.act==u'edit_item':
			appuifw.app.menu = [(u'Enter',lambda:self.edit_item()),(u'Cancel',lambda:self.exit_key_handler())]
			appuifw.app.title = u"Edit Path:"
			self.cindx=self.hmain.lb.current()
			name=self.hmain.entries[self.cindx][0]
			self.name=appuifw.query(u'Name','text',name)
			self.data=self.hmain.entries[self.cindx][1]
		if self.act==u'readme':
			appuifw.app.menu = [(u'Close',lambda:self.exit_key_handler())]
			appuifw.app.title = u"Read Me:"
			try:
				F=codecs.open(self.hmain.rm,'r','utf-8')
				self.data=F.read()
			finally:
				F.close()
			self.name=u'ok'
		if self.act==u'log':
			appuifw.app.menu = [(u'Del Log',lambda:self.del_log()),(u'Close',lambda:self.exit_key_handler())]
			appuifw.app.title = u"View Log"
			try:
				F=codecs.open(self.log,'r','utf-8')
				self.data=F.read()
			finally:
				F.close()
			self.name=u'ok'			
		if self.name:
			self.refresh()
		else:
			self.exit_key_handler()
	def add_item(self):
		if (self.name!=None):
			data = unicode(self.t.get())
			if data!=u'':
				if (unicode(self.hmain.entries[0][0]) == unicode('Please, add items...')):
					del self.hmain.entries[0]
					if len(self.hmain.entries)<=0:
						self.hmain.entries=[]  
				self.hmain.entries.append((self.name,data))
				self.hmain.save_list()
		self.exit_key_handler()
	def edit_item(self):
		if (self.name!=None):
			data = unicode(self.t.get())
			if data!=u'':
				self.cindx = self.hmain.lb.current()
				self.hmain.entries[self.cindx]=(self.name,data)
				self.hmain.save_list()
		self.exit_key_handler()
	def refresh(self):
		appuifw.app.exit_key_handler = self.exit_key_handler
		appuifw.app.body = self.t
		self.t.clear()
		self.t.set(self.data)		
		self.t.set_pos(0)
	def del_log(self):
		try:
			os.remove(self.log)
			appuifw.note(u'Log was deleted')
		except:
			appuifw.note(u'Cannot delete log')
		self.exit_key_handler()
	def exit_key_handler(self):
		self.hmain.refresh()
class Filebrowser:
	def __init__(self, hmain):
		self.hmain = hmain
		self.entries = []
		self.dirlist = []
	def run(self):
		self.get_dirs()
		self.lb = appuifw.Listbox(self.entries, self.lbox_observe)
		self.refresh()
	def refresh(self):
		appuifw.app.title = u"Choose Folder"
		appuifw.app.menu = [(u'Open Folder',lambda:self.lbox_observe()),(u'Select Files In Folder',lambda:self.select_folder()),(u'Add Folder To List',lambda:self.add_folder()),(u'Exit',lambda:self.exit_key_handler())]
		appuifw.app.exit_key_handler = self.exit_key_handler
		appuifw.app.body = self.lb
	def get_dirs(self):
		if len(self.dirlist) == 0:
			self.entries = [u'C:',u'E:']#e32.drive_list()
			self.dirlist = []
		else:
			self.entries = []
			cpath = string.join(self.dirlist,os.sep)+os.sep
			cpath = cpath.encode('utf-8')
			for file in os.listdir(str(cpath)):
				full_name = os.path.join(str(cpath), file)
				if os.path.isdir(full_name):
					self.entries.append(unicode(file,encoding='utf-8', errors='replace'))
			self.entries.insert(0, u'..')
	def add_folder(self):
		cidx=self.lb.current()
		cfile=self.entries[cidx]
		if (cfile != '..'):
			if len(self.dirlist) == 0:
				cpath = unicode(cfile+os.sep)
			else:
				cpath = unicode(string.join(self.dirlist,os.sep)+os.sep+cfile+os.sep)
			cpath = cpath.encode('utf-8')
			q=appuifw.query(u"You want to add this folder??" , 'query')
			if q:
				self.hmain.add_br_items(cpath)
			self.exit_key_handler()
	def select_folder(self):
		cidx=self.lb.current()
		cfile=self.entries[cidx]
		if (cfile != '..'):
			if len(self.dirlist) == 0:
				cpath = unicode(cfile+os.sep)
			else:
				cpath = unicode(string.join(self.dirlist,os.sep)+os.sep+cfile+os.sep)
			cpath = cpath.encode('utf-8')
			files_arr = []
			for file in os.listdir(str(cpath)):
				full_name = os.path.join(str(cpath), file)
				if not os.path.isdir(full_name):
					files_arr.append(unicode(file,encoding='utf-8', errors='replace'))
			if (len(files_arr) > 0):
				selection = appuifw.multi_selection_list(files_arr, style='checkbox', search_field=0)
				if selection:
					sel_files = []
					new_items = u''
					sel_files = [files_arr[i] for i in selection]
					cpath = unicode(cpath,encoding='utf-8', errors='replace')
					new_items=cpath+'::'
					for file in sel_files:
						new_items += file + ';'
					new_items = new_items[:-1].encode('utf-8')
					self.hmain.add_br_items(new_items)
					self.exit_key_handler()
				else:
					appuifw.note(u'You not selected items')
	def exit_key_handler(self):
		self.hmain.refresh()
	def lbox_observe(self):
		cidx=self.lb.current()
		cfile=unicode(self.entries[cidx])
		if (cfile == u'..'):
			if (len(self.dirlist)-1 > 0):
				self.dirlist=self.dirlist[:-1]
			else:
				self.dirlist=[]
		else:
				self.dirlist.append(cfile)
		self.get_dirs()
		self.lb.set_list(self.entries, 0)

if __name__ == '__main__':
	hmain = Fremover()

