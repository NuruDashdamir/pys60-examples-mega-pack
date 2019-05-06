#created by Igor aka kAIST

import camera,time,thread,e32
from graphics import *
from appuifw import *
from audio import Sound
canvas=Canvas(event_callback=None, redraw_callback=None)
app.body=canvas
pt=0

def ru(x):return x.decode('utf-8')
app.title=ru('Семь нот')
_state=0
_null=[]
_prev=None
_path=u'e:\\System\\Apps\\RunPython\\Apps\\7not\\Sounds\\'
_sounds=[]
_notes=[ru('си'),ru('ля'),ru('соль'),ru('фа'),ru('ми'),ru('ре'),ru('до'),ru('нет')]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
def screen():
 s=Image.new((176,144))
 s.clear((0x7777ff))
 s.text((60,25),ru('7  н о т'),font='title')
 s.text((10,45),ru('автор: Игорь аka kAIST'))
 s.text((10,58),ru('e-mail: igor.kaist@gmail.com'))
 s.text((10,70),ru('ICQ:211141235'))
 s.text((40,110),ru('идет загрузка...'),0xffffff)
 canvas.blit(s)
 e32.ao_sleep(2)
screen()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
try:
 g=open('e:/System/Apps/7not/sens.dat','rb')
 x=g.read() 
 _sens=int(x)
except:_sens=300

for w in range(0,7):
 p=Sound.open(_path+str(w)+u'.amr')
 _sounds.append(p)

def state():
 global _state
 e32.ao_sleep(5)
 _state=1
 return 1

def sum(photo,x,y):
 de=0
 for b in [(0,0),(2,0),(1,4),(0,6),(2,6)]:
  a=photo.getpixel((x+b[0],y+b[1]))
  de=de+a[0][0]+a[0][1]+a[0][2]
 return de

def detector(photo):
 a=[20,40,60,80,100,120,140]
 b=[]
 for x in range(0,7):
  photo.rectangle((a[x]-1,124,a[x]+3,132),0xff0000)
  b.append(sum(photo,a[x],125))
 return b

def otrabotka(mass):
 global _null,_sens
 for x in range(0,7):
  if _null[x]-mass[x]>_sens:return x


def go(number):
 global _prev,_sounds
 if number<>None and number<>_prev:
  try:
   _sounds[6-number].play()
   e32.ao_sleep(0.05)
  except:pass
 if number==None:
  try:_sounds[6-_prev].stop()
  except:pass
 _prev=number

def main(photo):
 global canvas,pt,_state,_null,_notes
 d=time.clock()*100
 z=int(100/(d-pt))
 pt=d
 if _state:
  photo.text((2,23),'готово к игре'.decode('utf-8'),0xffffff)
  rez=otrabotka(detector(photo))
  go(rez)
  if rez==None:rez1=7
  else:rez1=rez
  photo.text((2,40),ru('нота: ')+_notes[rez1],0xffffff)

 else:
  photo.text((2,23),'подготовка к игре'.decode('utf-8'),0xffffff)
  _null= detector(photo)

   
 photo.text((2,13),u'fps '+str(z).decode('utf-8'),0xffffff)
 canvas.blit(photo,target=(0,0))

def reload():
 global _state
 try:camera.stop_finder()
 except:pass
 screen()
 _state=0
 thread.start_new_thread(state,())
 camera.start_finder(main)

def senset():
 global _sens
 x=query(ru('Чувствительность:'),'number',_sens)
 _sens=x
 m=open('e:/System/Apps/7not/sens.dat','w') 
 m.write(str(x))
 m.close()


app.menu=[(ru('перезапуск'),reload),(ru('чувствительность'),senset)]
reload()
