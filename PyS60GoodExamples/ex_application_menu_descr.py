# this script lets you create a simple application menu

# NOTE:
# press the options key in order to open the applicaion menu
# when running the script!

# imort appuifw and the e32 modules
import appuifw
import e32

# define an exit handler
def exit_key_handler():
    app_lock.signal()
 

# create the "callback functions" for the application menu 
def item1():
    appuifw.note(u"Foo", "info")

def item2():
    appuifw.note(u"Outch", "info")


# create an active object
app_lock = e32.Ao_lock()

# create the application menu include the selectable options (one, two)
# and the related callback functions (item1, item2) 
appuifw.app.menu = [(u"one", item1),
                    (u"two", item2)]


appuifw.app.exit_key_handler = exit_key_handler

# start a scheduler
app_lock.wait()
