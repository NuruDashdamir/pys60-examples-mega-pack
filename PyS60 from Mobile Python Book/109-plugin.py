
import urllib, appuifw

URL = "http://www.myownserver.com/pycode/"

def download_plugin(plugin_name):
    filename = plugin_name + ".py"
    code = urllib.urlopen(URL + filename).read()
    f = file(u"E:\\Python\\Lib\\" + filename, "w")
    f.write(code)
    f.close()
    return __import__(plugin_name)

plugin_name = appuifw.query(u"Give plug-in name", "text")
print "Downloading plugin", plugin_name
plugin = download_plugin(plugin_name)
print "Plugin loaded!"
plugin.askword()

