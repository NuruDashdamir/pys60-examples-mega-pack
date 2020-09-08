import e32
from appuifw import *
from key_codes import *
import appuifw
appuifw.app.screen = 'full' 
class Keyboard(object):
    def __init__(self):
        self.state = {}  # is this key pressing ?
        self.buffer= {}  # is it waiting to be processed ?
    def handle_event(self, event): # for event_callback
        code = event['scancode']
        if event['type'] == EEventKeyDown:
            self.buffer[code]= 1   # put into queue
            self.state[code] = 1
        elif event['type'] == EEventKeyUp:
            self.state[code] = 0
    def pressing(self, code):      # just check
        return self.state.get(code,0)
    def pressed(self, code):       # check and process the event
        if self.buffer.get(code,0):
            self.buffer[code] = 0  # take out of queue
            return 1
        return 0
 
key = Keyboard()
app.body = canvas = Canvas(event_callback=key.handle_event)
 
def quit():
    global running
    running = 0
 
app.exit_key_handler = quit
running = 1
 
#
# Calling polygon may be faster than a blit.
#
 
x,y = 20,20
arrow = [(0,0), (0,10), (2,8), (4,12), (6,11), (4,7), (7,7)]
 
while running:
    if key.pressing(EScancodeUpArrow):
        y -= 1
    if key.pressing(EScancodeDownArrow):
        y += 1
    if key.pressing(EScancodeLeftArrow):
        x -= 1
    if key.pressing(EScancodeRightArrow):
        x += 1
    if key.pressed(EScancodeSelect):
        r = 1
        while key.pressing(EScancodeSelect):
            r += 1       # bigger red circle
            canvas.ellipse([(x-r,y-r),(x+r,y+r)], fill=0xff0000)
            canvas.polygon([(x+dx,y+dy) for dx,dy in arrow], 0, 0xffffff)
            e32.ao_sleep(0.03)
 
    canvas.clear(0)
    canvas.polygon([(x+dx,y+dy) for dx,dy in arrow], 0, 0xffffff)
    e32.ao_sleep(0.01)