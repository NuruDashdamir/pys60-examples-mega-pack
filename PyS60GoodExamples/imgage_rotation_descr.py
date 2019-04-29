import camera
# import from graphics all functions
from graphics import *
# import all functions of appuifw -> means we can leave the "appuifw" away when calling its funtions
# because they are known now by this script by their name (namespace issue)
# so instead of using appuifw.app.body = ... we can do now use app.body = ...
from appuifw import *
import e32
import key_codes
import time

def exit_key_callback():
    global running
    running=0
    lock.signal()

# get a photo in using the camera function
def getphoto_callback():
    global photo
    photo=camera.take_photo(size=(160,120))
    # release the active object scheduler
    lock.signal()

# rotatate the photo and set "photo" newly
def rotate_left_callback():
    global photo
    photo=photo.transpose(ROTATE_90)
    # release the active object scheduler
    lock.signal()
    
# rotatate the photo and set "photo" newly
def rotate_right_callback():
    global photo
    photo=photo.transpose(ROTATE_270)
    # release the active object scheduler
    lock.signal()
    
# reopen the photo and set "photo" newly (afer the timecode has been printed on the photo)
def load_callback():
    global photo
    photo=Image.open('e:\\photo.jpg')
    # release the active object scheduler
    lock.signal()

# label the photo with the time and date
def save_callback():
    photo.text((0,60),unicode(time.asctime()),fill=0xffff00)
    # save the photo with the time imprinted
    photo.save('e:\\photo.jpg')
    # release the active object scheduler
    lock.signal()

def refresh(rect):
    # clear screen to black
    c.clear(0)
    # draw the photo there
    c.blit(photo)
    # print some explanatory white text
    c.text((10,10),u'Select to take picture', fill=0xffffff) 
    c.text((10,20),u'Left/Right to rotate', fill=0xffffff) 
    c.text((10,30),u'Down to save', fill=0xffffff) 
    c.text((10,40),u'Up to load', fill=0xffffff) 

# create an initial image and store it to photo
photo=Image.new((160,120))
# clear the photo to black
photo.clear(0)

# create the canvas
c=Canvas(redraw_callback=refresh)
app.body=c
app.exit_key_handler=exit_key_callback

# bind certain keys to certain callback functions
c.bind(key_codes.EKeySelect, getphoto_callback)
c.bind(key_codes.EKeyLeftArrow, rotate_left_callback)
c.bind(key_codes.EKeyRightArrow, rotate_right_callback)
c.bind(key_codes.EKeyDownArrow, save_callback)
c.bind(key_codes.EKeyUpArrow, load_callback)

running=1
# create an active object
lock=e32.Ao_lock()
while running:
    # draw the screen again and again
    refresh(())
    # Wait for something to happen (start a scheduler)
    lock.wait()

