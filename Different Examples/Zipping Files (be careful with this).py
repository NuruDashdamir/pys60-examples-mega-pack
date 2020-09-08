import zipfile as zf
import e32,appuifw
import os

wa=e32.ao_sleep
com=zf.ZIP_DEFLATED

def zip(path,name):
    name=appuifw.query(u'name','text',u'New archive')
    c=os.listdir(path)
    z=zf.ZipFile('e:/'+name+'.zip','w',com)
    for i in xrange(len(c)):
        if os.path.isdir(path+c[i])==1:pass
        else:
            print c[i]	
            wa(0.01)
            z.write(path+c[i],path[3:]+c[i])
            wa(0.01)
    z.close()
    print 'e:/'+name+'.zip'

zip('e:/0/',"test")