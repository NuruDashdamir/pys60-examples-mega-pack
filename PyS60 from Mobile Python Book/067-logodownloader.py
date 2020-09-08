
import urllib, appuifw, e32

URL = "http://www.python.org/images/python-logo.gif"

dest_file = u"E:\\Images\\python-logo.gif"
urllib.urlretrieve(URL, dest_file)

lock = e32.Ao_lock()
viewer = appuifw.Content_handler(lock.signal)
viewer.open(dest_file)
lock.wait()
