
import camera, appuifw, e32

def viewfinder(img):
        img.point((100, 100), outline = (255, 0, 0), width = 10)
        canvas.blit(img)

def quit():
        camera.stop_finder()
        lock.signal()

appuifw.app.body = canvas = appuifw.Canvas()
appuifw.app.exit_key_handler = quit

camera.start_finder(viewfinder)
lock = e32.Ao_lock()
lock.wait()

