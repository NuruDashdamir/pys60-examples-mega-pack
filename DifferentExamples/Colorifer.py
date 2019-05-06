#
#
# screept by _killed_
# http://killed.h2m.ru
#
#
import appuifw,e32
appuifw.app.body=t=appuifw.Text()
r,g,b=0,0,0
for r in xrange(0,255,25):
 for g in xrange(0,255,25):
  for b in xrange(0,255,25):
   appuifw.app.body.color=r,g,b
   appuifw.app.title=unicode(str(r)+','+str(g)+','+str(b))
   t.add(u'#')
   e32.ao_sleep(0.01)
  t.add(u'\n')
 t.add(u''+str(r)+','+str(g)+','+str(b)+'\n')
e32.Ao_lock().wait()