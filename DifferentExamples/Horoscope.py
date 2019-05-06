#Name:		Horoscope
#Version:	1.1
#Idea:		Freekill
#Authors:	Gazetdinov _ALBERT_
#email:		tarlovka@rambler.ru
import os,e32,appuifw,socket

def ru(text):
	return text.decode('utf-8')
def ur(text):
	return text.encode('utf-8')

class data:
	list=[ru('Овен'),
		ru('Телец'),
		ru('Близнецы'),
		ru('Рак'),
		ru('Львы'),
		ru('Дева'),
		ru('Весы'),
		ru('Скорпион'),
		ru('Стрельцы'),
		ru('Козерог'),
		ru('Водолей'),
		ru('Рыбы')]
	stack=[]
data=data()

def forward():
	data.stack.append((appuifw.app.menu,appuifw.app.exit_key_handler,appuifw.app.body))
def backward():
	appuifw.app.menu,appuifw.app.exit_key_handler,appuifw.app.body=data.stack.pop()

def check():
	current=appuifw.app.body.current()
	if not appuifw.query(ru('Выбран ')+data.list[current]+ru('. Соединится с интернетом?'),'query'):
		return
	forward()
	appuifw.app.menu=[(ru('Отмена'),backward)]
	appuifw.app.exit_key_handler=backward
	appuifw.app.body=appuifw.Text()
	try:
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		appuifw.app.body.add(ru('Соединение с сервером...\n'))
		sock.connect((u'wap.horo.mail.ru',80))
		appuifw.app.body.add(ru('Отправка запроса...\n'))
		sock.send('GET /prediction.html?sign='+str(current+1)+'&time=1 HTTP/1.0\r\nHost: wap.horo.mail.ru\r\nRange: bytes=0-\r\nAccept-Encoding: *//*\r\nUser-agent: Python 1.4\r\n\r\n')
		appuifw.app.body.add(ru('Получение информации...\n'))
		page=''
		while 1:
			load=sock.recv(8192)
			if not load:
				break
			else:
				page+=load
		sock.close()
	except:
		appuifw.note('Невозможно получить информацию из интернета. Попробуйте еще раз.','error')
		backward()
		return
	appuifw.app.body.set(ru('	'+page[page.find('\n<div class="inner f7">\n')+28:page.find('\n</p>\n\n</div>\n')].replace('&ndash;','-').replace('\n</p>\n<p>\n',' ')))
	appuifw.app.body.set_pos(0)
	appuifw.app.body.set_pos(200)

def about():
	forward()
	appuifw.app.menu=[(ru('Назад'),backward)]
	appuifw.app.exit_key_handler=backward
	appuifw.app.body=appuifw.Text(ru('Имя:\n	Horoscope\nВерсия:\n	1.1\nИдея:\n	Freekill\nАвтор:\n	Газетдинов _ALBERT_\nemail:\n	tarlovka@rambler.ru'))

def exit():
	if appuifw.query(ru('Выйти из программы?'),'query'):
		os.abort()

appuifw.app.menu=[(ru('Гороскоп'),check),(ru('О программе'),about),(ru('Выйти'),exit)]
appuifw.app.exit_key_handler=exit
appuifw.app.body=appuifw.Listbox(data.list,check)

if appuifw.app.full_name().find(u'Python')!=-1:
	appuifw.app.title=u'Goroskop'
	lock=e32.Ao_lock()
	os.abort=lock.signal
	lock.wait()