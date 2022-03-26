import appuifw,e32
appuifw.app.body=r=appuifw.Text()
##########################

l=150

##########################
##########################
##########################

def text_bar(i,l,name=None):
 if name==None:pass
 else:
  r.set(u''+str(name)+'\n'+str(i)+'/'+str(l))
 e32.ao_sleep(0.001)

for i in xrange(l):
 text_bar(i,l,'text_bar')

##########################

def text_procent_bar(i,l,name=None):
 procent=l*0.01
 obw=i/procent
 if name==None:pass
 else:
  r.set(u''+str(name)+'\n'+str(obw)[:5]+'%')
 e32.ao_sleep(0.001)

for i in xrange(l):
 text_procent_bar(i,l,'text_procent_bar')

##########################
##########################
##########################

appuifw.app.body=canv=appuifw.Canvas()

##########################

def canvas_bar(i,l,name=None):
  procent=l*0.01
  obw=i/procent
  canv.clear(0xaaaaaa)
  if name==None:pass
  else:
    canv.text((10,80),u''+str(name))
  canv.rectangle((7,100,7+obw*1.6,110),0xff0000,0x0000ff)
  canv.text((7,95),u''+str(obw)[:5]+u'%')
  e32.ao_sleep(0.1)

for i in xrange(l):
 canvas_bar(i,l,'canvas_bar')

##########################

def new_canvas_bar(i,l,name=None):
  procent=l*0.01
  obw=i/procent
  canv.clear(0xaaaaaa)
  if name==None:pass
  else:
    canv.text((10,80),u''+str(name))
  canv.rectangle((7,100,7+obw*1.6,110),0xff0000,0x0000ff)
  canv.text((7+obw,95),u''+str(obw)[:5]+u'%')
  e32.ao_sleep(0.00001)

for i in xrange(l):
 new_canvas_bar(i,l,'new_canvas_bar')

##########################