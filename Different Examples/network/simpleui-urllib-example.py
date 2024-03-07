# this script lets you download a picture from the net
import urllib
import appuifw

def fetchfile():
    # HTTP supported url (not HTTPS-only) where a picture is located
    url = "http://eu.httpbin.org/image/jpeg"
    # the file name and the location of the file download
    tempfile = "D:\\testimg.jpeg"
    try:
        # fetch the image
        urllib.urlretrieve(url, tempfile)
        appuifw.note(u"Image received", "info")
    except:
        appuifw.note(u"Could not fetch file", "info")

if appuifw.query(u"fetch image?","query"):
    fetchfile()