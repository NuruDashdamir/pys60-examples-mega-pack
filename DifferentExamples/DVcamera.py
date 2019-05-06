#by Shrim
import appuifw,os,e32
from graphics import*
from appuifw import*
from camera import*
from time import strftime
app.body=cs=Canvas()
app.screen,app.exit_key_handler='full',app.set_exit
wb,fm,mz,em,ca=white_balance_modes(),flash_modes(),max_zoom(),exposure_modes(),cameras_available()
def ru(x):
 t=x.decode('utf-8')
 return t
inf1,inf2,inf3=Image.new((176,13)),Image.new((8,120)),Image.new((176,75))
inf1.clear(0x000000),inf2.clear(0x000000),inf3.clear(0x000000)
inf1.text((55,12),u'DV Camera',fill=0x0000ff,font=u'latinbold12') 
inf3.text((3,12),ru('#1 вспышка:'),fill=0x0000ff,font=u'alp')
inf3.text((3,23),ru('#2 режимы:'),fill=0x0000ff,font=u'alp')
inf3.text((3,34),ru('#3 баланс белого:'),fill=0x0000ff,font=u'alp')
inf3.text((3,55),u'Zoom:',fill=0x0000ff,font=u'latinbold12')
f,z,e,w,p=0,0,0,3,0
def shop():
 foto=take_photo(mode='RGB',size=(1280,960),flash=fm[f],zoom=z,exposure=em[e],white_balance=wb[w],position=p)
 cs.text((3,205),ru('сохраняю снимок ...'),fill=0x0000ff,font=u'alp')
 name=strftime('%d%m%Y%H%M%S')
 foto.save('e:\\images\\'+name+'.png',bpp=24,quality=100),e32.ao_yield()
def zoomin():
 global z
 if z<mz:z+=1
def zoomout():
 global z
 if z>0:z-=1
def flas():
 global f
 if f<len(fm)-1:f+=1
 else:f=0
def expo():
 global e
 if e<len(em)-1:e+=1
 else:e=0
def white():
 global w
 if w<len(wb)-1:w+=1
 else:w=0
def pos():
 global p
 if p<ca-1:p+=1
 else:p=0
cs.bind(63557,shop),cs.bind(63497,zoomin),cs.bind(63498,zoomout),cs.bind(49,flas),cs.bind(50,expo),cs.bind(51,white),cs.bind(56,pos)
while 1:
 img=take_photo(size=(160,120),zoom=z,exposure=em[e],white_balance=wb[w],position=p)
 tim=strftime('%H:%M:%S')
 cs.blit(inf1),cs.blit(inf2,target=(0,13)),cs.blit(inf2,target=(168,13)),cs.blit(inf3,target=(0,133)),cs.blit(img,target=(8,13)),cs.text((100,145),unicode(fm[f]),fill=0x0000ff,font=u'alp'),cs.text((100,156),unicode(em[e]),fill=0x0000ff,font=u'alp'),cs.text((100,167),unicode(wb[w]),fill=0x0000ff,font=u'alp'),cs.text((45,188),unicode(z),fill=0x0000ff,font=u'acb14'),cs.text((115,205),unicode(tim),fill=0x0000ff,font=u'acb14'),e32.ao_yield()
