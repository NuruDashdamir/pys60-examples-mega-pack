import appuifw,e32,random
appuifw.app.body=r=appuifw.Canvas()
def crack():
 appuifw.app.title=u'Cracking Pass...'
 a=str(random.randint(11111111,99999999))+str(random.randint(11111111,99999999))
 for i in xrange(len(a)):
  for p in xrange(9):
   r.clear(0xaaaaaa)
   r.text((30,70),u''+a[:i]+str(p)*(len(a)-i))
   r.rectangle((7,100,7+(170/len(a))*i,110),0x0000f0,0x808080)
   e32.ao_sleep(0.03)
 appuifw.app.title=u'Passwort was Cracked!'
appuifw.app.menu=[(u'Crack',crack)]
e32.Ao_lock().wait()