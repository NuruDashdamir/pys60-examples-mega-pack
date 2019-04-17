
import e32, camera, appuifw, key_codes

def viewfinder(img):
    canvas.blit(img)

def shoot():
    camera.stop_finder()
    photo = camera.take_photo(size = (640, 480))
    w, h = canvas.size
    canvas.blit(photo, target = (0, 0, w, 0.75 * w), scale = 1)
    photo.save('D:\\photo.jpg')

def quit():
    camera.stop_finder()
    app_lock.signal()

appuifw.app.body = canvas = appuifw.Canvas()
appuifw.app.title = u"Camera"
appuifw.app.exit_key_handler = quit

camera.start_finder(viewfinder)
canvas.bind(key_codes.EKeySelect, shoot)

app_lock = e32.Ao_lock()
app_lock.wait()
