
import md5, urllib, httplib, camera, key_codes, os, os.path

API_KEY = "c62dcNiOgTeVhAaLdIxDsdf17ee3afe9"
SECRET = "c932fFxAkK9E648d"
API_URL = "http://flickr.com/services/rest/"
UPLOAD_URL = "http://api.flickr.com/services/upload/"

IMG_FILE = u"E:\\Data\\Instaflickr\\instaflickr.jpg"
TOKEN_FILE = u"E:\\Data\\Instaflickr\\instaflickr.txt"
BLOCKSIZE = 8192

PROGRESS_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 0, 0)

if not os.path.exists("E:\\Data\\Instaflickr"):
        os.makedirs("E:\\Data\\Instaflickr")

def naive_xml_parser(key, xml):
        key = key.lower()
        for tag in xml.split("<"):
                tokens = tag.split()
                if tokens and tokens[0].lower().startswith(key):
                        return tag.split(">")[1].strip()
        return None


def load_token():
        global flickr_token
        try:
                flickr_token = file(TOKEN_FILE).read()
        except:
                new_token()

def new_token():
        global flickr_token
        
        mini_token = appuifw.query(u"Give Flickr mini-token "
                u"(e.g. 123456100)", "number")
        if not mini_token:
                return
        
        params = {"method": "flickr.auth.getFullToken",
                  "api_key": API_KEY,
                  "mini_token": str(mini_token)}
        flickr_token = naive_xml_parser("token",
                   flickr_signed_call(params))
        if flickr_token:
                try:
                        f = file(TOKEN_FILE, "w")
                        f.write(flickr_token)
                        f.close()
                        appuifw.note(u"Token saved!", "info")
                except:
                        appuifw.note(u"Could not save token",
                                        "error")
        else:
                appuifw.note(u"Invalid token", "error")


def flickr_signed_call(params):
        keys = params.keys()
        keys.sort()
        msg = SECRET
        for k in keys:
                if k != "photo":
                        msg += k + params[k]
        
        params['api_sig'] = md5.new(msg).hexdigest()
        
        if "photo" in params:
                return flickr_multipart_post(params)
        else:
                url = API_URL + "?" + urllib.urlencode(params)
                return urllib.urlopen(url).read()



def flickr_multipart_post(params):
        BOUNDARY = "----ds9io349sfdfd!%#!dskm"
        body = []
        for k, v in params.items():
                body.append("--" + BOUNDARY)
                part_head = 'Content-Disposition: '
                            'form-data; name="%s"' % k
                if k == "photo":
                        body.append(part_head +
                                ';filename="up.jpg"')
                        body.append('Content-Type: image/jpeg')
                else:
                        body.append(part_head)
                body.append('')
                body.append(v)

        body.append("--" + BOUNDARY + "--")
        body_txt = "\r\n".join(body)

        proto, tmp, host, path = UPLOAD_URL.split('/', 3)

        h = httplib.HTTP(host)
        h.putrequest('POST', "/%s" % path)
        h.putheader('content-type', 
                "multipart/form-data; boundary=%s" % BOUNDARY)
        h.putheader('content-length', str(len(body_txt)))
        h.endheaders()

        try:
                offs = 0
                for i in range(0, len(body_txt), BLOCKSIZE):
                        offs += BLOCKSIZE
                        h.send(body_txt[i: offs])
                        progress_bar(min(1.0, 
                                offs / float(len(body_txt))))
                
                errcode, errmsg, headers = h.getreply()
                return h.file.read()
        except:
                return None


def progress_bar(p):
        y = canvas.size[1] / 2
        max_w = canvas.size[0] - 30
        canvas.rectangle((15, y, p * max_w, y + 10),\
                         fill = PROGRESS_COLOR)

def show_text(txt):
        s = canvas.size
        canvas.text((10, s[1] / 2 - 15), txt,\
                fill=TEXT_COLOR, font="title")

def finder_cb(im):
        canvas.blit(im)

def start_viewfinder():
        if flickr_token:
                camera.start_finder(finder_cb)
                canvas.bind(key_codes.EKeySelect, take_photo)
        else:
                appuifw.note(u"Give a Flickr token first",
                             "error")

def take_photo():
        canvas.bind(key_codes.EKeySelect, None)
        camera.stop_finder()
        
        show_text(u"Hold still!")
        image = camera.take_photo(size = (640, 480))

        s = canvas.size
        canvas.blit(image,target=(0,0,s[0],(s[0]/4*3)), scale=1)
        show_text(u"Uploading to Flickr...")
        
        image.save(IMG_FILE)
        jpeg = file(IMG_FILE, "r").read()

        params = {'api_key': API_KEY, 'title': 'InstaFlickr', 
                  'auth_token': flickr_token,\
                  'photo': jpeg}
        ret = flickr_signed_call(params)
        canvas.clear((255, 255, 255))
        if ret:
                show_text(u"Photo sent ok!")
        else:
                show_text(u"Network error")


def access_point():
        global ap_id
        ap_id = socket.select_access_point()
        apo = socket.access_point(ap_id)
        socket.set_default_access_point(apo)

def quit():
        camera.stop_finder()
        app_lock.signal()
        
appuifw.app.exit_key_handler = quit
appuifw.app.title = u"InstaFlickr"
appuifw.app.menu = [(u"Take photo", start_viewfinder),
                    (u"New token", new_token),
                    (u"Access point", access_point),
                    (u"Quit", quit)]

appuifw.app.body = canvas = appuifw.Canvas()
canvas.clear((255, 255, 255))
show_text(u"Welcome to InstaFlickr")

load_token()
app_lock = e32.Ao_lock()
app_lock.wait()
