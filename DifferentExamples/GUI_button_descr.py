# Copyright (c) 2005 Jurgen Scheible

# use keyboard key Select to press the graphical button

import appuifw
import e32
from key_codes import *

# import all functions from the graphics module
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

# basically we use 2 images: a background image showing the button unpressed and a foreground imgage showing the button as pressed
# open the background image and assign it to a vaiable im_back
im_back =Image.open('e:\\gui_background.jpg')
# open the foreground image and assign it to a vaiable im_front
im_front =Image.open('e:\\gui_foreground.jpg')

running=1

appuifw.app.screen='full'

# create the canvas
canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=None)
appuifw.app.body=canvas

appuifw.app.exit_key_handler=quit


while running:
    # if the select key is hold down then show the front image (assign the front image to photo")
    if keyboard.is_down(EScancodeSelect):
        photo = im_front
    else:
        # otherwise show the background image (assign the front image to photo")
        photo = im_back
    # redraw the photo (the button picture)
    canvas.blit(photo)

    # Wait for something to happen
    e32.ao_yield()
    



        


 



