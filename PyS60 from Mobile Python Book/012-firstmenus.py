
import appuifw, e32

def photo():
    appuifw.note(u"Cheese!")

def darken():
    appuifw.note(u"I can't see a thing!")

def lighten():
    appuifw.note(u"My eyes are burning!")

def quit():
    print "WANNABE PHOTOEDITOR EXITS"
    app_lock.signal()

appuifw.app.exit_key_handler = quit
appuifw.app.title = u"PhotoEditor"
appuifw.app.menu = [(u"Take Photo", photo), (u"Edit photo",
    ((u"Darken", darken), (u"Lighten", lighten)))]

print "WANNABE PHOTOEDITOR STARTED"
app_lock = e32.Ao_lock()
app_lock.wait()
