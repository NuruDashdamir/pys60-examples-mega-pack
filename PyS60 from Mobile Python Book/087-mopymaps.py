

import urllib, appuifw, e32, graphics, key_codes, os, os.path

APP_ID = "reuBqRjOdK4E3NaKfEsYopj3459fmas_xg7oa"
MAP_URL = "http://local.yahooapis.com/MapsService/V1/mapImage?"
MAP_FILE = u"E:\\Images\\mopymap.png"

if not os.path.exists("E:\\Images"):
        os.makedirs("E:\\Images")

def naive_xml_parser(key, xml):
        key = key.lower()
        for tag in xml.split("<"):
                tokens = tag.split()
                if tokens and tokens[0].lower().startswith(key):
                        return tag.split(">")[1].strip()
        return None


def new_map():
        addr = appuifw.query(u"Address:", "text")
        if not addr:
                return
        params = {"location": addr,
                  "appid": APP_ID,
                  "image_type": "png",
                  "image_height": "600",
                  "image_width": "600",
                  "zoom": "6"
        }
        show_text(u"Loading map...")
        try:
                url = MAP_URL + urllib.urlencode(params)
                res = urllib.urlopen(url).read()
        except:
                show_text(u"Network error")
                return

        img_url = naive_xml_parser("result", res)
        if img_url:
                show_text(u"Loading map......")
                load_image(img_url)
                handle_redraw(canvas.size)
        else:
                msg = naive_xml_parser("message", res)
                show_text(u"%s" % msg)

def load_image(url):
        global mapimg, map_x, map_y, status
        res = urllib.urlopen(url).read()
        f = file(MAP_FILE, "w")
        f.write(res)
        f.close()
        mapimg = graphics.Image.open(MAP_FILE)
        map_x = mapimg.size[0] / 2 - canvas.size[0] / 2
        map_y = mapimg.size[1] / 2 - canvas.size[1] / 2
        status = None



def show_text(txt):
        global status
        status = txt
        handle_redraw(canvas.size)

def handle_redraw(rect):
        if mapimg:
                canvas.blit(mapimg, target=(0, 0),
                            source=(map_x, map_y))
        else:
                canvas.clear((255, 255, 255))
        if status:
                canvas.text((10, 50), status,
                            fill=(0, 0, 255), font="title")

def handle_keys(event):
        global map_x, map_y
        if event['keycode'] == key_codes.EKeyLeftArrow:
                map_x -= 10
        elif event['keycode'] == key_codes.EKeyRightArrow:
                map_x += 10
        elif event['keycode'] == key_codes.EKeyUpArrow:
                map_y -= 10
        elif event['keycode'] == key_codes.EKeyDownArrow:
                map_y += 10
        handle_redraw(canvas.size)

def quit():
    app_lock.signal()

map_x = map_y = 0
mapimg = status = None

appuifw.app.exit_key_handler = quit
appuifw.app.title = u"MopyMaps!"
appuifw.app.menu = [(u"New location", new_map),
                    (u"Quit", quit)]

canvas = appuifw.Canvas(redraw_callback = handle_redraw,
        event_callback = handle_keys)
appuifw.app.body = canvas

show_text(u"Welcome to MopyMaps!")
app_lock = e32.Ao_lock()
app_lock.wait()
