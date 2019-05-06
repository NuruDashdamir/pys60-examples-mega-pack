import appuifw
import e32
from graphics import *

def ru(x):
  return x.decode('utf-8')

def ur(x):
  return x.encode('utf-8')

app_lock=e32.Ao_lock()

def exit_key_handler():
    app_lock.signal()

global i
i=0

img=Image.new((176,208))
appuifw.app.body=k=appuifw.Canvas()
def menu():
  k.clear(0x3f3f3f)
  appuifw.app.screen='large'
  k.text((60,30),ru('Меню'),0x888888,font=u'albi17b')
  k.text((47,50),ru('Справка'),0x888888,font=u'albi17b')
  k.text((53,70),ru('Выход'),0x888888,font=u'albi17b')


def klet():
  global i
  k.rectangle((40,15+i,117,32+i),0x555555)

def down():
  global i
  if i<40:
      i+=20
      k.clear()
      menu()
  else:pass
  klet()
k.bind(63498,down)

def up():
  global i
  if i>10:
      i-=20
      k.clear()
      menu()
  else:pass
  klet()
k.bind(63497,up)

menu()
k.rectangle((40,15,117,32),0x555555)

appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()
