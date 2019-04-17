import e32
import appuifw
import camera
import key_codes

def viewfinder_cb(img):
    appuifw.app.body.blit(img)

def capture_cb():
    global photo
    photo=camera.take_photo()
    camera.stop_finder()
    lock.signal()

old_body=appuifw.app.body
appuifw.app.body=appuifw.Canvas()
lock=e32.Ao_lock()
photo=None
camera.start_finder(viewfinder_cb)
appuifw.app.body.bind(key_codes.EKeySelect, capture_cb)
lock.wait()
appuifw.app.body=old_body

filename=u'c:\\photo.jpg'
photo.save(filename)
print "Photo taken and saved at:",filename
