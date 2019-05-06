# Copyright (c) 2005 Jurgen Scheible

# use keyboard key Select to press the graphical button

import appuifw
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

im_back =Image.open('e:\\gui_background.jpg')
im_front =Image.open('e:\\gui_foreground.jpg')

running=1

appuifw.app.screen='full'

canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=None)
appuifw.app.body=canvas

appuifw.app.exit_key_handler=quit


while running:        
    if keyboard.is_down(EScancodeSelect):
        photo = im_front
    else:
        photo = im_back
    canvas.blit(photo)

    # Wait for something to happen
    e32.ao_yield()
    



        


 



