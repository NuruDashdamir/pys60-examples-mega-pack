import zipfile
import e32
import appuifw
import os

def zip(path, name):
    name=appuifw.query(u'name', 'text', u'New archive')
    c=os.listdir(path)
    z=zipfile.ZipFile('e:/'+name+'.zip', 'w', zf.ZIP_DEFLATED)
    for i in xrange(len(c)):
        if os.path.isdir(path+c[i])==1:pass
        else:
            print c[i]	
            e32.ao_sleep(0.01)
            z.write(path+c[i],path[3:]+c[i])
            e32.ao_sleep(0.01)
    z.close()
    print 'e:/'+name+'.zip'

zip('e:/0/', 'test')