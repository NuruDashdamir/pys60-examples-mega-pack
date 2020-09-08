# Camera application

# use Select key to take a photo
# press left soft key to restart the camera


from appuifw import *
from graphics import *
import camera
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


running=1
switch = 1
appuifw.app.screen='full'
img=Image.new((176,208))


def quit():
    global running
    running=0
    appuifw.app.set_exit()


def handle_redraw(rect):
    canvas.blit(img)


canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=handle_redraw)
appuifw.app.body=canvas

app.exit_key_handler=quit

screen_picture = camera.take_photo(size = (160,120))



while running:

    if switch == 1:
        screen_picture = camera.take_photo(size = (160,120))

    img.blit(screen_picture,target=(8,10,168,130),scale=1)

    handle_redraw(())
    e32.ao_yield()

    if keyboard.pressed(EScancodeLeftSoftkey):
        switch = 1
    
    if keyboard.pressed(EScancodeSelect):
        switch = 2
        e32.ao_yield()
        image = camera.take_photo(size = (640,480))
        filename=u'c:\\picture.jpg'
        image.save(filename)
        screen_picture =Image.open(u'c:\\picture.jpg')
        e32.ao_yield()



        


 



