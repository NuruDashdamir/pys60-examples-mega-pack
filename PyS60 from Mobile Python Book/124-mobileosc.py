import appuifw, e32, graphics, key_codes, socket, OSCmobile

sound = 0
y_pos_contr = 100

slidershaft = graphics.Image.open("e:\\background.jpg")

makeMaskTemp = graphics.Image.open('e:\\controller_mask.jpg')
makeMaskTemp.save("e:\\controller_mask.png", bpp=1)
contrMask = graphics.Image.new(size = (97,149),mode = '1')
contrMask.load("e:\\controller_mask.png")
contr = graphics.Image.open("e:\\controller.jpg")

makeMaskTemp = graphics.Image.open('e:\\button_mask.jpg')
makeMaskTemp.save("e:\\button_mask.png", bpp=1)
buttnMask = graphics.Image.new(size = (111,78),mode = '1')
buttnMask.load("e:\\button_mask.png")
buttnOn = graphics.Image.open("e:\\button_red.jpg")
buttnOff = graphics.Image.open("e:\\button_dark.jpg")

def keys(event):
    global y_pos_contr, sound		
    if event['keycode'] == key_codes.EKeyDownArrow:
        if y_pos_contr < 260 :
            y_pos_contr = y_pos_contr + 5
            sending(str(3))

    if event['keycode'] == key_codes.EKeyUpArrow:
        if y_pos_contr > 0 :
            y_pos_contr = y_pos_contr - 5
            sending(str(4))

    if event['keycode'] == key_codes.EKeySelect:
        if sound == 1:
            sound = 0
        else:
            sound = 1
        sending(str(5))

    handle_redraw(())

def handle_redraw(rect):
    global sound, img, w,h
    img.blit(slidershaft, target = (0,0,w,h))
    img.blit(contr, target=(142,y_pos_contr), mask=contrMask)
    if sound == 1:
        img.blit(buttnOn, target=(8,328), mask=buttnMask)
    else:
        img.blit(buttnOff, target=(8,328), mask=buttnMask)
    canvas.blit(img, target = (0,0,w,h), scale = 1 )

def choose_service(services):
    names = []
    channels = []
    for name, channel in services.items():
        names.append(name)
        channels.append(channel)
    index = appuifw.popup_menu(names, u"Choose service")
    return channels[index]

def connect():
    global sock
    address, services = socket.bt_discover()
    channel = choose_service(services)
    sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
    sock.connect((address, channel))
    
def sending(data):
    global sock
    message = OSCmobile.OSCMessage()
    message.setAddress("/phone/user1")
    message.append(data)
    sock.send(message.getBinary())

def quit():
    app_lock.signal()

canvas=appuifw.Canvas(event_callback=keys,redraw_callback=handle_redraw)
appuifw.app.body=canvas
appuifw.app.screen='full'
w, h = canvas.size
img = graphics.Image.new((w,h))
appuifw.app.exit_key_handler=quit
handle_redraw(())
connect()
app_lock = e32.Ao_lock()
app_lock.wait()