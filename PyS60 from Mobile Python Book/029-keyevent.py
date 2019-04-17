
import appuifw, key_codes, e32

def keys(event):
    if event['keycode'] == key_codes.EKeyUpArrow:
        appuifw.note(u"Arrow up was pressed")
    elif event['keycode'] == key_codes.EKey2:
        appuifw.note(u"Key 2 was pressed")

def quit():
    app_lock.signal()

canvas = appuifw.Canvas(event_callback = keys)
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()
