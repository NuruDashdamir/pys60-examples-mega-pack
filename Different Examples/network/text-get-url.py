import urllib
import appuifw
import e32

text = appuifw.Text()
text.set(u'http://httpforever.com')
appuifw.app.body = text
appuifw.app.body.color = 255
appuifw.app.title = u'Enter URL'

def ok():
    url_address = text.get()
    html_content = urllib.urlopen(url_address).read()
    text.set(unicode(html_content))

def clear():
    text.set(u'')

appuifw.app.menu = [
 (u'Ok', ok),
 (u'Clear', clear),
]

def exit():
    appuifw.app.set_exit()

lock = e32.Ao_lock()
appuifw.app.exit_key_handler = exit
lock.wait()

