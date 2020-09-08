
import appuifw, e32, key_codes 

def up():
    appuifw.note(u"Arrow up was pressed")
    
def two():
    appuifw.note(u"Key 2 was pressed")   

def quit():
    app_lock.signal()

canvas = appuifw.Canvas()
appuifw.app.body = canvas

canvas.bind(key_codes.EKeyUpArrow, up)
canvas.bind(key_codes.EKey2, two)

appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()
