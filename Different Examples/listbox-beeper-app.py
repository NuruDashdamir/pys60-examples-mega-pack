#233737
import topwindow as TopWindow
import graphics
import appuifw
import e32
import time
import audio
import sysinfo
import string
import inbox
import os
import telephone
try: import miso
except: pass

ppb=[u'LCGJukebox',u'FIVNPlayer',u'Other',u'None']
fpp=[u'C:\\Data\\Beeper\\',u'E:\\Beeper\\',u'None']
aww=[u'AMR',u'WAV']

fn='REC'
li=ladow=ekran=mp3=0

def koniec():
 if appuifw.query(u'Exit ?','query')==True: appuifw.app.set_exit()

def prog():
 appuifw.note(u'Beeper 6.00'+u'\n'+'forum.gsmcenter.pl'+u'\n'+'kompiler@tlen.pl','info')
 appuifw.note(u'English version for'+u'\n'+'symbian-freak.com','info')

def ukryj():
 try: e32.start_exe(u'z:\\sys\\bin\\phone.exe','')
 except: pass

def nic():
 pass

def call(state):
 global fn
 global rec
 q=1
 if state[0]==3: 
  fn='REC'+state[1]
  fn=fn.replace('+','')
 if state[0]==6:
  if len(fn)<=3: 
   (rok,mies,dz,godz,min,k,k,k,k)=time.localtime()
   rok=str(rok)[2:4] 
   mies='%02d'%(mies) 
   dz='%02d'%(dz)  
   godz='%02d'%(godz) 
   min='%02d'%(min) 
   fn='REC'+rok+mies+dz+godz+min
  while os.path.isfile(unicode(fpp[int(ustaw[56:57])]+fn+'_'+str(q)+'.'+string.lower(aww[int(ustaw[55:56])]))): q=q+1
  if fpp[int(ustaw[56:57])]==u'C:\\Data\\Beeper\\':
   if os.path.isdir('C:\\Data\\Beeper\\') is not True: 
    try: os.mkdir('C:\\Data')
    except: pass
    try: os.mkdir('C:\\Data\\Beeper')
    except: pass
  if fpp[int(ustaw[56:57])]==u'E:\\Beeper\\':
   if os.path.isdir('E:\\Beeper\\') is not True:
    try: os.mkdir('E:\\Beeper')
    except: pass
  if fpp[int(ustaw[56:57])]<>u'None':
   rec =audio.Sound.open(unicode(fpp[int(ustaw[56:57])]+fn+'_'+str(q)+'.'+string.lower(aww[int(ustaw[55:56])])))
   rec.record()
 if state[0]==8:
  try:
   fn='REC'
   rec.stop()
   rec.close()
  except: pass
 telephone.call_state(call)
telephone.call_state(call)

try:
 dat=open(u'c:\\system\\Beeper.data','r')
 xt=dat.readline()
 ustaw=xt[0:57]
 sciezkaplik=sck=dat.readline()
 pb=dat.readline()
 dat.close()
except:
 try: dat.close()
 except: pass
 ustaw=u'060015000000001012000000000255255255100006022010000060002'
 sck=sciezkaplik=''
 pb=ppb[3]
xt=0
sck=sciezkaplik=sck.replace(chr(10),'')
if int(ustaw[48:51])==1: ukryj()
screen = TopWindow.TopWindow()
img = graphics.Image.new((int(ustaw[0:3]),int(ustaw[3:6])))
ima = graphics.Image.new((int(ustaw[0:3]),int(ustaw[3:6])))
if int(ustaw[18:21])==888: ima.blit(graphics.screenshot(),((int(ustaw[6:9]),int(ustaw[9:12])),(int(ustaw[6:9])+int(ustaw[0:3]),int(ustaw[9:12])+int(ustaw[3:6]))))

