# use keyboard keys Arrow up,down,lefet,right, 1 and * to trigger pop-up note

import appuifw
import e32
from key_codes import *

# you can use this class as a chunk as it is.
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

# set and instance of Keyboard (so you can use all the functions of
# that class later in the script by typing e.g. keyboard.pressed...)
keyboard=Keyboard()

# define the function that lets the application quit
def quit():
    global running
    running=0
    appuifw.app.set_exit()

running=1

appuifw.app.screen='normal'

# use the appuifw.Canvas function and as "event_callback" put "
# keyboard.handle_event", a function which does the keyboard scan
canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=None)

# set the application body to canvas
appuifw.app.body=canvas

appuifw.app.exit_key_handler=quit

# create a loop which the script runs all the time through to check whether a
# key has been pressed.
while running:
    # check if the left arrow key has been pressed
    if keyboard.pressed(EScancodeLeftArrow):
        appuifw.note(u"Arrow left", "info")
    # check if the right arrow key has been pressed
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
    



        


 



