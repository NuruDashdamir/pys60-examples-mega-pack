#
#
# screept by _killed_
# http://killed.h2m.ru
#
#
import appuifw,e32,random
appuifw.app.body=r=appuifw.Text()
appuifw.app.body.color=0x00ff00
appuifw.app.screen='full'
n=0
while 1:
 s=''
 for i in xrange(28):
  s+=str(random.randint(0,1))
 r.set_pos(0)
 r.add(u'\n')
 r.set_pos(0)
 r.add(u''+s)
 del s
 e32.ao_sleep(0.001)
e32.Ao_lock().wait()