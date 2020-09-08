
# use of keys
# use button Arrow up,down,lefet,right, 1 and * to trigger pop-up note

import appuifw
from appuifw import *
import e32
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



def quit():
    global running
    running=0


running=1

appuifw.app.screen='full'

canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=None)
appuifw.app.body=canvas

app.exit_key_handler=quit




while running:

    if keyboard.pressed(EScancodeLeftArrow):
        appuifw.note(u"Arrow left", "info")

    if keyboard.pressed(EScancodeRightArrow):
        appuifw.note(u"Arrow right", "info")


    if keyboard.pressed(EScancodeDownArrow):
        appuifw.note(u"Arrow down", "info")


    if keyboard.pressed(EScancodeUpArrow):
        appuifw.note(u"Arrow up", "info")
        
    if keyboard.pressed(EScancodeSelect):
        appuifw.note(u"Select", "info")

    if keyboard.pressed(EScancode1):
        appuifw.note(u"1", "info")
    
    if keyboard.pressed(EScancodeStar):
        appuifw.note(u"*", "info")
        
    e32.ao_yield()
    



        


 



