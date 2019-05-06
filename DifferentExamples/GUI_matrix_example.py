from appuifw import *
from graphics import *
import e32
from key_codes import *
import socket

class Keyboard(object):    def __init__(self,onevent=lambda:None):        self._keyboard_state={}        self._downs={}        self._onevent=onevent    def handle_event(self,event):        if event['type'] == appuifw.EEventKeyDown:            code=event['scancode']            if not self.is_down(code):                self._downs[code]=self._downs.get(code,0)+1            self._keyboard_state[code]=1        elif event['type'] == appuifw.EEventKeyUp:            self._keyboard_state[event['scancode']]=0        self._onevent()
    def is_down(self,scancode):        return self._keyboard_state.get(scancode,0)
    def pressed(self,scancode):        if self._downs.get(scancode,0):            self._downs[scancode]-=1            return True        return False
keyboard=Keyboard()

running=1switch = 1
appuifw.app.screen='full'img=Image.new((176,208))
p1 = 0s1 = 0p2 = 0s2 = 0p3 = 0s3 = 0p4 = 0s4 = 0p5 = 0s5 = 0
debug = u"hello"

background = Image.open(u'e:\\Images\White.jpg')on = Image.open(u'e:\\Images\Black.jpg')
blobsize = 10location_x = 80location_y = 100
def quit():    global running    running=0    appuifw.app.set_exit()
def handle_redraw(rect):    canvas.blit(img)
sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
# target=('00:0c:84:00:06:70',1)
if not target:    address,services=socket.bt_discover()    print "Discovered: %s, %s"%(address,services)    if len(services)>1:        import appuifw        choices=services.keys()        choices.sort()        choice=appuifw.popup_menu([unicode(services[x])+": "+x                                   for x in choices],u'Choose port:')        target=(address,services[choices[choice]])    else:        target=(address,services.values()[0])
print "Connecting to "+str(target)
sock.connect(target)
canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=handle_redraw)
appuifw.app.body=canvas

app.exit_key_handler=quit


######################################################

def mousein_stat(x,y):
    global debug
    #Col 1, Row 1
    l = pos_check(x, y, 26, 51, 17, 42, 1, 1)
    debug = u"list " + str(l)
    if not l=="":
        send_cmd(l)


def pos_check(location_x, location_y, x1, x2, y1, y2, col, row):
    global debug
    global p1
    global s1
    debug = u"pos"
    l = ""
    if location_x > x1:
        debug = u"x1"
        if location_x < x2:
            debug = u"x2"
            if location_y > y1:
                debug = u"y1"
                if location_y < y2:
                    debug = u"y2"
                    if keyboard.pressed(EScancodeSelect):
                        if s1 == 1:
                            p1 = 0
                            s1 = 0
                            l = range(3)
                            l[0] = col
                            l[1] = row
                            l[2] = 0
                            debug = u"1"
                        else:
                            p1 = 1
                            l = range(3)
                            l[0] = col
                            l[1] = row
                            l[2] = 1
                            debug = u"2"
    return l

def send_cmd(list):
    cnt=0
    test = u""
    running = 1
    while running:
        test = test + str(list[cnt])
        cnt = cnt + 1
        if cnt == 3:
            running = 0
    test = test + u"\r"
    sock.send(test)

######################################################


while running:      img.blit(background,target=(0,0,176,208),scale=1)
# row 1
    
    mousein_stat(location_x,location_y)

