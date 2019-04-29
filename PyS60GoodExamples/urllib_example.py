# this script lets you download a picture from the net


# use the urllib library
import urllib
import appuifw

def fetchfile():
    # define a url where the picture you want to download is located on the net
    url = "http://weather.gov/mdl/radar/rcm1pix_b.gif"
    # define the file name and the location of the downloaded file for local storage e.g. on the c drive
    tempfile = "c:\\testimg.gif"
    try:
        # fetch the image
        urllib.urlretrieve(url, tempfile)
        appuifw.note(u"Image received", "info")
    except:
        print "Could not fetch file."

if appuifw.query(u"fetch image?","query") == True:
    fetchfile()        
