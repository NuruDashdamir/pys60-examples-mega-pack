# use the urllib library

# useful for simply downloading files from the net

import urllib

import appuifw



def imgdw():

	def fetchfile():

    # define a url where the picture you want to download is located on the net

    		url = appuifw.query(u"Enter valid url","text",u"http://www.python.org/images/python-logo.gif")

    # define the file name and the location of the downloaded file for local storage e.g. on the c drive

    		tempfile = u"E:\\testimg.gif"

    		try:

        # fetch the image

        		urllib.urlretrieve(url, tempfile)

        		appuifw.note(u"Image received", "info")

    		except:

        		print "Could not fetch file."



	if appuifw.query(u"fetch image?","query") == True:

    		fetchfile()
