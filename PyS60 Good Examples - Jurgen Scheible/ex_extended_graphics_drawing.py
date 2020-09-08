
# use button Arrow up,down,left,right, to move the colour point
# Use button 6 to change the colour of the point to yellow (0xffff00) and button 5 to change it back.
# Use button 9 to change the colour of the background to pink (0xff00ff) and button 8 to change it back.
# Use button 4 to shrink the colour point and button 7 to increase its size.

import appuifw
from appuifw import *
import e32
from key_codes import *
from graphics import *


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



def quit():
    global running
    running=0
    appuifw.app.set_exit()


appuifw.app.screen='full'
img=Image.new((176,208))
blobsize=30
location_x = 100.
location_y = 100.
point_colour=0xff0000
background_colour = 0x0000ff

def handle_redraw(rect):
    canvas.blit(img)

running=1

canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=handle_redraw)
appuifw.app.body=canvas

app.exit_key_handler=quit

while running:

    img.clear(background_colour)
    img.point((location_x + blobsize/2,location_y + blobsize/2),point_colour,width=blobsize)

    handle_redraw(())

    if keyboard.is_down(EScancodeLeftArrow):
        location_x = location_x - 1

    if keyboard.is_down(EScancodeRightArrow):
        location_x = location_x + 1


    if keyboard.is_down(EScancodeDownArrow):
        location_y = location_y + 1


    if keyboard.is_down(EScancodeUpArrow):
        location_y = location_y - 1
        
    if keyboard.pressed(EScancode4):
        blobsize = blobsize - 4
        
    if keyboard.pressed(EScancode7):
        blobsize = blobsize + 4
        
    if keyboard.pressed(EScancode6):
        point_colour=0xffff00

        
    if keyboard.pressed(EScancode9):
        background_colour = 0xff00ff
        
    if keyboard.pressed(EScancode5):
        point_colour=0xff0000

        
    if keyboard.pressed(EScancode8):
        background_colour = 0x0000ff


    e32.ao_yield()





        


 



