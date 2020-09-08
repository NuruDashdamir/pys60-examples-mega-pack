
import appuifw, e32

def quit():
    print "Exit key pressed!"
    app_lock.signal()

appuifw.app.exit_key_handler = quit
appuifw.app.title = u"First App!"

appuifw.note(u"Application is now running")

app_lock = e32.Ao_lock()
app_lock.wait()
print "Application exits"
