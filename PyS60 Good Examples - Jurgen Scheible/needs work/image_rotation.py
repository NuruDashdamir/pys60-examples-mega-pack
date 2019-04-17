import camera
from graphics import *
from appuifw import *
import e32
import key_codes
import time

def exit_key_callback():
    global running
    running=0
    lock.signal()

def getphoto_callback():
    global photo
    photo=camera.take_photo(size=(160,120))
    lock.signal()

def rotate_left_callback():
    global photo
    photo=photo.transpose(ROTATE_90)
    lock.signal()

def rotate_right_callback():
    global photo
    photo=photo.transpose(ROTATE_270)
    lock.signal()

def load_callback():
    global photo
    photo=Image.open('e:\\photo.jpg')
    lock.signal()

def save_callback():
    photo.text((0,60),unicode(time.asctime()),fill=0xffff00)
    photo.save('e:\\photo.jpg')
    lock.signal()

def refresh(rect):
    c.clear(0)
    c.blit(photo)
    c.text((10,10),u'Select to take picture', fill=0xffffff) 
    c.text((10,20),u'Left/Right to rotate', fill=0xffffff) 
    c.text((10,30),u'Down to save', fill=0xffffff) 
    c.text((10,40),u'Up to load', fill=0xffffff)

photo=Image.new((160,120))
photo.clear(0)
c=Canvas(redraw_callback=refresh)
app.body=c
app.exit_key_handler=exit_key_callback
c.bind(key_codes.EKeySelect, getphoto_callback)
c.bind(key_codes.EKeyLeftArrow, rotate_left_callback)
c.bind(key_codes.EKeyRightArrow, rotate_right_callback)
c.bind(key_codes.EKeyDownArrow, save_callback)
c.bind(key_codes.EKeyUpArrow, load_callback)
running=1
lock=e32.Ao_lock()

while running:
    refresh(())
    lock.wait()
