
import appuifw, graphics, e32, key_codes

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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

def key_is_down(code):
        if key_down and key_down == (code, "down"):
                return True
        return False

def quit():
        global running
        running = False

def handle_redraw(rect):
        if img: canvas.blit(img)

img = None
canvas = appuifw.Canvas(event_callback=handle_event,
        redraw_callback=handle_redraw)
appuifw.app.screen = 'full'
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit

x = y = 100
w, h = canvas.size
img = graphics.Image.new((w, h))
img.clear(WHITE)

running = True
while running:
    if key_is_down(key_codes.EKeyLeftArrow): x -= 5
    elif key_is_down(key_codes.EKeyRightArrow): x += 5
    elif key_is_down(key_codes.EKeyDownArrow): y += 5
    elif key_is_down(key_codes.EKeyUpArrow): y -= 5
    
    #img.clear(WHITE)
    img.point((x, y), outline = BLACK, width = 50)
    handle_redraw(None)
    e32.ao_yield()
