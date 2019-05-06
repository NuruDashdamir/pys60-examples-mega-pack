#SYMBIANUID=0x00201525
import appuifw,urlparse,urllib,e32,httplib,codecs,string,sys,os
from socket import *
import thread

class GetFile:
	def __init__(self,hmain):
		self.hmain=hmain
		self.of=None
		self.http=None
		self.url=u''
		self.fname=u''
		self.dir=hmain.dfldr
		self.ph=hmain.proxy_host
		self.pp=hmain.proxy_port
		self.proxy_sock=None
		self.fsize=0
		self.loaded=0
	def start_conn(self):
		self.url=self.hmain.entries[0][1]
		self.fname=self.hmain.entries[0][0]
		urlparts = urlparse.urlsplit(self.url)
		netloc = urlparts[1].split(':') 
		host = netloc[0] 
		port = 80
		if len(netloc) > 1: 
			port = int(netloc[1]) 
#		apid = socket.select_access_point()
#		appuifw.note(unicode(apid))
#		apo=socket.access_point(apid)
#		socket.set_default_access_point(apo)
		if self.ph!=u'':
			s=u'Proxy: '+unicode(self.ph)+u':'+unicode(self.pp)
			self.put_status(s)
			self.proxy_sock=socket(AF_INET, SOCK_STREAM)
			self.proxy_sock.connect((self.ph, self.pp))
		s=u'Connecting to: '+unicode(host)+u':'+unicode(port)
		self.put_status(s)
		self.http = httplib.HTTPConnection(host, port)
		if self.proxy_sock:
			self.http.sock=self.proxy_sock
		self.http.putrequest('GET', self.url)
		self.http.putheader('Accept', '*/*')
		self.http.putheader('User-Agent', 'PyGet/0.1')
		self.http.putheader('Host', host)
		file=unicode(os.path.join(self.dir,self.fname))
		existSize = 0
		if os.path.exists(file):
			if appuifw.query(u'File exist...\n Ok - Continue\n Cancel - Restart','query'):
				self.of = open(file,'ab') 
				existSize = os.path.getsize(file)
			else:
				self.of = open(file,'wb')
		else:
			self.of = open(file,'wb') 
		if existSize > 0:
			self.http.putheader('Range', 'bytes=%d-' % (existSize, ))
		self.http.endheaders()
		self.hmain.running = 1
		self.get_file()
	def put_status(self,str):
		self.hmain.entries[0]=(self.hmain.entries[0][0],self.hmain.entries[0][1],str,self.hmain.entries[0][3])
		self.hmain.set_lb(self.hmain.lb.current())
	def get_filename(self,url):
		o = urlparse.urlsplit(url)
		file=os.path.split(o[2])[1]
		return unicode(os.path.join(self.dir,file))
	def get_file(self):
		r = self.http.getresponse()
		errcode = r.status
		errmsg = r.reason
		self.put_status(unicode(errmsg))
		self.loaded,pos,self.fsize=0,0,r.length
		done=0
		if (errcode == 200 or 206)and(self.of.tell()<self.fsize):
			if errcode == 206:
				self.fsize+=self.of.tell()
			if self.fsize/1000>0:
				self.fsize=self.fsize/1000
			try:
				while 1:
					if self.hmain.running==1:
						temp = r.read(8192)
						if temp == '':
							done=1
							break
						self.of.write(temp)
						self.loaded=self.of.tell()
						s=u'%dKb/%sKb' % (self.loaded/1000, self.fsize)
						self.put_status(s)
			finally:
				self.of.close()
				self.hmain.entries[0]=(self.hmain.entries[0][0],self.hmain.entries[0][1],self.hmain.entries[0][2],done)
				self.hmain.save_settings()
		self.close_conn()
	def close_conn(self):
		self.http.close()
		if self.proxy_sock is not None: 
			self.proxy_sock.close() 
			self.proxy_sock = None 
		if self.of:	self.of.close()
		s=u'%dKb/%sKb' % (self.loaded/1000, self.fsize)
		self.put_status(s)
		if (self.hmain.running==1):
			self.hmain.next_file()