def wybierz():
 global lista
 global listbox
 global li
 global screen
 global img 
 global ustaw
 global ekran
 global mp3
 global sciezkaplik
 global ladow
 global sck
 global pb
 mp3=0
 sciezkaplik=sck
 index=listbox.current()
 appuifw.app.body=listbox=appuifw.Listbox([(u'Beeper 6.00',u'symbian-freak.com')],ukryj)
 if int(ustaw[45:48])<>0:screen.hide()
 if lista[index][0]==u'General Options':
  k=1
  while (k>0):
   k=appuifw.popup_menu([u'Alert sound',u'Alert volume',u'Hour alert range',u'Text style',u'Bar info',u'Startup appearance'],u'General Options')
   if k==1:
    q=appuifw.popup_menu([u'100%',u'75%',u'50%',u'25%',u'Silent'],u'Alert volume')
    if q<>None: ustaw=ustaw[0:36]+'%03d'%(100-(q*25))+ustaw[39:57]  
   elif k==2:
    q=appuifw.query(u'Begin (0-23)','number',int(ustaw[39:42]))
    if (q<>None)and(q<24):
     ustaw=ustaw[0:39]+'%03d'%q+ustaw[42:57]
     q=appuifw.query(u'End (0-23)','number',int(ustaw[42:45]))
     if (q<>None)and(q<24): ustaw=ustaw[0:42]+'%03d'%q+ustaw[45:57]
   elif k==3:
    q=appuifw.popup_menu([u'Normal',u'Bold',u'Normal italic',u'Bold italic'],u'Text style')
    if q<>None: ustaw=ustaw[0:45]+'%03d'%(q+(10*(int(ustaw[45:48])/10)))+ustaw[48:57]
   elif k==4:
    q=appuifw.popup_menu([u'None',u'Time',u'Date',u'Ram',u'Signal',u'Battery'],u'Bar info')
    if q<>None: ustaw=ustaw[0:45]+'%03d'%((q*10)+(int(ustaw[45:48])%10))+ustaw[48:57]
   elif k==5:
    q=appuifw.popup_menu([u'Show after startup',u'Hide after startup'],u'Startup appearance')
    if q<>None: ustaw=ustaw[0:48]+'%03d'%q+ustaw[51:57]
 elif lista[index][0]==u'Bar Face':
  k=0
  while k is not None:
   k=appuifw.popup_menu([u'Bar size',u'Bar position',u'Text position'],u'Bar Face')
   if k==0:
    q=appuifw.query(u'Value X','number',int(ustaw[0:3]))
    if (q<>None)and(q<353): 
     ustaw='%03d'%q+ustaw[3:57]
     q=appuifw.query(u'Value Y','number',int(ustaw[3:6]))
     if (q<>None)and(q<417): 
      ustaw=ustaw[0:3]+'%03d'%q+ustaw[6:57]
   if k==1:
    q=appuifw.query(u'Value X','number',int(ustaw[6:9]))
    if (q<>None)and(q<353): 
     ustaw=ustaw[0:6]+'%03d'%q+ustaw[9:57]
     q=appuifw.query(u'Value Y','number',int(ustaw[9:12]))
     if (q<>None)and(q<417):
      ustaw=ustaw[0:9]+'%03d'%q+ustaw[12:57]  
   if k==2:
    q=appuifw.query(u'Value X','number',int(ustaw[12:15]))
    if (q<>None)and(q<353): 
     ustaw=ustaw[0:12]+'%03d'%q+ustaw[15:57] 
     q=appuifw.query(u'Value Y','number',int(ustaw[15:18]))
     if (q<>None)and(q<417): 
      ustaw=ustaw[0:15]+'%03d'%q+ustaw[18:57]
 elif lista[index][0]==u'Bar Color':
  k=0
  while k is not None:
   k=appuifw.popup_menu([u'Bar color',u'Text color'],u'Bar Color')
   if k==0:
    q=appuifw.query(u'Value R (0-256) (888)','number',int(ustaw[18:21])) 
    if q==888:
     ustaw=ustaw[0:18]+'888000000'+ustaw[27:57]
     ima.blit(graphics.screenshot(),((int(ustaw[6:9]),int(ustaw[9:12])),(int(ustaw[6:9])+int(ustaw[0:3]),int(ustaw[9:12])+int(ustaw[3:6]))))
    else:
     if (q<>None)and(q<256):
      ustaw=ustaw[0:18]+'%03d'%q+ustaw[21:57]
      q=appuifw.query(u'Value G (0-256)','number',int(ustaw[21:24])) 
      if (q<>None)and(q<257):
       ustaw=ustaw[0:21]+'%03d'%q+ustaw[24:57]
       q=appuifw.query(u'Value B (0-256)','number',int(ustaw[24:27])) 
       if (q<>None)and(q<257):
        ustaw=ustaw[0:24]+'%03d'%q+ustaw[27:57]
   elif k==1:
    q=appuifw.query(u'Value R (0-255)','number',int(ustaw[27:30])) 
    if (q<>None)and(q<256):
     ustaw=ustaw[0:27]+'%03d'%q+ustaw[30:57]
     q=appuifw.query(u'Value G (0-255)','number',int(ustaw[30:33])) 
     if (q<>None)and(q<256):
      ustaw=ustaw[0:30]+'%03d'%q+ustaw[33:57]
      q=appuifw.query(u'Value B (0-255)','number',int(ustaw[33:36])) 
      if (q<>None)and(q<256):
       ustaw=ustaw[0:33]+'%03d'%q+ustaw[36:57]
 elif lista[index][0]==u'Extras':
  p=0
  while p is not None:
   p=appuifw.popup_menu([u'Test alarm',u'Highlight screen',u'Battery charge',u'Restart phone',u'Export sms',u'Program starter',u'Call recorder'],u'Extras')
   if p==0:
    try:
     if os.path.isdir(sciezkaplik):
      q=appuifw.query(u'Sound file (0-24)','number',0)
      mp3=audio.Sound.open(unicode(sciezkaplik+'\\'+str('%02d'%q)+'.mp3'))
     else: mp3=audio.Sound.open(unicode(sciezkaplik))
     mp3.play()
     audio.Sound.set_volume(mp3,int(audio.Sound.max_volume(mp3)*(float(int(ustaw[36:39]))/float(100))))
    except: pass
    try:
     miso.vibrate(500,100)
    except: pass
   elif p==1:
    if ekran>0: ekran=0
    else: ekran=1
    p=None
   elif p==2:
    if ladow>0: ladow=0
    else: ladow=1
    p=None
   elif p==3:
    if appuifw.query(u'Restart phone now ?','query')==True: e32.start_exe(u'z:\\sys\\bin\\starter.exe','')
   elif p==4:
    lista=[(u'Please wait',u'')]
    appuifw.app.body = listbox = appuifw.Listbox(lista, nic)
    index=0
    tx = appuifw.Text()
    inb = inbox.Inbox()
    msgs = inb.sms_messages()
    tx.clear()
    for msg in msgs:
     mies=time.strftime('%m',time.localtime(inb.time(msg)))
     dz=time.strftime('%d',time.localtime(inb.time(msg)))
     rok=time.strftime('%Y',time.localtime(inb.time(msg)))
     czas=time.strftime('%H:%M:%S',time.localtime(inb.time(msg)))
     tx.add(u'Sender: ')
     tx.add(unicode(inb.address(msg)))
     tx.add(u'\n')
     tx.add(u'Date: ')
     tx.add(unicode(dz+'.'+mies+'.'+rok))
     tx.add(u'\n')
     tx.add(u'Time: ')
     tx.add(unicode(czas))
     tx.add(u'\n')
     tx.add(unicode(inb.content(msg)))
     tx.add(u'\n')
     tx.add(u'\n')
    if len(tx.get())==0:
     tx.add(u'None message')
     tx.add(u'\n')
    (rok,mies,dz,godz,min,x,x,x,x)=time.localtime()
    rok=str(rok)[2:4] 
    mies='%02d'%(mies) 
    dz='%02d'%(dz)  
    godz='%02d'%(godz) 
    min='%02d'%(min) 
    appuifw.app.body = listbox = appuifw.Listbox([(u'Beeper 6.00',u'symbian-freak.com')], nic)
    q=appuifw.query(u'C:\\Data\\', 'text',unicode(rok+mies+dz+godz+min+'.txt'))
    if q is not None:
     k=tx.get() 
     try: 
      f=open('c:\\data\\'+q,'w') 
      k=k.replace(unichr(8233),unichr(13)+unichr(10))
      f.write(k.encode('utf-16')) 
      f.close() 
     except: appuifw.note(u'Error','error')
     else: 
      if appuifw.query(u'Open file now ?','query')==True: appuifw.Content_handler().open_standalone('c:\\data\\'+q)
   elif p==5:
    q=0
    while q<>None:
     q= appuifw.popup_menu([u'Program '+unicode(pb),u'Time '+unicode(ustaw[51:53])+u':'+unicode(ustaw[53:55])],u'Program starter')
     if q==0:
      k=appuifw.popup_menu(ppb,u'Program')
      if k is not None: 
       if k<>2: pb=ppb[k]
       else:
        k=appuifw.query(u'X:\\Sys\\Bin\\','text',u'program.exe')
        if k is not None:
         if len(k)>4:
          if k[len(k)-4:]=='.exe': pb=k[:len(k)-4]
     if q==1:
      k=appuifw.query(u'Time','time',float(int(ustaw[51:53])*3600+int(ustaw[53:55])*60))
      if k is not None: ustaw=ustaw[0:51]+str('%02d'%(k//3600))+str('%02d'%((k-((k//3600)*3600))//60))+ustaw[55:57]
   elif p==6:
    q=0
    while q<>None:
     q= appuifw.popup_menu([unicode(u'File path '+fpp[int(ustaw[56:57])]),unicode('File format '+aww[int(ustaw[55:56])])],u'Call recorder')
     if q==0:
      k=appuifw.popup_menu(fpp,u'File path')
      if k is not None: ustaw=ustaw[0:56]+str(k)
     if q==1:
      k=appuifw.popup_menu(aww,u'File format')
      if k is not None: ustaw=ustaw[0:55]+str(k)+ustaw[56:57]
 screen = TopWindow.TopWindow()
 screen.size=(int(ustaw[0:3]),int(ustaw[3:6]))
 screen._set_position((int(ustaw[6:9]),int(ustaw[9:12])))
 screen.add_image(img,(0,0))
 if (lista[index][0]==u'General Options')and(k==0):
  lista=[u'..']
  listbox=appuifw.Listbox(lista,pozycja)
  sck=sciezkaplik
  pozycja()
 else:
  try:
   xt=str(ustaw)+chr(10)+str(sciezkaplik)+chr(10)+str(pb)
   dat=open('c:\\system\\Beeper.data','w')
   dat.write(xt)
   dat.close()
  except: pass
  xt=0
  li=0
  lista=[(u'General Options',u'('+str(int(ustaw[36:39]))+') ('+str(int(ustaw[39:42]))+','+str(int(ustaw[42:45]))+') ('+str(1+int(ustaw[45:48])%10)+') ('+str(1+int(ustaw[45:48])/10)+') ('+str(1+int(ustaw[48:51]))+')'),(u'Bar Face',u'('+str(int(ustaw[0:3]))+','+str(int(ustaw[3:6]))+') ('+str(int(ustaw[6:9]))+','+str(int(ustaw[9:12]))+') ('+str(int(ustaw[12:15]))+','+str(int(ustaw[15:18]))+')'),(u'Bar Color',u'('+str(int(ustaw[18:21]))+','+str(int(ustaw[21:24]))+','+str(int(ustaw[24:27]))+') ('+str(int(ustaw[27:30]))+','+str(int(ustaw[30:33]))+','+str(int(ustaw[33:36]))+')'),(u'Extras',u'(Additional Functions)')]
  appuifw.app.body=listbox=appuifw.Listbox(lista, wybierz)
  appuifw.app.menu=[(u'Hide program',ukryj),(u'About',prog)]
  appuifw.app.exit_key_handler=koniec
  if int(ustaw[45:48])<>0: screen.show()

def pasek():
 global screen
 global img
 global ekran
 global mp3
 global ladow
 while 1:
  e32.Ao_timer().after(1)
  (rok,mies,dz,godz,min,sek,x,x,x)=time.localtime()
  godz='%02d'%(godz) 
  min='%02d'%(min) 
  sek='%02d'%(sek)
  if (godz==ustaw[51:53])and(min==ustaw[53:55])and(sek=='00')and(pb<>'None'):
   e32.reset_inactivity()
   try: appuifw.e32.start_exe(u'c:\\sys\\bin\\'+unicode(pb)+u'.exe','') 
   except:
    try: appuifw.e32.start_exe(u'e:\\sys\\bin\\'+unicode(pb)+u'.exe','')  
    except:
     try: appuifw.e32.start_exe(u'z:\\sys\\bin\\'+unicode(pb)+u'.exe','')  
     except: pass
  try:
   if (int(ustaw[36:39])<>0)and(sysinfo.active_profile()<>u'silent'):
    if ( (int(min)==0)and(int(sek)==0) or (int(sysinfo.battery())==100)and(ladow>0) ):
     if (int(sysinfo.battery())==100)and(ladow>0): ladow=0
     if os.path.isdir(sciezkaplik):
      if (int(min)==0)and(int(sek)==0):
       mp3=audio.Sound.open(unicode(sciezkaplik+'\\'+str(godz)+'.mp3'))
      else: mp3=audio.Sound.open(unicode(sciezkaplik+'\\'+'24.mp3'))
     else: mp3=audio.Sound.open(unicode(sciezkaplik))
     if (int(ustaw[39:42])<int(ustaw[42:45]))and(int(godz)>=int(ustaw[39:42]))and(int(godz)<=int(ustaw[42:45])):mp3.play()
     elif (int(ustaw[39:42])>int(ustaw[42:45]))and((int(godz)>=int(ustaw[39:42]))or(int(godz)<=int(ustaw[42:45]))):mp3.play()
     elif int(godz)==int(ustaw[39:42]):mp3.play()
     audio.Sound.set_volume(mp3,int(audio.Sound.max_volume(mp3)*(float(int(ustaw[36:39]))/float(100))))
   if audio.Sound.state(mp3)<>2: mp3=0
   if (int(min)==0)and(int(sek)==0):
    if (int(ustaw[39:42])<int(ustaw[42:45]))and(int(godz)>=int(ustaw[39:42]))and(int(godz)<=int(ustaw[42:45])):miso.vibrate(500,100)
    elif (int(ustaw[39:42])>int(ustaw[42:45]))and((int(godz)>=int(ustaw[39:42]))or(int(godz)<=int(ustaw[42:45]))):miso.vibrate(500,100)
    elif int(godz)==int(ustaw[39:42]):miso.vibrate(500,100)
  except:pass
  if int(ustaw[18:21])==888: img.blit(ima,((0,0),(int(ustaw[0:3]),int(ustaw[3:6]))))
  else: img.rectangle([ (0,0),(int(ustaw[0:3]),int(ustaw[3:6]))],(int(ustaw[18:21]),int(ustaw[21:24]),int(ustaw[24:27])),fill=(int(ustaw[18:21]),int(ustaw[21:24]),int(ustaw[24:27])))
  if pb<>'None':
   img.line([(0,0),(0,int(ustaw[3:6]))],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   img.line([(-1+int(ustaw[0:3]),0),(-1+int(ustaw[0:3]),int(ustaw[3:6])) ],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
  if fpp[int(ustaw[56:57])]<>'None':
   img.line([(0,0),(0,4)],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   img.line([(0,0),(4,0)],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   img.line([(-1+int(ustaw[0:3]),0),(-1+int(ustaw[0:3]),4)],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   img.line([(-1+int(ustaw[0:3]),0),(-1-4+int(ustaw[0:3]),0)],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   img.line([(-1+int(ustaw[0:3]),-1+int(ustaw[3:6])),(-1-4+int(ustaw[0:3]),-1+int(ustaw[3:6]))],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   img.line([(-1+int(ustaw[0:3]),-1+int(ustaw[3:6])),(-1+int(ustaw[0:3]),-1-4+int(ustaw[3:6]))],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   img.line([(0,-1+int(ustaw[3:6])),(0,-1-4+int(ustaw[3:6]))],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   img.line([(0,-1+int(ustaw[3:6])),(4,-1+int(ustaw[3:6]))],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
  if ekran>0:
   e32.reset_inactivity()
   img.line([(0,-1+int(ustaw[3:6])),(int(ustaw[0:3]),-1+int(ustaw[3:6]))],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
  if ladow>0: img.line([(0,0),(int(ustaw[0:3]),0)],(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
  if int(ustaw[45:48])/10>0:
   if int(ustaw[45:48])/10==1: k=unicode(str(godz)+':'+str(min)+':'+str(sek))
   elif int(ustaw[45:48])/10==2: k=unicode('%02i'%(dz)+'.'+'%02i'%(mies)+'.'+str(rok))
   elif int(ustaw[45:48])/10==3: k=unicode('%06.3f'%(float(sysinfo.free_ram())/float(1000000)))
   elif int(ustaw[45:48])/10==4: k=unicode('%03i'%(sysinfo.signal_dbm())+' dBm')
   elif int(ustaw[45:48])/10==5: k=unicode('%03i'%(sysinfo.battery())+' %')
   if int(ustaw[45:48])%10==1:  
    q=(None,None,graphics.FONT_BOLD|graphics.FONT_ANTIALIAS)
   elif int(ustaw[45:48])%10==2:  
    q=(None,None,graphics.FONT_ITALIC|graphics.FONT_ANTIALIAS)
   elif int(ustaw[45:48])%10==3:  
    q=(None,None,graphics.FONT_BOLD|graphics.FONT_ITALIC|graphics.FONT_ANTIALIAS)
   else: q=(None,None,graphics.FONT_ANTIALIAS)
   img.text((int(ustaw[12:15]),int(ustaw[15:18])),k,font=q,fill=(int(ustaw[27:30]),int(ustaw[30:33]),int(ustaw[33:36])))
   screen.background_color=0xffffff
  else: screen.hide()

def pliki():
 global lista
 global sck
 global sciezkaplik
 global listbox
 index = listbox.current()
 if (lista[index][0]==u'[')and(lista[index][len(lista[index])-1]==u']'): lista[index]=lista[index][1:len(lista[index])-1]
 if lista[index]=='..':
  sciezka,plik=os.path.split(sciezkaplik)
  if plik <> '': sciezkaplik=sciezka
  pozycja()
 else:
  try: sciezkaplik=os.path.join(sciezkaplik,lista[index])
  except: pass
  sck=sciezkaplik
  wybierz()

def pozycja():
 global listbox
 global lista
 global sciezkaplik
 global sck
 index=listbox.current()
 if (lista[index][0]==u'[')and(lista[index][len(lista[index])-1]==u']'): lista[index]=lista[index][1:len(lista[index])-1]
 if lista[index]=='..':
  sciezka,plik=os.path.split(sciezkaplik)
  if plik <> '': sciezkaplik=sciezka
  else: 
   sciezkaplik=''
   lista=appuifw.e32.drive_list()
 else:
  if lista==appuifw.e32.drive_list(): sciezkaplik=os.path.join(sciezkaplik,lista[index]+'\\')
  else: sciezkaplik=os.path.join(sciezkaplik,lista[index])
 if os.path.isdir(sciezkaplik): 
  if sciezkaplik <> '':
   sciezka=os.listdir(sciezkaplik)
   lista=[u'..']
   for plik in sciezka:
    try: 
     if os.path.isdir(sciezkaplik+u'\\'+plik):
      lista.append(unicode('['+plik+']'))
    except: pass   
   for plik in sciezka:
    try: 
     if os.path.isfile(sciezkaplik+u'\\'+plik):
      nazwa,rozszerzenie=os.path.splitext(plik)
      if string.lower(rozszerzenie)=='.mp3': lista.append(unicode(plik))
      elif string.lower(rozszerzenie)=='.aac': lista.append(unicode(plik))
      elif string.lower(rozszerzenie)=='.wav': lista.append(unicode(plik))
      elif string.lower(rozszerzenie)=='.amr': lista.append(unicode(plik))
      elif string.lower(rozszerzenie)=='.mid': lista.append(unicode(plik))
      elif string.lower(rozszerzenie)=='.rng': lista.append(unicode(plik))
    except: pass
  appuifw.app.body=listbox=appuifw.Listbox(lista,pozycja)
  appuifw.app.menu=[(u'Choice',pliki)]
  appuifw.app.exit_key_handler=wybierz
 else: 
  sciezkaplik,plik=os.path.split(sciezkaplik)
  sck=sciezkaplik 
  pliki()

lista=[u' ']
appuifw.app.body = listbox = appuifw.Listbox(lista, wybierz)
appuifw.app.menu=[(u'Hide program',ukryj),(u'About',prog)]
appuifw.app.exit_key_handler=koniec
wybierz()
pasek()
