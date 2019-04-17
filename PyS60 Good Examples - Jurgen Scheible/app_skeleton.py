# application skeleton (no main loop)
# it is recommended to use "print" statements only for debugging purposes


# 1. import all modules needed
import appuifw
import e32


# 2. set the screen size to large
appuifw.app.screen='large'


# 3. create your application logic ...
# e.g. create all your definitions (functions) or classes and build instances of them or call them etc.
# ...... application logic ....
application_body = appuifw.Text()


# 4. create the application menu including submenus
# create the callback functions for the application menu and its submenus
def item1():
    #print "hello"
    appuifw.note(unicode("hello"))

def subitem1():
    #print "aha"
    appuifw.note(unicode("aha"))

def subitem2():
    #print "good"
    appuifw.note(unicode("good"))

appuifw.app.menu = [(u"item 1", item1),
                    (u"Submenu 1", ((u"sub item 1", subitem1),
                                    (u"sub item 2", subitem2)))]    


# 5. create and set an exit key handler
def exit_key_handler():
    app_lock.signal()


# 6. set the application title
appuifw.app.title = u"drawing"    
 
 
# 7. crate an active object
app_lock = e32.Ao_lock()


# 8. set the application body 
appuifw.app.body = application_body

# 9. set exit key handler (right softkey) and application lock (so app won't exit)
appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()