import appuifw, e32

import urllib

print "press options"



# function that handles the fetching and the playing of the video

def vdwn():

	def fetching():

    # define the url where the video file is located on the server

    		url ="http://www.leninsgodson.com/courses/pys60/resources/vid001.3gp"

    # define the loction on the phone where the fetched video file shall be stored

    		tempfile = "e:\\video01.3gp"

    		try:

        		print "Retrieving information..."

        # fetch down the video and store it to you hard drive

        		urllib.urlretrieve(url, tempfile)

        # create an active object before playin the video

        		lock=e32.Ao_lock()

        # a content handler handles the playing of the video

        # load the content handler and tell to release the active object after the video has  
          finished playing (lock.signal)

        		content_handler = appuifw.Content_handler(lock.signal)

        # open the video via the content handler. It will start playing automatically

        		content_handler.open(tempfile)

        # Wait for the user to exit the image viewer.

        		lock.wait()

        		print "Video viewing finished."

    		except:

        		print "Problems."


	def quit():

    		app_lock.signal()



# define the application menu with one choice "get video" and call the fetching video

	appuifw.app.menu = [(u"get video", fetching)]



	appuifw.app.title = u"Get video"



	appuifw.app.exit_key_handler = quit

	app_lock = e32.Ao_lock()

	app_lock.wait()
