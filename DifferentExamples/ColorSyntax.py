import appuifw as a,e32
f=open('c:/2.Py')
x=f.read()
f.close()
try:
 for i in xrange(50000):
  j=x.split('\n')[i]
  m=j.split(' ')

  if 'def' in m:
   a.app.body.color=0xff0000
   print j

  elif 'import' in m:
   a.app.body.color=0xaaaaaa
   print j


  elif 'class' in m:
   a.app.body.color=0x00ff00
   print j

  elif ('except') in m:
   a.app.body.color=0xf0ff00
   print j
  elif ('try') in m:
   a.app.body.color=0xf0ff00
   print j


  elif ('if') in m:
   a.app.body.color=0xf0ff00
   print j
  elif ('elif') in m:
   a.app.body.color=0xf0ff00
   print j
  elif ('else:') in m:
   a.app.body.color=0xf0ff00
   print j



  elif ('del') in m:
   a.app.body.color=0x0f0f0f
   print j
  elif ('return') in m:
   a.app.body.color=0x0f0f0f
   print j
  elif ('global') in m:
   a.app.body.color=0x0f0f0f
   print j


  elif ('while') in m:
   a.app.body.color=0x333333
   print j
  elif ('for') in m:
   a.app.body.color=0x333333
   print j


  else:
   a.app.body.color=0x0000ff
   print j
  e32.ao_sleep(0.2)
except:print 'Done'