class App:
	def __init__(self):
		self.old_title = appuifw.app.title
		self.lock = e32.Ao_lock()
		self.old_exit_key = appuifw.app.exit_key_handler
		self.entries = []
		self.conn = None
		self.running = 0
		self.cfg = 'pyget.lst'
		self.errlog='pyget.log'
		scriptshell_dir = os.path.split(appuifw.app.full_name())[0]
		if os.path.exists(scriptshell_dir)==1:
			if e32.in_emulator():
				self.cfg = os.path.join('c:',self.cfg)
				self.errlog = os.path.join('c:',self.errlog)
			else:
				self.cfg = os.path.join(scriptshell_dir,self.cfg)
				self.errlog = os.path.join(scriptshell_dir,self.errlog)
		else:
			self.cfg = os.path.join('c:',self.cfg)
			self.errlog = os.path.join('c:',self.errlog)
		self.my_log = Logger(self.errlog)
		sys.stderr = sys.stdout = self.my_log
		self.cindx = 0
		self.lb = None
		self.FileBrowser = None
		self.q = None
		self.proxy_host=u''
		self.proxy_port=0
		self.dfldr=u''
		self.delad=0
		self.get_settings()
		if len(self.entries)<=0:
			self.entries.append((u'Please, add items...',u''))
		self.lb = appuifw.Listbox([(u'',u'')], self.lbox_observe)
		self.set_lb(0)
		self.refresh()
		self.lock.wait()
	def refresh(self):
		appuifw.app.title = u'PyGet'
		menu1= (u'List',((u'Move Top',lambda:self.move_item(0)),(u'Move Up',lambda:self.move_item(1)),(u'Move Down',lambda:self.move_item(-1)),(u'Move Bottom',lambda:self.move_item(-2))))
		menu2= (u'Url' ,((u'Add Url',lambda:self.add_item()),(u'Edit Url',lambda:self.edit_item()),(u'Delete Url',lambda:self.del_item())))
		menu3= (u'Settings',((u'Proxy',lambda:self.proxy_set()),(u'Downloads Folder',lambda:self.dfldr_set()),(u'Del Url After Download',lambda:self.delad_set())))
		appuifw.app.menu = [(u'Start/Stop download',lambda:self.start()),(u'Launch file',lambda:self.launch()),menu1,menu2,menu3]
		appuifw.app.exit_key_handler = self.exit_handler
		appuifw.app.body = self.lb
	def next_file(self):
		if self.running==0:
			if int(self.entries[self.cindx][3]) == 0:
				list_item=self.entries.pop(self.cindx)
				self.entries.insert(0, list_item)
				self.set_lb(0)
				self.conn.start_conn()
			else:
				if self.cindx+1<=len(self.entries)-1:
					self.cindx += 1
					self.next_file()
	def start(self):
		self.cindx=0
		if self.running==1:
			if appuifw.query(u'Stop?','query'):
					self.running=0
					self.conn.close_conn()
		else:
			if (unicode(self.entries[self.cindx][0]) != unicode('Please, add items...')):
				self.conn=GetFile(self)
				self.next_file()
	def add_item(self):
		self.q = TextField(self,'add_url')
		self.q.run()
	def edit_item(self):
		self.cindx=self.lb.current()
		if (unicode(self.entries[self.cindx][0]) != unicode('Please, add items...')):
			self.q = TextField(self,'edit_url')
			self.q.run()
	def del_item(self):
		self.cindx=self.lb.current()
		if appuifw.query(u'Do you want to delete this entry?','query'):
			del self.entries[self.cindx]
			if len(self.entries)<=0:
				self.entries.append((u'Please, add items...',u''))
			self.save_settings()
	def move_item(self,to):
		def move(ipos,dpos):
			list_item=self.entries.pop(ipos)
			self.entries.insert(dpos, list_item)
			self.set_lb(dpos)
		self.cindx=self.lb.current()
		if (unicode(self.entries[self.cindx][0]) != unicode('Please, add items...')):
			if (to==0)and(self.cindx>0):
				if self.running==1:
					if appuifw.query(u'You want to stop current downloading?','query'):
						self.running=0
						self.conn.close_conn()
						move(self.cindx,0)
				else:
					move(self.cindx,0)
			if (to==1)and(self.cindx>0):
				if (self.cindx-1==0)and(self.running==1):
					if appuifw.query(u'You want to stop current downloading?','query'):
						self.running=0
						self.conn.close_conn()
						move(self.cindx,self.cindx-1)
				else:
					move(self.cindx,self.cindx-1)
			if (to==-1):
				if (self.cindx==0)and(self.running==1):
					if appuifw.query(u'You want to stop current downloading?','query'):
						self.running=0
						self.conn.close_conn()
						move(self.cindx,self.cindx+1)
				else:
					move(self.cindx,self.cindx+1)
			if (to==-2):
				if (self.cindx==0)and(self.running==1):
					if appuifw.query(u'You want to stop current downloading?','query'):
						self.running=0
						self.conn.close_conn()
						move(self.cindx,len(self.entries))
				else:
					move(self.cindx,len(self.entries))
			self.save_settings()
	def proxy_set(self):
		self.q = TextField(self,'edit_proxy')
		self.q.run()
	def dfldr_set(self):
		self.FileBrowser = Filebrowser(self)
		self.FileBrowser.run()
	def delad_set(self):
		if appuifw.query(u'Ok - delete after downloading\nCancel - past to end of list?','query'):
			self.delad=1
		else:
			self.delad=0
		self.save_settings()
	def launch(self):
		apprun = u'z:\\system\\programs\\apprun.exe'
		zipman = u'"E:\\System\\Apps\\Zipman\\Zipman.app" "'
		self.cindx=self.lb.current()
		if (unicode(self.entries[self.cindx][0]) != unicode('Please, add items...')):
			if int(self.entries[self.cindx][3])==1:
				path=zipman+unicode(os.path.join(self.dfldr,self.entries[self.cindx][0]))+u'"'
				try:
					appuifw.note(path)
					e32.start_exe(apprun,path)
				except:
					 self.my_log.print_exception_trace()
	def lbox_observe(self):
		self.cindx=self.lb.current()
		self.launch()
	def get_settings(self):
		if os.path.exists(self.cfg)==1:
			F=codecs.open(self.cfg,'r','utf-8')
