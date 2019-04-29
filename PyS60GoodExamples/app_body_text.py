import appuifw
import e32

def exit_key_handler():
    app_lock.signal()

# create an instance of appuifw.Text()
round = appuifw.Text()
# change the style of the text
round.style = appuifw.STYLE_UNDERLINE
# set the text to 'hello'
round.set(u'hello')

# put the screen size to full screen
appuifw.app.screen='full' 

# create an Active Object
app_lock = e32.Ao_lock()

# set the application body to Text
# by handing over "round" which is an instance of appuifw.Text() as definded above
appuifw.app.body = round

appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()