import appuifw
import e32

def exit_key_handler():
    app_lock.signal()
 

# create the callback functions for the application menu and its submenus
def item1():
    print ""
    round.set(u'item one was selected')

def subitem1():
    print ""
    round.set(u'subitem one was selected')

def subitem2():
    round.set(u'subitem two was selected')


app_lock = e32.Ao_lock()
round = appuifw.Text()
round.set(u'press options')
appuifw.app.screen='large'
appuifw.app.body = round

# create the application menu including submenus
appuifw.app.menu = [(u"item 1", item1),
                    (u"Submenu 1", ((u"sub item 1", subitem1),
                                    (u"sub item 2", subitem2)))]


appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()