#Read proxy value
			line=F.readline()
			line=line[:-1]
			one,two = string.split(line,'=',1)
			if (unicode(two) != u''):
				o = two.split(':') 
				self.proxy_host = o[0]
				self.proxy_port = 80
				if len(o[1]) > 0: 
					self.proxy_port = int(o[1])
			else:
				self.proxy_host = u''
				self.proxy_port = 0
#Read download folder value
			line=F.readline()
			line=line[:-1]
			one,two = string.split(line,'=',1)
			self.dfldr=unicode(two)
#Read delete after dovnload value
			line=F.readline()
			line=line[:-1]
			one,two = string.split(line,'=',1)
			self.delad=int(two)
#Read items
			while 1:
				line=F.readline()
				if line=='':
					break
				line=line[:-1]
				data = line.split('|')
				self.entries.append((unicode(data[0]),unicode(data[1]),unicode(data[2]),unicode(data[3])))
			F.close()
		else:
			self.proxy_host=u'192.118.11.56' 
			self.proxy_port=8080
			self.proxy_sock=None 
			self.dfldr=u'c:'+unicode(os.sep)
			self.delad=0
			self.entries=[]
			self.entries.append((u'iphone_by_anod.sis.zip',u'http://server3.dimonvideo.ru/uploader/temy/47321_iphone_by_anod.sis.zip',u' ',0))
			self.entries.append((u'mcdonalds_smartphone.zip',u'http://server3.dimonvideo.ru/uploader/ljubitelskoe_video/43746_mcdonalds_smartphone.zip',u' ',0))
			self.save_settings()
	def save_settings(self):
		F=codecs.open(self.cfg,'w','utf-8')
		if self.proxy_host!=u'':
			F.write(u'Proxy='+unicode(self.proxy_host)+u':'+unicode(self.proxy_port)+u'\n')
		else:
			F.write(u'Proxy=\n')
		F.write(u'Download_folder='+self.dfldr+u'\n')
		F.write(u'Del_after='+unicode(self.delad)+u'\n')
		for name,url,stat,done in self.entries:
			F.write(name+u'|'+url+u'|'+stat+u'|'+unicode(done)+u'\n')
		F.close()
		if (self.lb!=None):
			self.set_lb(self.lb.current())
	def set_lb(self,pos):
		tlist=[]
		for name,url,stat,done in self.entries:
			if int(done)==1:
				stat += u' Done.'
			tlist.append((unicode(name),unicode(stat)))
		self.lb.set_list(tlist,pos)
	def exit_handler(self):
		self.save_settings()
		appuifw.app.title = self.old_title
		appuifw.app.exit_key_handler = self.old_exit_key
		self.lock.signal()
