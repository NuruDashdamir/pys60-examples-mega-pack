DEBUG = True
VERSION = u'1.10'
import e32
import sysinfo
import appuifw
import graphics
canvas = None
img = ima = mask = None
img0 = ima0 = None
img1 = ima1 = None
xx = yy = cx = cy = vx = vy = dx = 0
RGB_BLACK = (0,
 0,
 0)
RGB_WHITE = (255,
 255,
 255)

def cb_redraw(dummy = (0,
 0,
 0,
 0)):
    if img:
        canvas.blit(img)



def cb_view(im):
    global cy
    global cx
    global mask
    if (not cx):
        (aa, bb,) = im.size
        cx = ((vx / 2) - (aa / 2))
        cy = ((vy / 2) - (bb / 2))
        del mask
        mask = graphics.Image.new(im.size, mode='L')
        mask.clear(RGB_BLACK)
        mask.ellipse((0,
         0,
         aa,
         bb), fill=RGB_WHITE, outline=RGB_WHITE)
    ima.blit(img, target=((0,
      0),
     (vx,
      vy)), source=((dx,
      dx),
     ((vx - dx),
      (vy - dx))), scale=1)
    img.blit(ima)
    img.blit(im, target=(cx,
     cy), mask=mask)
    canvas.blit(img)



def set_camera(id):
    global vx
    global vy
    global cx
    global img
    global ima
    count = _camera.Camera(0).cameras_available()
    a = b = 0
    if (count > 1):
        camera.stop_finder()
        cx = 0
        if (id == 0):
            appuifw.app.orientation = 'landscape'
            (vx, vy,) = (xx,
             yy)
            img = img0
            ima = ima0
            a = ((3 * vx) / 4)
            b = ((3 * vy) / 4)
        elif (id == 1):
            appuifw.app.orientation = 'portrait'
            (vx, vy,) = (yy,
             xx)
            img = img1
            ima = ima1
            a = vx
            b = vy
        wait_note(u'Changing camera,', u'please wait!')
        img.clear(RGB_BLACK)
        camera._my_camera = camera._camera.Camera(id)
        camera.start_finder(cb_view, size=(a,
         b))
    else:
        appuifw.note(u'Cannot find other camera!', 'error')



def wait_note(s1, s2):
    fnt = 'title'
    ((x1, y1, x2, y2,), dummy, dummy,) = canvas.measure_text(s1, font=fnt)
    img.text((((vx / 2) - (x2 / 2)),
     (((vy / 2) - (y1 / 2)) - 20)), s1, RGB_WHITE, fnt)
    ((x1, y1, x2, y2,), dummy, dummy,) = canvas.measure_text(s2, font=fnt)
    img.text((((vx / 2) - (x2 / 2)),
     (((vy / 2) - (y1 / 2)) + 20)), s2, RGB_WHITE, fnt)
    canvas.blit(img)



def menu_about():
    appuifw.note((((u'Kameramation v' + VERSION) + u'\n') + u'jouni.miettunen.googlepages.com\n\xa92009 Jouni Miettunen'))



def cb_quit():
    camera.stop_finder()
    camera.release()
    app_lock.signal()


if (e32.pys60_version_info > (1,
 9)):
    screen = 'full'
else:
    screen = 'large'
    s = sysinfo.sw_version()
    if (s.find('RM-505') != -1):
        pass
    elif (s.find('RM-506') != -1):
        pass
    elif (s.find('RM-507') != -1):
        pass
    elif (s.find('RM-356') != -1):
        pass
    else:
        screen = 'full'
appuifw.app.screen = screen
appuifw.app.orientation = 'landscape'
appuifw.app.title = u'Kameramation'
appuifw.app.exit_key_handler = cb_quit
appuifw.app.menu = [(u'View:',
  ((u'Primary camera',
    lambda :set_camera(0)
),
   (u'Secondary camera',
    lambda :set_camera(1)
))),
 (u'About',
  menu_about),
 (u'Exit',
  cb_quit)]
canvas = appuifw.Canvas(redraw_callback=cb_redraw)
appuifw.app.body = canvas
(vx, vy,) = (xx, yy,) = canvas.size
img0 = graphics.Image.new((vx,
 vy))
ima0 = graphics.Image.new((vx,
 vy))
img1 = graphics.Image.new((vy,
 vx))
ima1 = graphics.Image.new((vy,
 vx))
img = img0
ima = ima0
img.clear(RGB_BLACK)
wait_note(u'Initializing,', u'please wait!')
if (xx > 320):
    dx = 20
else:
    dx = 10
import camera
import _camera
camera.start_finder(cb_view, size=(((3 * vx) / 4),
 ((3 * vy) / 4)))
app_lock = e32.Ao_lock()
app_lock.wait()

