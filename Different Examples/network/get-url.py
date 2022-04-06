import urllib
import appuifw
import e32
import socket

appuifw.app.body = text = appuifw.Text()
appuifw.app.body.color = 255
appuifw.app.title = u'Enter URL'

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


appuifw.app.menu = [
 (u'Ok', ok),
 (u'Clear', clear),
 (u'Access Point', access)
 ]

def exit():
    appuifw.app.set_exit()


lock = e32.Ao_lock()
appuifw.app.exit_key_handler = exit
lock.wait()

