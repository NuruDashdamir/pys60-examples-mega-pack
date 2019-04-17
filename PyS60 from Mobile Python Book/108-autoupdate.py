
import urllib

CODE = "mytest.py"
URL = "http://www.myownserver.com/pycode/"

code = urllib.urlopen(URL + CODE).read()
f = file(u"E:\\Python\\" + CODE, "w")
f.write(code)
f.close()
print "File %s updated succesfully!" % CODE
