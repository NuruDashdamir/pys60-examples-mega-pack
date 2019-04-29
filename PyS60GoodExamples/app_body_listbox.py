import appuifw
import e32

def exit_key_handler():
    app_lock.signal()

# define a callback function
def shout():
    index = lb.current()
    print index
    print entries[index]

# create your content list of your listbox including the icons to be used for each entry
entries = [u"Signal",u"Battery"]
lb = appuifw.Listbox(entries,shout)

# create an Active Object
app_lock = e32.Ao_lock()

# create an instance of appuifw.Listbox(), include the content list "entries" and the callback function "shout"
# and set the instance of Listbox now as the application body
appuifw.app.body = lb


appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()