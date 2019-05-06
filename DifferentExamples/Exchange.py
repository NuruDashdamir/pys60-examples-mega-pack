#Exchange_v1.30 by Газетдинов Альберт

import os,e32,sys,appuifw

RU=lambda text:text.decode('utf-8')

INF=lambda mess:appuifw.note(RU(mess),"info",1)
ERR=lambda mess:appuifw.note(RU(mess),"error",1)

class sets:
	PATH=sys.argv[0][0]+':\\system\\apps\\Exchange\\'
	def __init__(self):
		self.path=self.PATH+'settings.dat'
		self.keys=[]
		try:
			for line in open(self.path,'rb').read().split('\n'):
				key,value=line.split('=')
				setattr(self,key,eval(value))
				self.keys.append(key)
		except:
			ERR('Ошибка при загрузки настроек')
			os.abort()
	def save(self):
		open(self.path,'wb').write('\n'.join([key+'='+repr(getattr(self,key)) for key in self.keys]))
sets=sets()

def location(name):
	appuifw.Content_handler().open(sets.PATH+name)

def screen(menu=[],body=None,stack=[]):
	if menu and body:
		stack.append((appuifw.app.menu,appuifw.app.exit_key_handler,appuifw.app.body))
		appuifw.app.menu,appuifw.app.exit_key_handler,appuifw.app.body=menu,menu[-1][1],body
	else:
		appuifw.app.menu,appuifw.app.exit_key_handler,appuifw.app.body=stack.pop()

class error:
	flag=0
	def write(self,text):
		if self.flag:
			appuifw.app.body.add(RU(text))
		else:
			self.flag=1
			mess='Произошла ошибка в программе Exchange v1.30'
			ERR(mess)
			screen([
				(RU('Выйти'),os.abort)],
				appuifw.Text(RU(mess)+u'.\n'))
			appuifw.app.body.color=(255,0,0)
sys.stderr=error()

sets.NAMES=(
	RU('Российский рубль'),
	RU('Доллар США'),
	RU('ЕВРО'),
	RU('Украинская гривна'),
	RU('Белорусский рубль'),
	RU('Казахская тенге'),
	RU('Австрал-ий доллар'),
	RU('Канадский доллар'),
	RU('Швейцарский франк'),
	RU('Датская крона'),
	RU('Фунт стерлинга'),
	RU('Исландская крона'),
	RU('Японская иена'),
	RU('Норвежская крона'),
	RU('Cингап-ий доллар'),
	RU('Туретская лира'),
	RU('Cпец. права заимст.'))

sets.SENDS=(
	"RUR",
	"USD",
	"EUR",
	"UAH",
	"BLR",
	"KZT",
	"AUD",
	"CAD",
	"CHF",
	"DKK",
	"GBP",
	"ISK",
	"JPY",
	"NOK",
	"SGD",
	"TRL",
	"XDR")

sets.MULTS=(
	1.0,
	1.0,
	1.0,
	10.0,
	100.0,
	100.0,
	1.0,
	1.0,
	1.0,
	10.0,
	1.0,
	100.0,
	100.0,
	10.0,
	1.0,
	1000000.0,
	1.0)

def trans(arg1,arg2):
	import socket
	try:
		number=appuifw.query(RU('Сумма:'),"float")/sets.MULTS[arg1]
	except:
		return
	try:
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((u"wap.rbc.ru",80))
		sock.send("GET /cgi-bin/conver/conver.cgi?summa="+str(number)+"&kom=0&step=3&group=1&from="+sets.SENDS[arg1]+"&to="+sets.SENDS[arg2]+" HTTP/1.0\r\nHost: wap.rbc.ru\r\nRange: bytes=0-\r\nAccept-Encoding: *//*\r\nUser-agent: Python 1.4\r\n\r\n")
		page=RU('')
		while 1:
			load=sock.recv(8192)
			if not load:
				break
			page+=load
		sock.close()
	except:
		return ERR("Невозможно загрузить информацию. Попробуйте еще раз.")
	try:
		temp=page.find("&#1048;&#1090;&#1086;&#1075;&#1086;")
		appuifw.query(RU('Итого:'),"float",float(page[temp+37:page.find("<br/>",temp)])*sets.MULTS[arg2])
	except:
		return ERR("Сервер не поддерживает данное направление перевода валют.")

def newlist():
	result=[]
	sets.TRANS.sort()
	for index in range(len(sets.NAMES)):
		if index in sets.TRANS:
			temp="+ "
		else:
			temp="- "
		result.append(temp+sets.NAMES[index])
	return result

def check():
	index=appuifw.app.body.current()
	try:
		sets.TRANS.remove(index)
	except:
		sets.TRANS.append(index)
	appuifw.app.body.set_list(newlist(),index)

def start():
	menu=[]
	for index1 in sets.TRANS:
		temp=()
		for index2 in sets.TRANS:
			if index1!=index2:
				temp=temp+((sets.NAMES[index2],eval("lambda:trans("+str(index1)+","+str(index2)+")")),)
		menu.append((sets.NAMES[index1],temp))
	appuifw.app.menu=menu+appuifw.app.menu[-3:]

screen([
	(RU('Настройки'),lambda:screen([
		(RU('Изменить'),check),
		(RU('Назад'),lambda:sets.save() or screen() or start())],
		appuifw.Listbox(newlist(),check))),
	(RU('О программе'),lambda:screen([
		(RU('www.mobi.ru'),lambda:location('wwwmobi.html')),
		(RU('wap.mobimag.ru'),lambda:location('wapmobi.html')),
		(RU('Назад'),screen)],
		appuifw.Text(RU('Название:\n	Exchange v1.30\nРазработчики:\n	Газетдинов Альберт\nКоординаты:\n	www.mobi.ru\n	wap.mobimag.ru\n	tarlovka@rambler.ru')))),
	(RU('Выйти'),lambda:appuifw.query(RU('Выйти из программы?'),'query') and os.abort())],
	appuifw.Text(RU('	Программа конвертирует суммы в рублях и иностранной валюте между собой по курсу Центробанка России, используя интернет-сервис сайта wap.rbc.ru')))

start()

if appuifw.app.full_name().lower().find(u'python')!=-1:
	appuifw.app.title=u'Exchange'
	lock=e32.Ao_lock()
	os.abort=lock.signal
	lock.wait()