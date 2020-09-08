
import camera, e32, socket, appuifw

PHOTO = u"e:\\Images\\bt_photo_send.jpg"

def send_photo():
    try:
            address, services = socket.bt_obex_discover()
    except:
            appuifw.note(u"OBEX Push not available", "error")
            return
        
    if u'OBEX Object Push' in services:
            channel = services[u'OBEX Object Push']
            socket.bt_obex_send_file(address, channel, PHOTO)
            appuifw.note(u"photo sent", "info")
    else:
            appuifw.note(u"OBEX Push not available", "error")

def take_photo():
    photo = camera.take_photo()
    canvas.blit(photo, scale = 1)
    photo.save(PHOTO)

def quit():
    app_lock.signal()

canvas = appuifw.Canvas()
appuifw.app.body = canvas
appuifw.app.exit_key_handler = quit
appuifw.app.title = u"BT photo send"
appuifw.app.menu = [(u"Take photo", take_photo),
                    (u"Send photo", send_photo)]
app_lock = e32.Ao_lock()
app_lock.wait()
