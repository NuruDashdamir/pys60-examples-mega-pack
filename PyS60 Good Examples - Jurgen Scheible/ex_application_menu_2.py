# this script lets you create a simple application menu

# NOTE:
# press the options key in order to open the applicaion menu
# when running the script!


import appuifw, e32, messaging


def item1():
    appuifw.note(u"Foo", "info")

def item2():
    appuifw.note(u"Outch", "info")

def item3():
    nbr1 = "3456" # add here a propper mobile number
    txt = u"Greetings from Heaven"
    messaging.sms_send(nbr1, txt)
    appuifw.note(u"Message sent", "info")
    
def quit():
    app_lock.signal()

appuifw.app.menu = [(u"one", item1),
                    (u"two", item2),
                    (u"send message", item3)]

appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()