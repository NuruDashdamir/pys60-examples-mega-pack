import appuifw, e32, urllib

print "press options"

def fetching():
    url = "http://www.leninsgodson.com/courses/pys60/resources/vid001.3gp"
    tempfile = "e:\\video01.3gp"
    try:
        print "Retrieving information..."
        urllib.urlretrieve(url, tempfile)
        lock=e32.Ao_lock()
        content_handler = appuifw.Content_handler(lock.signal)
        content_handler.open(tempfile)
        # Wait for the user to exit the image viewer.
        lock.wait()
        print "Video viewing finished."
    except:
        print "Problems."

def quit():
    app_lock.signal()

appuifw.app.menu = [(u"get video", fetching)]

appuifw.app.title = u"Get video"

appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()


 