#    if location_x > 26:
#        if location_x < 51:
#            if location_y > 17:
#                if location_y < 42:
#                    if keyboard.pressed(EScancodeSelect):
#                        if s1 == 1:
#                            p1 = 0
#                            s1 = 0
#                            test = u"110/r"
#                            sock.send(test)
#                        else:
#                            p1 = 1
#                            test = u"111/r"
#                            sock.send(test)
    if location_x > 51:
        if location_x < 76:
            if location_y > 17:
                if location_y < 42:
                    if keyboard.pressed(EScancodeSelect):
                        if s2 == 1:
                            p2 = 0
                            s2 = 0
                            test = u"210/r"
                            sock.send(test)
                        else:
                            p2 = 1
                            test = u"211/r"
                            sock.send(test)

    if location_x > 76:
        if location_x < 101:
            if location_y > 17:
                if location_y < 42:
                    if keyboard.pressed(EScancodeSelect):
                        if s3 == 1:
                            p3 = 0
                            s3 = 0
                            test = u"310/r"
                            sock.send(test)
                        else:
                            p3 = 1
                            test = u"311/r"
                            sock.send(test)

    if location_x > 101:
        if location_x < 126:
            if location_y > 17:
                if location_y < 42:
                    if keyboard.pressed(EScancodeSelect):
                        if s4 == 1:
                            p4 = 0
                            s4 = 0
                            test = u"410/r"
                            sock.send(test)
                        else:
                            p4 = 1
                            test = u"411/r"
                            sock.send(test)

    if location_x > 126:
        if location_x < 151:
            if location_y > 17:
                if location_y < 42:
                    if keyboard.pressed(EScancodeSelect):
                        if s5 == 1:
                            p5 = 0
                            s5 = 0
                            test = u"510/r"
                            sock.send(test)
                        else:
                            p5 = 1
                            test = u"511/r"
                            sock.send(test)



    if p1 == 1:
        img.blit(on,target=(26,17,51,42),scale=1)
        s1=1

    if p2 == 1:
        img.blit(on,target=(51,17,76,42),scale=1)
        s2=1

    if p3 == 1:
        img.blit(on,target=(76,17,101,42),scale=1)
        s3=1

    if p4 == 1:
        img.blit(on,target=(101,17,126,42),scale=1)
        s4=1

    if p5 == 1:
        img.blit(on,target=(126,17,151,42),scale=1)
        s5=1



# row 2

    img.blit(on,target=(26,42,51,67),scale=1)


    img.blit(on,target=(51,42,76,67),scale=1)


    img.blit(on,target=(76,42,101,67),scale=1)


    img.blit(on,target=(101,42,126,67),scale=1)


    img.blit(on,target=(126,42,151,67),scale=1)



# row 3

    img.blit(on,target=(26,67,51,92),scale=1)


    img.blit(on,target=(51,67,76,92),scale=1)


    img.blit(on,target=(76,67,101,92),scale=1)


    img.blit(on,target=(101,67,126,92),scale=1)


    img.blit(on,target=(126,67,151,92),scale=1)



# row 4

    img.blit(on,target=(26,92,51,117),scale=1)


    img.blit(on,target=(51,92,76,117),scale=1)


    img.blit(on,target=(76,92,101,117),scale=1)


    img.blit(on,target=(101,92,126,117),scale=1)


    img.blit(on,target=(126,92,151,117),scale=1)



# row 5

    img.blit(on,target=(26,117,51,142),scale=1)


    img.blit(on,target=(51,117,76,142),scale=1)


    img.blit(on,target=(76,117,101,142),scale=1)


    img.blit(on,target=(101,117,126,142),scale=1)


    img.blit(on,target=(126,117,151,142),scale=1)



# row 6

    img.blit(on,target=(26,142,51,167),scale=1)


    img.blit(on,target=(51,142,76,167),scale=1)


    img.blit(on,target=(76,142,101,167),scale=1)


    img.blit(on,target=(101,142,126,167),scale=1)


    img.blit(on,target=(126,142,151,167),scale=1)



# row 7

    img.blit(on,target=(26,167,51,192),scale=1)


    img.blit(on,target=(51,167,76,192),scale=1)


    img.blit(on,target=(76,167,101,192),scale=1)


    img.blit(on,target=(101,167,126,192),scale=1)


    img.blit(on,target=(126,167,151,192),scale=1)




    img.point((location_x, location_y),0xff0000,width=blobsize)
    img.text((0,14), debug,0xffffff)

    handle_redraw(())
    e32.ao_yield()

    
        
    if keyboard.is_down(EScancodeLeftArrow):
        location_x = location_x - 2

    if keyboard.is_down(EScancodeRightArrow):
        location_x = location_x + 2

    if keyboard.is_down(EScancodeDownArrow):
        location_y = location_y + 2


    if keyboard.is_down(EScancodeUpArrow):
        location_y = location_y - 2
        
        

    e32.ao_yield()









































































































