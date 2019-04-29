# Camera application

# use Select key to take a photo
# press left soft key to restart the camera


from appuifw import *
from graphics import *
# import the camera module
import camera
import e32
from key_codes import *

# the keys as usual
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
# create an empty image
img=Image.new((176,208))


def quit():
    global running
    running=0
    appuifw.app.set_exit()

# define the redraw function (redraws the screen)
def handle_redraw(rect):
    canvas.blit(img)

# define the canvas including key scanning fucntion as callback and also the redraw handler as callback
canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=handle_redraw)
# set the application body to canvas
appuifw.app.body=canvas

app.exit_key_handler=quit

# take a photo in of the size 160x120 pixels
screen_picture = camera.take_photo(size = (160,120))


# create a loop to get stuff handled that needs to be done again and again
while running:
    # activate the camera again taking in pictures again and again (till key 2 is pressed)
    if switch == 1:
        screen_picture = camera.take_photo(size = (160,120))
    # draw the new picture on the canvas in the upper part -> numbers are coordinates of the location of the picture on the canvas
    img.blit(screen_picture,target=(8,10,168,130),scale=1)
    # redraw the canvas
    handle_redraw(())
    e32.ao_yield()
    # scann for left softkey to switch on the camera again
    if keyboard.pressed(EScancodeLeftSoftkey):
        switch = 1
    # scan for the Select key (navigaiton key pressed)
    # if pressed the go out of the previous loop of getting in pictures again and again
    if keyboard.pressed(EScancodeSelect):
        switch = 2
        e32.ao_yield()
        # take the main picture in with 640 x 480 pixels in size
        image = camera.take_photo(size = (640,480))
        # define a filename under which teh picture shall be saved
        filename=u'c:\\picture.jpg'
        # save the newly taken in picture
        image.save(filename)
        # set the picture that remains on the screen to the newly taken in one (to hold it)
        screen_picture =Image.open(u'c:\\picture.jpg')
        e32.ao_yield()



        


 



