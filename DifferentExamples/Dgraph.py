
import appuifw, e32, key_codes, graphics

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

def draw_rectangle():
    img.rectangle((50,100,100,150), fill = YELLOW)

def draw_point():
    img.point((90,50), outline = RED, width = 30)

def draw_text():
    img.text((10,40), u'Hello', fill = WHITE)

def handle_redraw(rect):
    if img: canvas.blit(img)

def handle_event(event):
    ev = event['keycode']        
    if event['type'] == appuifw.EEventKeyDown: 
        img.clear(BLUE)

    if ev == key_codes.EKeyUpArrow:
        draw_point()
    elif ev == key_codes.EKeyRightArrow:
        draw_text()
    elif ev == key_codes.EKeyDownArrow:
        draw_rectangle()
    elif ev == key_codes.EKeyLeftArrow:
        draw_point()
        draw_text()
        draw_rectangle()
    handle_redraw(None)

def quit():
    app_lock.signal()

img = None
canvas = appuifw.Canvas(\
                  redraw_callback = handle_redraw,\
                  event_callback = handle_event)

appuifw.app.body = canvas
appuifw.app.screen = 'full'
appuifw.app.exit_key_handler = quit

w, h = canvas.size
img = graphics.Image.new((w, h))
img.clear(BLUE)

app_lock = e32.Ao_lock()
app_lock.wait()
