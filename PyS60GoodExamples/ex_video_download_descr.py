
import appuifw
import e32
# import urllib
import urllib

print "press options"

# function that handles the fetching and the playing of the video
def fetching():
    # define the url where the video file is located on the server
    url = "http://www.leninsgodson.com/courses/pys60/resources/vid001.3gp"
    # define the loction on the phone where the fetched video file shall be stored
    tempfile = "c:\\video01.3gp"
    try:
        print "Retrieving information..."
        # fetch down the video and store it to you hard drive
        urllib.urlretrieve(url, tempfile)
        # create an active object before playin the video
        lock=e32.Ao_lock()
        # a content handler handles the playing of the video
        # load the content handler and tell to release the active object after the video has finnished playing (lock.signal)
        content_handler = appuifw.Content_handler(lock.signal)
        # open the video via the content handler. It will start playing automatically
        content_handler.open(tempfile)
        # Wait for the user to exit the image viewer.
        lock.wait()
        print "Video viewing finished."
        print "press options or exit."
    except IOError:
        print "Could not fetch the image."
    except:
        print "Could not open data received."

# define the application menu with one choice "get video" and call the fetching video
def main_menu_setup():
    appuifw.app.menu = [(u"get video", fetching)]

def exit_key_handler():
    global script_lock
    script_lock.signal()
    appuifw.app.set_exit()
    
script_lock = e32.Ao_lock()

appuifw.app.title = u"Get video"

# call the application menu function
main_menu_setup()

appuifw.app.exit_key_handler = exit_key_handler
script_lock.wait()


 

