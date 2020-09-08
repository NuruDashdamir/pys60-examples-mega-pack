
import appuifw, e32, key_codes

key_down = None
clicked = None

def handle_event(event):
    global clicked, key_down
    if event['type'] == appuifw.EEventKey:
            if key_down:
                    key_down = (event['keycode'], "down")
            else:
                    key_down = (event['keycode'], "pressed")
    elif event['type'] == appuifw.EEventKeyUp and key_down:
            code, mode = key_down
            if mode == "pressed":
                    clicked = code
            key_down = None

def key_clicked(code):
        global clicked
        if code == clicked:
                clicked = None
                return True
        return False

def key_is_down(code):
        if key_down and key_down == (code, "down"):
                return True
        return False

def quit():
        global running
        running = False

canvas = appuifw.Canvas(event_callback=handle_event)
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit

running = True
while running:
    e32.ao_sleep(0.1)

    if key_clicked(key_codes.EKeyUpArrow):
            appuifw.note(u"Arrow up was pressed")
    elif key_is_down(key_codes.EKey2):
            canvas.clear((0, 0, 255))
    else:
            canvas.clear((255, 255, 255))
