
import os, os.path, audio, appuifw, camera, key_codes, graphics

PATH = "E:\\Data\\Vocabulector\\"

def load_translations():
        global trans, dict_file
        if not os.path.exists(PATH):
                os.makedirs(PATH)
        dict_file = file(PATH + "trans.txt", "rw")
        trans = []
        for line in dict_file:
                line = line.decode("utf-8")
                native, foreign = line.strip().split(":")
                trans.append((native, foreign))


def add_entry():
        global fname, text, photo
        text = photo = None

        native = appuifw.query(u"Native word:", "text")
        if not native: return
        foreign = appuifw.query(u"Foreign word:", "text")
        if not foreign: return

        fname = PATH + native
        trans.append((native, foreign))
        line = "%s:%s" % (native, foreign)
        print >> dict_file, line.encode("utf-8")

        if appuifw.query(u"Record sound", "query"):
                record_sound()
        if appuifw.query(u"Take photo", "query"):
                camera.start_finder(viewfinder)
                canvas.bind(key_codes.EKeySelect, take_photo)
        else:
                appuifw.note(u"Entry added!", "info")

def record_sound():
        snd = audio.Sound.open(fname + ".wav")
        snd.record()
        appuifw.query(u"Press OK to stop recording", "query")
        snd.close()

def viewfinder(img):
        canvas.blit(img)

def take_photo():
        global photo
        canvas.bind(key_codes.EKeySelect, None)
        camera.stop_finder()
        photo = camera.take_photo(size = (640,480))
        handle_redraw(None)
        photo.save(fname + ".jpg")


def show_native():
        lst = []
        for native, foreign in trans:
                lst.append(native)
        idx = appuifw.selection_list(choices = lst, search_field = 1)
        if idx != None:
                foreign = trans[idx][1]
                fname = PATH + lst[idx]
                show(fname, foreign)

def show_foreign():
        lst = []
        for native, foreign in trans:
                lst.append(foreign)
        idx = appuifw.selection_list(choices = lst, search_field = 1)
        if idx != None:
                native = trans[idx][0]
                fname = PATH + native
                show(fname, native)

def show(fname, translation):
        global photo, text, snd
        photo = None
        text = translation
        try:
                photo = graphics.Image.open(fname + ".jpg")
        except: pass
        handle_redraw(None)
        try:
                snd = audio.Sound.open(fname + ".wav")
                snd.play()
        except: pass


def handle_redraw(rect):
        canvas.clear((255, 255, 255))
        w, h = canvas.size
        if photo:
                canvas.blit(photo, target = (0, 0, w, int(0.75 * h)),
                        scale = 1)
        if text:
                canvas.text((20, h / 2), text,
                        fill = (0, 0, 255), font = "title")

def quit():
        dict_file.close()
        app_lock.signal()

photo = None
text = u"<vocabulector>"
appuifw.app.title = u"Personal vocabulary trainer"
appuifw.app.exit_key_handler = quit
appuifw.app.screen = 'large'

canvas = appuifw.Canvas(redraw_callback = handle_redraw)
appuifw.app.body = canvas
appuifw.app.menu = [(u"Add entry", add_entry),
                    (u"Show native entries", show_native),
                    (u"Show foreign entries", show_foreign)]

load_translations()
app_lock = e32.Ao_lock()
app_lock.wait()
