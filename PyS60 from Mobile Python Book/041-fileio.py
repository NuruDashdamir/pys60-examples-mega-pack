
f = file(u"c:\\python\\test.txt", "w+")
print >> f, "Ip dip, sky blue"
f.seek(0)
print "File says", f.read()
f.close()
