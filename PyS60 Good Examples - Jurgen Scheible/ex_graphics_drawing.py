# Graphics drawing
# use button Arrow up,down,left,right, to move the colour point

import appuifw, graphics, e32
from key_codes import *


class Keyboard(object):
    def __init__(self,onevent=lambda:None):
        self._keyboard_state={}
        self._downs={}
        self._onevent=onevent
    def handle_event(self,event):
        if event['type'] == appuifw.EEventKeyDown:
            code=event['scancode']
            if not self.is_down(code):
                self._downs[code]=self._downs.get(code,0)+1
            self._keyboard_state[code]=1
        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']]=0
        self._onevent()
    def is_down(self,scancode):
        return self._keyboard_state.get(scancode,0)
    def pressed(self,scancode):
        if self._downs.get(scancode,0):
            self._downs[scancode]-=1
            return True
        return False

keyboard=Keyboard()

blobsize=30
location_x = 100
location_y = 100
BLUE=0x0000ff
RED=0xff0000
running=1

def handle_redraw(rect):
    canvas.blit(img)

def quit():
    global running
    running=0


canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=handle_redraw)
appuifw.app.body=canvas

appuifw.app.screen='full'
w,h = canvas.size
img=graphics.Image.new((w,h))

appuifw.app.exit_key_handler=quit

while running:

    img.clear(BLUE)
    img.point((location_x,location_y),RED,width=blobsize)

    handle_redraw(())
    e32.ao_yield()

    if keyboard.is_down(EScancodeLeftArrow):
        location_x = location_x - 1

    if keyboard.is_down(EScancodeRightArrow):
        location_x = location_x + 1


    if keyboard.is_down(EScancodeDownArrow):
        location_y = location_y + 1


    if keyboard.is_down(EScancodeUpArrow):
        location_y = location_y - 1







        


 



