
import camera, httplib

PHOTO = u"e:\\Images\\photo_upload.jpg"

def photo():
    photo = camera.take_photo()
    photo.save(PHOTO)
     
def upload():
    image = file(PHOTO).read()
    conn = httplib.HTTPConnection("www.myserver.com")
    conn.request("POST", "/upload.php", image)
    conn.close()

photo()
print "photo taken"
upload()
print "uploading done"
