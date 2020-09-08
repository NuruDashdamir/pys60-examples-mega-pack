# Copyright (c) 2006 Jurgen Scheible
# image upload to URL

import appuifw,e32,httplib


def upload_image_to_url():
    
    filename = 'e:\\Images\\picture1.jpg'
    picture = file(filename).read()

    conn = httplib.HTTPConnection("www.mobilenin.com")
    conn.request("POST", "/pys60/php/upload_image_to_url.php", picture)
    print "upload started ..."
    e32.ao_yield()
    response = conn.getresponse()
    remote_file = response.read()
    conn.close()
    appuifw.note(u" " + remote_file, "info")
    print remote_file


upload_image_to_url()