#		appuifw.app.set_exit()
class TextField:
	def __init__(self, hmain,act):
		self.hmain = hmain
		self.dir = self.hmain.dfldr
		self.t = appuifw.Text()
		self.log = self.hmain.errlog.encode('utf-8')
		self.cindx = 0
		self.act=act
	def run(self):
		if self.act==u'add_url':
			appuifw.app.menu = [(u'Enter',lambda:self.add_url()),(u'Cancel',lambda:self.exit_key_handler())]
			appuifw.app.title = u"Enter Url:"
		if self.act==u'edit_url':
			appuifw.app.menu = [(u'Enter',lambda:self.edit_url()),(u'Cancel',lambda:self.exit_key_handler())]
			appuifw.app.title = u"Edit Url:"
			self.cindx=self.hmain.lb.current()
			url=self.hmain.entries[self.cindx][1]
			self.t.set(url)
		if self.act==u'edit_proxy':
			appuifw.app.menu = [(u'Enter',lambda:self.proxy()),(u'Cancel',lambda:self.exit_key_handler())]
			appuifw.app.title = u"Edit Proxy:\n(0.0.0.0:80)"
			self.t.set(self.hmain.proxy_host+u':'+unicode(self.hmain.proxy_port))
		self.t.set_pos(0)
		self.refresh()
	def get_filename(self,url):
		o = urlparse.urlsplit(url)
		file=os.path.split(o[2])[1]
		return unicode(file)
	def add_url(self):
		data = unicode(self.t.get())
		if data!=u'':
			if (unicode(self.hmain.entries[0][0]) == unicode('Please, add items...')):
				del self.hmain.entries[0]
				if len(self.hmain.entries)<=0:
					self.hmain.entries=[]  
			name=self.get_filename(data)
			nname = appuifw.query(u'File name','text',name)
			if nname==u'':
				nname=name
			self.hmain.entries.append((nname,data,u' ',0))
		self.exit_key_handler()
		self.hmain.save_settings()
	def edit_url(self):
		data = unicode(self.t.get())
		if data!=u'':
			name=self.get_filename(data)
			nname = appuifw.query(u'File name','text',name)
			if nname==u'':
				nname=name
			stat=self.hmain.entries[self.cindx][2]
			done=self.hmain.entries[self.cindx][3]
			self.hmain.entries[self.cindx]=(nname,data,stat,done)
		self.exit_key_handler()
		self.hmain.save_settings()
	def proxy(self):
		data = unicode(self.t.get())
		if data!=u'':
			o = data.split(':') 
			self.hmain.proxy_host = o[0]
			self.hmain.proxy_port = 80
			if len(o[1]) > 1: 
				self.hmain.proxy_port = int(o[1])
		else:
			self.hmain.proxy_host = u''
			self.hmain.proxy_port = 0
		self.exit_key_handler()
		self.hmain.save_settings()
	def refresh(self):
		appuifw.app.exit_key_handler = self.exit_key_handler
		appuifw.app.body = self.t
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
		appuifw.app.menu = [(u'Open Folder',lambda:self.lbox_observe()),(u'Select Folder',lambda:self.add_folder()),(u'Exit',lambda:self.exit_key_handler())]
		appuifw.app.exit_key_handler = self.exit_key_handler
		appuifw.app.body = self.lb
	def get_dirs(self):
		if len(self.dirlist) == 0:
			self.entries = [u'C:',u'E:']
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
		cfile=unicode(self.entries[cidx])
		if (cfile != '..'):
			if len(self.dirlist) == 0:
				cpath = unicode(os.path.join(cfile))
			else:
				cpath = string.join(self.dirlist,os.sep)+os.sep
				cpath = unicode(os.path.join(cpath,cfile))
			cpath = cpath.encode('utf-8')
			q=appuifw.query(u"You want to use this folder??" , 'query')
			if q:
				self.hmain.dfldr=cpath
				self.hmain.save_settings()
				appuifw.note(unicode(self.hmain.dfldr)+' selected...')
			self.exit_key_handler()
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
class Logger: 
	def __init__(self, log_name): 
		self.logfile = log_name 
	def write(self, obj): 
		log_file = open(self.logfile, 'a')
		log_file.write(obj) 
		log_file.close() 
	def writelines(self, obj): 
		self.write(''.join(list)) 
	def flush(self): 
		pass 
	def print_exception_trace(self): 
		import sys, traceback 
		logfile=codecs.open(self.logfile,'a','utf-8') 
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
		
if __name__ == '__main__':
	hmain = App()