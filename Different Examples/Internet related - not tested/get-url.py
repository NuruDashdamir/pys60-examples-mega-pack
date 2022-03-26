import urllib
import appuifw
import e32
import socket

def ru(x):
    return x.decode('utf-8')


appuifw.app.body = text = appuifw.Text()
appuifw.app.body.color = 255
appuifw.app.title = ru('\xd0\x92\xd0\xb2\xd0\xb5\xd0\xb4\xd0\xb8\xd1\x82\xd0\xb5 URL')

def ok():
    try:
        file = open('e:\\system\\apps\\geturl\\set.ini', 'r')
        poin = file.read()
        file.close()
        socket.set_default_access_point(socket.access_point(int(poin)))
    except:
        pass
    url = text.get()
    urln = urllib.urlopen(url)
    ur = urln.geturl()
    text.set(ru(ur))



def clear():
    text.set('')



def access():
    point = socket.select_access_point()
    set = open('e:\\system\\apps\\geturl\\set.ini', 'w')
    set.write(str(point))
    set.close()


appuifw.app.menu = [(u'Ok',
  ok),
 (ru('\xd0\x9e\xd1\x87\xd0\xb8\xd1\x81\xd1\x82\xd0\xb8\xd1\x82\xd1\x8c'),
  clear),
 (ru('\xd0\xa2\xd0\xbe\xd1\x87\xd0\xba\xd0\xb0 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb0'),
  access)]

def exit():
    appuifw.app.set_exit()


lock = e32.Ao_lock()
appuifw.app.exit_key_handler = exit
lock.wait()

