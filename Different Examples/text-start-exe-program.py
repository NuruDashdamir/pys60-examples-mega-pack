# calling a native symbian app from within script 

import appuifw
import e32

def startApp():
    try:
        # start_exe(filename, command [,wait ])
        # this starts the "Calendar" app on your phone
        e32.start_exe("z:\\sys\\bin\\Calendar.exe", "")
    except:
        appuifw.note(u"Something went wrong", "error")


def exit_key_handler():
    script_lock.signal()
    appuifw.app.set_exit()
    
script_lock = e32.Ao_lock()

appuifw.app.title = u"App Start Test"
appuifw.app.menu = [(u"Start Some App", startApp)]
appuifw.app.exit_key_handler = exit_key_handler

script_lock.wait()


 

