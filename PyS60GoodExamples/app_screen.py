import appuifw
import e32

def exit_key_handler():
    app_lock.signal()


round = appuifw.Text()
round.set(u'hello')

# put the application screen size to full screen
appuifw.app.screen='full' #(a full screen)

# other options:
#appuifw.app.screen='normal' #(a normal screen with title pane and softkeys)
#appuifw.app.screen='large' #(only softkeys visible)



app_lock = e32.Ao_lock()

appuifw.app.body = round

appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()