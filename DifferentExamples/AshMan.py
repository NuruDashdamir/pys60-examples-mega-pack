#uid: 0x27462610
#name: AshMan.py

def _level(l):
 global x,y,field,x1,x2,y1,y2,ai1_pos,ai2_pos,ai3_pos,ai4_pos,ai1_x1,ai1_x2,ai1_y1,ai1_y2,ai2_x1,ai2_x2,ai2_y1,ai2_y2,ai3_x1,ai3_x2,ai3_y1,ai3_y2,ai4_x1,ai4_x2,ai4_y1,ai4_y2,ai1_vect,ai2_vect,ai3_vect,ai4_vect,pos,rot,vect

 x = [0,22,44,66,88,110,132,154,176]
 y = [0,26,52,78,104,130,156,182,208]
 rot=1
 vect='down'

 if l==1:
  field = [
   1,1,1,1,1,1,1,1,
   1,2,2,2,2,2,2,1,
   1,2,1,1,1,1,2,1,
   1,2,0,1,1,1,2,1,
   1,2,1,1,1,2,2,1,
   1,2,1,1,1,1,2,1,
   1,2,2,2,2,2,2,1,
   1,1,1,1,1,1,1,1]
  x1,y1,x2,y2 = x[2],y[3],x[3],y[4]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[6],y[1],x[7],y[2]
  ai1_pos=14
  ai2_pos,ai3_pos,ai4_pos=64,64,64
  ai1_vect='left'
  pos=26

 if l==2:
  field = [
   2,2,2,2,2,2,2,2,
   0,1,2,1,1,2,1,2,
   2,1,2,2,2,2,1,2,
   2,1,2,1,1,2,1,2,
   2,1,2,1,1,2,1,2,
   2,1,2,2,2,2,1,2,
   2,1,2,1,1,2,1,2,
   2,2,2,2,2,2,2,2]
  x1,y1,x2,y2 = x[0],y[1],x[1],y[2]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[7],y[0],x[8],y[1]
  ai2_x1,ai2_y1,ai2_x2,ai2_y2 = x[0],y[7],x[1],y[8]
  ai1_pos,ai2_pos=7,56
  ai3_pos,ai4_pos=64,64
  ai1_vect='left'
  ai2_vect='right'
  pos=8

 if l==3:
  field = [
   2,2,2,2,1,2,2,0,
   2,1,1,2,2,2,1,2,
   2,1,1,2,1,1,2,2,
   2,2,2,2,2,1,2,1,
   1,2,1,2,2,2,2,2,
   2,2,1,1,2,1,1,2,
   2,1,2,2,2,1,1,2,
   2,2,2,1,2,2,2,2]
  x1,y1,x2,y2 = x[7],y[0],x[8],y[1]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[0],y[0],x[1],y[1]
  ai2_x1,ai2_y1,ai2_x2,ai2_y2 = x[7],y[7],x[8],y[8]
  ai1_pos,ai2_pos=0,63
  ai3_pos,ai4_pos=64,64
  ai1_vect='down'
  ai2_vect='up'
  pos=7

 if l==4:
  field = [
   0,1,2,2,2,2,2,2,
   2,1,2,1,1,2,1,2,
   2,1,2,2,2,2,1,2,
   2,1,2,1,1,2,1,2,
   2,1,2,1,1,2,1,2,
   2,1,2,2,2,2,1,2,
   2,1,2,1,1,2,1,2,
   2,2,2,2,2,2,1,2]
  x1,y1,x2,y2 = x[0],y[0],x[1],y[1]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[2],y[0],x[3],y[1]
  ai2_x1,ai2_y1,ai2_x2,ai2_y2 = x[5],y[7],x[6],y[8]
  ai1_pos,ai2_pos=2,61
  ai3_pos,ai4_pos=64,64
  ai1_vect='down'
  ai2_vect='up'
  pos=0

 if l==5:
  field = [
   2,2,2,2,2,2,2,2,
   2,1,2,1,1,2,1,2,
   2,1,0,2,2,2,1,2,
   2,1,1,1,1,1,1,2,
   2,1,1,2,2,1,1,2,
   2,2,2,2,2,2,2,2,
   2,1,1,1,1,1,1,2,
   2,2,2,2,2,2,2,2]
  x1,y1,x2,y2 = x[2],y[2],x[3],y[3]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[0],y[3],x[1],y[4]
  ai2_x1,ai2_y1,ai2_x2,ai2_y2 = x[7],y[2],x[8],y[3]
  ai3_x1,ai3_y1,ai3_x2,ai3_y2 = x[0],y[7],x[1],y[8]
  ai1_pos,ai2_pos=24,23
  ai3_pos,ai4_pos=56,64
  ai1_vect='down'
  ai2_vect='up'
  ai3_vect='right'
  pos=18

 if l==6:
  field = [
   0,2,2,2,2,2,2,2,
   1,1,1,1,1,1,1,2,
   2,2,2,2,2,2,2,2,
   2,1,2,1,1,1,1,2,
   2,1,1,1,1,2,1,2,
   2,2,2,2,2,2,2,2,
   2,1,1,1,1,1,1,1,
   2,2,2,2,2,2,2,2]
  x1,y1,x2,y2 = x[0],y[0],x[1],y[1]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[3],y[2],x[4],y[3]
  ai2_x1,ai2_y1,ai2_x2,ai2_y2 = x[0],y[5],x[1],y[6]
  ai3_x1,ai3_y1,ai3_x2,ai3_y2 = x[7],y[5],x[8],y[6]
  ai1_pos,ai2_pos=19,40
  ai3_pos,ai4_pos=47,64
  ai1_vect='left'
  ai2_vect='right'
  ai3_vect='up'
  pos=0

 if l==7:
  field = [
   1,1,2,2,2,2,1,1,
   1,1,1,2,2,1,1,1,
   0,1,2,2,2,2,1,2,
   2,2,2,0,0,2,2,2,
   2,2,2,0,0,2,2,2,
   2,1,2,2,2,2,1,2,
   1,1,1,2,2,1,1,1,
   1,1,2,2,2,2,1,1]
  x1,y1,x2,y2 = x[0],y[2],x[1],y[3]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[0],y[3],x[1],y[4]
  ai2_x1,ai2_y1,ai2_x2,ai2_y2 = x[4],y[7],x[5],y[8]
  ai3_x1,ai3_y1,ai3_x2,ai3_y2 = x[7],y[4],x[8],y[5]
  ai4_x1,ai4_y1,ai4_x2,ai4_y2 = x[3],y[0],x[4],y[1]
  ai1_pos,ai2_pos,ai3_pos,ai4_pos=24,60,39,3
  ai1_vect='right'
  ai2_vect='up'
  ai3_vect='left'
  ai4_vect='down'
  pos=16

 if l==8:
  field = [
   2,2,2,2,2,2,2,2,
   2,1,1,2,2,1,1,2,
   2,0,1,2,2,2,2,2,
   2,1,1,2,2,1,1,2,
   2,1,1,2,2,1,1,2,
   2,2,2,2,2,1,2,2,
   2,1,1,2,2,1,1,2,
   2,2,2,2,2,2,2,2]
  x1,y1,x2,y2 = x[1],y[2],x[2],y[3]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[0],y[0],x[1],y[1]
  ai2_x1,ai2_y1,ai2_x2,ai2_y2 = x[3],y[7],x[4],y[8]
  ai3_x1,ai3_y1,ai3_x2,ai3_y2 = x[7],y[0],x[8],y[1]
  ai4_x1,ai4_y1,ai4_x2,ai4_y2 = x[4],y[7],x[5],y[8]
  ai1_pos,ai2_pos,ai3_pos,ai4_pos=0,59,7,60
  ai1_vect='down'
  ai2_vect='up'
  ai3_vect='left'
  ai4_vect='right'
  pos=17

 if l==9:
  field = [
   2,2,2,2,2,2,2,2,
   2,1,1,2,2,1,1,2,
   2,1,0,2,2,1,1,2,
   2,2,2,2,2,2,2,2,
   2,2,2,2,2,2,2,2,
   2,1,1,2,2,2,1,2,
   2,1,1,2,2,1,1,2,
   2,2,2,2,2,2,2,2]
  x1,y1,x2,y2 = x[2],y[2],x[3],y[3]
  ai1_x1,ai1_y1,ai1_x2,ai1_y2 = x[0],y[0],x[1],y[1]
  ai2_x1,ai2_y1,ai2_x2,ai2_y2 = x[0],y[7],x[1],y[8]
  ai3_x1,ai3_y1,ai3_x2,ai3_y2 = x[7],y[7],x[8],y[8]
  ai4_x1,ai4_y1,ai4_x2,ai4_y2 = x[7],y[0],x[8],y[1]
  ai1_pos,ai2_pos,ai3_pos,ai4_pos=0,56,63,7
  ai1_vect='down'
  ai2_vect='up'
  ai3_vect='up'
  ai4_vect='down'
  pos=18

import keycapture,os
from appuifw import *
from graphics import *
from e32 import *

sleep = ao_sleep
app.screen = 'full'

path = os.path.split(app.full_name())[0]
level = os.path.join(path,u'level.lvl')
def _load():
 try:
  if os.path.exists(level)==1:
   f=open(level,'rb')
   f.seek(3)
   level_numb=int(f.read())
   f.close()
   return level_numb
 except:note(u'You dont have a saved game!','error')
img = Image.new((176,208))

def _redraw():
  can.blit(img)  

app.body = can = Canvas(event_callback=None,redraw_callback=_redraw)

def _intro():
 app.exit_key_handler=_menu
 color = [(153,204,255),(103,154,201),(53,100,155),(3,49,97),(0,0,0)]
 color_text = [(0,0,0),(3,49,97),(53,100,155),(103,154,201),(153,204,255)]
 for y in range(20):
  img.clear(0)
  img.rectangle((0,190-(y*10),176,208-(y*10)), 0x99ccff, fill=0x99ccff)
  _redraw()
  sleep(0.02)
 for blink in range(20):
  img.clear(0)
  img.rectangle((0,0,176,18), 0x99ccff, fill=0x99ccff)
  img.text((5,12),u'created by Ash_Rockit',color[blink/4])
  _redraw()
  sleep(0.03)
 sleep(1)
 for y in range(20):
  img.clear(0)
  img.rectangle((0,0,176,18+(y*10)), 0x99ccff, fill=color[y/4])
  _redraw()
  sleep(0.02)
 _menu()

menu_text_c = ['NEW GAME',
 'LOAD',
 'ABOUT',
 'EXIT']
menu_text = ['New game',
 'Load',
 'About',
 'Exit']

break_menu=0
run_ = 0
cursor_pos=0
y_cursor = 120

def _menu_down():
   global cursor_pos
   if cursor_pos < 3: cursor_pos += 1
   else: cursor_pos = 0

def _menu_up():
   global cursor_pos
   if cursor_pos > 0: cursor_pos -= 1
   else: cursor_pos = 3

def _menu_enter():
 global break_menu,run_,level_
 if cursor_pos == 0:
  f=open(level,'wb')
  f.write('\x00\xff\x581')
  f.close()
  level_ = 1
  _level(level_)
  run_ = 1
  _run()
 if cursor_pos == 1:
  level_=_load()
  _level(level_)
  run_ = 1
  _run()
 if cursor_pos == 2: _about()
 if cursor_pos == 3:
  os.abort()

def _about():
 can.bind(63497,lambda: None)
 can.bind(63498,lambda: None)
 can.bind(63557,lambda: None)
 can.bind(50,lambda: None)
 can.bind(56,lambda: None)
 app.exit_key_handler=_menu
 img.clear(0)
 img.rectangle((0,0,176,208), 0x99ccff)
 img.text((25,100),u'congratulation', 0xff0000)
 img.text((40,150),u'you win', 0xff0000)
 img.text((19,200),u'to be continued...', 0xffff00)
 _redraw()
 sleep(3)
 _menu()

def _about():
 can.bind(63497,lambda: None)
 can.bind(63498,lambda: None)
 can.bind(63557,lambda: None)
 can.bind(50,lambda: None)
 can.bind(56,lambda: None)
 app.exit_key_handler=_menu
 name='AshMan Adventures'
 me=' > created by Ash_Rockit'
 icq=' > icq: 448060955'
 mail=' > e-mail: ash_dump@mail.ru'
 ay=130
 text=''
 text2=''
 text3=''
 text4=''
 for a in name:
   img.clear(0)
   img.rectangle((0,0,176,208), 0x99ccff)
   img.ellipse((65,10,170,115), 0xffff00, fill=0xffff00)
   img.ellipse((75,30,100,55), 0, fill=0)
   img.ellipse((115,28,145,58), 0, fill=0)
   img.line((80,92,135,92), 0, width=3)
   text+=a
   img.text((10,ay),unicode(text),0x66ff66)
   img.text((2,200),u'(c)', 0xffff00)
   img.text((19,200),u'AshMan created by Ash_Rockit', 0xff0000)
   _redraw()
   sleep(0.1)
 ay+=17
 for a in me:
   img.clear(0)
   img.rectangle((0,0,176,208), 0x99ccff)
   img.ellipse((65,10,170,115), 0xffff00, fill=0xffff00)
   img.ellipse((75,30,100,55), 0, fill=0)
   img.ellipse((115,28,145,58), 0, fill=0)
   img.line((80,92,135,92), 0, width=3)
   text2+=a
   img.text((10,ay-17),unicode(text),0x66ff66)
   img.text((10,ay),unicode(text2),0x777777)
   img.text((2,200),u'(c)', 0xffff00)
   img.text((19,200),u'AshMan created by Ash_Rockit', 0xff0000)
   _redraw()
   sleep(0.1)
 ay+=17
 for a in icq:
   img.clear(0)
   img.rectangle((0,0,176,208), 0x99ccff)
   img.ellipse((65,10,170,115), 0xffff00, fill=0xffff00)
   img.ellipse((75,30,100,55), 0, fill=0)
   img.ellipse((115,28,145,58), 0, fill=0)
   img.line((80,92,135,92), 0, width=3)
   text3+=a
   img.text((10,ay-34),unicode(text),0x66ff66)
   img.text((10,ay-17),unicode(text2),0x777777)
   img.text((10,ay),unicode(text3),0x777777)
   img.text((2,200),u'(c)', 0xffff00)
   img.text((19,200),u'AshMan created by Ash_Rockit', 0xff0000)
   _redraw()
   sleep(0.1)
 ay+=17
 for a in mail:
   img.clear(0)
   img.rectangle((0,0,176,208), 0x99ccff)
   img.ellipse((65,10,170,115), 0xffff00, fill=0xffff00)
   img.ellipse((75,30,100,55), 0, fill=0)
   img.ellipse((115,28,145,58), 0, fill=0)
   img.line((80,92,135,92), 0, width=3)
   text4+=a
   img.text((10,ay-51),unicode(text),0x66ff66)
   img.text((10,ay-34),unicode(text2),0x777777)
   img.text((10,ay-17),unicode(text3),0x777777)
   img.text((10,ay),unicode(text4),0x777777)
   img.text((2,200),u'(c)', 0xffff00)
   img.text((19,200),u'AshMan created by Ash_Rockit', 0xff0000)
   _redraw()
   sleep(0.1)
 while 1:
   img.clear(0)
   img.rectangle((0,0,176,208), 0x99ccff)
   img.ellipse((65,10,170,115), 0xffff00, fill=0xffff00)
   img.ellipse((75,30,100,55), 0, fill=0)
   img.ellipse((115,28,145,58), 0, fill=0)
   img.line((80,92,135,92), 0, width=3)
   img.text((10,ay-51),unicode(text),0x66ff66)
   img.text((10,ay-34),unicode(text2),0x777777)
   img.text((10,ay-17),unicode(text3),0x777777)
   img.text((10,ay),unicode(text4),0x777777)
   img.text((2,200),u'(c)', 0xffff00)
   img.text((19,200),u'AshMan created by Ash_Rockit', 0xff0000)
   _redraw()
   sleep(0.1)

def _menu():
 can.bind(63497,lambda:_menu_up())
 can.bind(63498,lambda:_menu_down())
 can.bind(63557,lambda:_menu_enter())
 can.bind(50,lambda:_menu_up())
 can.bind(56,lambda:_menu_down())
 if run_== 1:
  app.exit_key_handler=_run
  try:
   f=open(level,'wb')
   f.write('\x00\xff\x58'+str(level_))
   f.close()
  except: note(u'Game not save :(','error')
 else: app.exit_key_handler=os.abort
 while 1:
  img.clear(0)
  img.rectangle((0,0,176,208), 0x99ccff)
  img.ellipse((65,10,170,115), 0xffff00, fill=0xffff00)
  img.ellipse((75,30,100,55), 0, fill=0)
  img.ellipse((115,28,145,58), 0, fill=0)
  img.line((80,92,135,92), 0, width=3)
  img.rectangle((10,y_cursor+(15*cursor_pos),156,y_cursor+(15*(cursor_pos+1))), 0x99ccff, fill=(103,154,201))
  for a in range(0,4):
    if a == cursor_pos:
      img.text((25,132+((a)*15)),unicode(menu_text_c[a]), 0x000000)
    else:
      img.text((20,132+((a)*15)),unicode(menu_text[a]), (103,154,201))
  img.text((2,200),u'(c)', 0xffff00)
  img.text((19,200),u'AshMan created by Ash_Rockit', 0xff0000)
  _redraw()
  sleep(0.08)

def _left():
  global x1,y1,x2,y2,pos,vect,field
  if x1 > 0:
   if pos-1 >= 0:
    if (field[pos-1]==0) or (field[pos-1]==2):
     x1 -= 22
     x2 -= 22
     pos -= 1
     for y_pos in range(0,8):
      for x_pos in range(0,8):  
       if ((y_pos*8)+x_pos) == pos:
        if field[(y_pos*8)+x_pos] == 2:
         field[(y_pos*8)+x_pos] = 0
  vect = 'left'

def _right():
  global x1,y1,x2,y2,pos,vect,field
  if x2 < 176:
   if pos+1 <= 63:
    if (field[pos+1]==0) or (field[pos+1]==2):
     x1 += 22
     x2 += 22
     pos += 1
     for y_pos in range(0,8):
      for x_pos in range(0,8):  
       if ((y_pos*8)+x_pos) == pos:
        if field[(y_pos*8)+x_pos] == 2:
         field[(y_pos*8)+x_pos] = 0
  vect = 'right'

def _up():
  global x1,y1,x2,y2,pos,vect,field
  if y1 > 0:
   if pos-8 >= 0:
    if (field[pos-8]==0) or (field[pos-8]==2):
     y1 -= 26
     y2 -= 26
     pos -= 8
     for y_pos in range(0,8):
      for x_pos in range(0,8):  
       if ((y_pos*8)+x_pos) == pos:
        if field[(y_pos*8)+x_pos] == 2:
         field[(y_pos*8)+x_pos] = 0
  vect = 'up'

def _down():
  global x1,y1,x2,y2,pos,vect,field
  if y2 < 208:
   if pos+8 <= 63:
    if (field[pos+8]==0) or (field[pos+8]==2):
     y1 += 26
     y2 += 26
     pos += 8
     for y_pos in range(0,8):
      for x_pos in range(0,8):  
       if ((y_pos*8)+x_pos) == pos:
        if field[(y_pos*8)+x_pos] == 2:
         field[(y_pos*8)+x_pos] = 0
  vect = 'down'

def _kolobok():
  global rot
  if vect == 'right':
   if rot == 0:
    img.ellipse((x1+1,y1+3,x2-1,y2-3),0xffff00,fill=0xffff00,)
    img.line((x2-12,y2-12,x2-1,y2-12),0x000000,width=1)
    img.point((x2-9,y1+8), 0x000000,width=4)
    rot = 1
   else:
    img.pieslice((x1+1,y1+3,x2-1,y2-3), 0.6, 5.6,0xffff00,fill=0xffff00,)
    img.point((x2-10,y1+6), 0x000000,width=4)
    rot = 0

  if vect == 'left':
   if rot == 0:
    img.ellipse((x1+1,y1+3,x2-1,y2-3),0xffff00,fill=0xffff00,)
    img.line((x1+1,y2-12,x1+11,y2-12),0x000000,width=1)
    img.point((x1+8,y1+8), 0x000000,width=4)
    rot = 1
   else:
    img.pieslice((x1+1,y1+3,x2-1,y2-3), 4.1, 2.5, 0xffff00,fill=0xffff00,)
    img.point((x1+8,y1+6), 0x000000,width=4)
    rot = 0

  if vect == 'down':
    img.ellipse((x1+1,y1+3,x2-1,y2-3),0xffff00,fill=0xffff00,)
    img.line((x1+1,y2-11,x2-1,y2-11),0x000000,width=1)
    img.point((x1+7,y1+8), 0x000000,width=4)
    img.point((x2-9,y1+8), 0x000000,width=4)

  if vect == 'up':
    img.ellipse((x1+1,y1+3,x2-1,y2-3),0xffff00,fill=0xffff00,)
    img.line((x1+10,y1+3,x1+10,y1+13),0x000000,width=1)
    img.line((x1+14,y1+3,x1+14,y1+13),0x000000,width=1)
    img.line((x1+6,y1+3,x1+6,y1+13),0x000000,width=1)

def _ai():
 global ai1_pos,ai2_pos,ai3_pos,ai4_pos,ai1_x1,ai1_x2,ai1_y1,ai1_y2,ai2_x1,ai2_x2,ai2_y1,ai2_y2,ai3_x1,ai3_x2,ai3_y1,ai3_y2,ai4_x1,ai4_x2,ai4_y1,ai4_y2,ai1_vect,ai2_vect,ai3_vect,ai4_vect

 if level_ == 1:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='down':
    if ai1_y2 < y[7]:
      ai1_y1 += 26
      ai1_y2 += 26
      ai1_pos += 8
    else: ai1_vect='right'
   if ai1_vect=='right':
    if ai1_x2 < x[7]:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='up'
   if ai1_vect=='up':
    if ai1_y1 > y[1]:
      ai1_y1 -= 26
      ai1_y2 -= 26
      ai1_pos -= 8
    else: ai1_vect='left'
   if ai1_vect=='left':
    if ai1_x1 > x[1]:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='down'
# ^ enemy one animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

 if level_ == 2:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='left':
    if ai1_pos > 0:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='right'
   if ai1_vect=='right':
    if ai1_pos < 7:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='left'
# ^ enemy one animation

  if ai2_y2 < 208 or ai2_y1 > 0 or ai2_x1 > 0 or ai2_x2 < 176:
   if ai2_vect=='left':
    if ai2_pos > 56:
      ai2_x1 -= 22
      ai2_x2 -= 22
      ai2_pos -= 1
    else: ai2_vect='right'
   if ai2_vect=='right':
    if ai2_pos < 63:
      ai2_x1 += 22
      ai2_x2 += 22
      ai2_pos += 1
    else: ai2_vect='left'
# ^ enemy two animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

  img.ellipse((ai2_x1+1,ai2_y1+3,ai2_x2-1,ai2_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai2_x1+7,ai2_y1+8), 0x000000,width=4)
  img.point((ai2_x2-9,ai2_y1+8), 0x000000,width=4)

 if level_ == 3:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='down':
    if ai1_y2 < y[4]:
      ai1_y1 += 26
      ai1_y2 += 26
      ai1_pos += 8
    else: ai1_vect='right'
   if ai1_vect=='right':
    if ai1_x2 < x[4]:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='up'
   if ai1_vect=='up':
    if ai1_y1 > 0:
      ai1_y1 -= 26
      ai1_y2 -= 26
      ai1_pos -= 8
    else: ai1_vect='left'
   if ai1_vect=='left':
    if ai1_x1 > 0:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='down'
# ^ enemy one animation

  if ai2_y2 < 208 or ai2_y1 > 0 or ai2_x1 > 0 or ai2_x2 < 176:
   if ai2_vect=='down':
    if ai2_y2 < 208:
      ai2_y1 += 26
      ai2_y2 += 26
      ai2_pos += 8
    else: ai2_vect='right'
   if ai2_vect=='right':
    if ai2_x2 < 176:
      ai2_x1 += 22
      ai2_x2 += 22
      ai2_pos += 1
    else: ai2_vect='up'
   if ai2_vect=='up':
    if ai2_y1 > y[4]:
      ai2_y1 -= 26
      ai2_y2 -= 26
      ai2_pos -= 8
    else: ai2_vect='left'
   if ai2_vect=='left':
    if ai2_x1 > x[4]:
      ai2_x1 -= 22
      ai2_x2 -= 22
      ai2_pos -= 1
    else: ai2_vect='down'
# ^ enemy two animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

  img.ellipse((ai2_x1+1,ai2_y1+3,ai2_x2-1,ai2_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai2_x1+7,ai2_y1+8), 0x000000,width=4)
  img.point((ai2_x2-9,ai2_y1+8), 0x000000,width=4)

 if level_ == 4:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='down':
    if ai1_y2 < 208:
      ai1_y1 += 26
      ai1_y2 += 26
      ai1_pos += 8
    else: ai1_vect='right'
   if ai1_vect=='right':
    if ai1_x2 < x[6]:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='up'
   if ai1_vect=='up':
    if ai1_y1 > 0:
      ai1_y1 -= 26
      ai1_y2 -= 26
      ai1_pos -= 8
    else: ai1_vect='left'
   if ai1_vect=='left':
    if ai1_x1 > x[2]:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='down'
# ^ enemy one animation

  if ai2_y2 < 208 or ai2_y1 > 0 or ai2_x1 > 0 or ai2_x2 < 176:
   if ai2_vect=='down':
    if ai2_y2 < 208:
      ai2_y1 += 26
      ai2_y2 += 26
      ai2_pos += 8
    else: ai2_vect='right'
   if ai2_vect=='right':
    if ai2_x2 < x[6]:
      ai2_x1 += 22
      ai2_x2 += 22
      ai2_pos += 1
    else: ai2_vect='up'
   if ai2_vect=='up':
    if ai2_y1 > 0:
      ai2_y1 -= 26
      ai2_y2 -= 26
      ai2_pos -= 8
    else: ai2_vect='left'
   if ai2_vect=='left':
    if ai2_x1 > x[2]:
      ai2_x1 -= 22
      ai2_x2 -= 22
      ai2_pos -= 1
    else: ai2_vect='down'
# ^ enemy two animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

  img.ellipse((ai2_x1+1,ai2_y1+3,ai2_x2-1,ai2_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai2_x1+7,ai2_y1+8), 0x000000,width=4)
  img.point((ai2_x2-9,ai2_y1+8), 0x000000,width=4)

 if level_ == 5:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='down':
    if ai1_y2 < y[6]:
      ai1_y1 += 26
      ai1_y2 += 26
      ai1_pos += 8
    else: ai1_vect='right'
   if ai1_vect=='right':
    if ai1_x2 < 176:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='up'
   if ai1_vect=='up':
    if ai1_y1 > 0:
      ai1_y1 -= 26
      ai1_y2 -= 26
      ai1_pos -= 8
    else: ai1_vect='left'
   if ai1_vect=='left':
    if ai1_x1 > 0:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='down'
# ^ enemy one animation

  if ai2_y2 < 208 or ai2_y1 > 0 or ai2_x1 > 0 or ai2_x2 < 176:
   if ai2_vect=='down':
    if ai2_y2 < y[6]:
      ai2_y1 += 26
      ai2_y2 += 26
      ai2_pos += 8
    else: ai2_vect='right'
   if ai2_vect=='right':
    if ai2_x2 < 176:
      ai2_x1 += 22
      ai2_x2 += 22
      ai2_pos += 1
    else: ai2_vect='up'
   if ai2_vect=='up':
    if ai2_y1 > 0:
      ai2_y1 -= 26
      ai2_y2 -= 26
      ai2_pos -= 8
    else: ai2_vect='left'
   if ai2_vect=='left':
    if ai2_x1 > 0:
      ai2_x1 -= 22
      ai2_x2 -= 22
      ai2_pos -= 1
    else: ai2_vect='down'
# ^ enemy two animation

  if ai3_y2 < 208 or ai3_y1 > 0 or ai3_x1 > 0 or ai3_x2 < 176:
   if ai3_vect=='down':
    if ai3_y2 < 208:
      ai3_y1 += 26
      ai3_y2 += 26
      ai3_pos += 8
    else: ai3_vect='right'
   if ai3_vect=='right':
    if ai3_x2 < 176:
      ai3_x1 += 22
      ai3_x2 += 22
      ai3_pos += 1
    else: ai3_vect='up'
   if ai3_vect=='up':
    if ai3_y1 > y[5]:
      ai3_y1 -= 26
      ai3_y2 -= 26
      ai3_pos -= 8
    else: ai3_vect='left'
   if ai3_vect=='left':
    if ai3_x1 > 0:
      ai3_x1 -= 22
      ai3_x2 -= 22
      ai3_pos -= 1
    else: ai3_vect='down'
# ^ enemy 3 animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

  img.ellipse((ai2_x1+1,ai2_y1+3,ai2_x2-1,ai2_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai2_x1+7,ai2_y1+8), 0x000000,width=4)
  img.point((ai2_x2-9,ai2_y1+8), 0x000000,width=4)

  img.ellipse((ai3_x1+1,ai3_y1+3,ai3_x2-1,ai3_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai3_x1+7,ai3_y1+8), 0x000000,width=4)
  img.point((ai3_x2-9,ai3_y1+8), 0x000000,width=4)

 if level_ == 6:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='down':
    if ai1_y2 < x[6]:
      ai1_y1 += 26
      ai1_y2 += 26
      ai1_pos += 8
    else: ai1_vect='right'
   if ai1_vect=='right':
    if ai1_x2 < 176:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='up'
   if ai1_vect=='up':
    if ai1_y1 > y[2]:
      ai1_y1 -= 26
      ai1_y2 -= 26
      ai1_pos -= 8
    else: ai1_vect='left'
   if ai1_vect=='left':
    if ai1_x1 > 0:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='down'
# ^ enemy one animation

  if ai2_y2 < 208 or ai2_y1 > 0 or ai2_x1 > 0 or ai2_x2 < 176:
   if ai2_vect=='down':
    if ai2_y2 < y[6]:
      ai2_y1 += 26
      ai2_y2 += 26
      ai2_pos += 8
    else: ai2_vect='right'
   if ai2_vect=='right':
    if ai2_x2 < 176:
      ai2_x1 += 22
      ai2_x2 += 22
      ai2_pos += 1
    else: ai2_vect='up'
   if ai2_vect=='up':
    if ai2_y1 > y[2]:
      ai2_y1 -= 26
      ai2_y2 -= 26
      ai2_pos -= 8
    else: ai2_vect='left'
   if ai2_vect=='left':
    if ai2_x1 > 0:
      ai2_x1 -= 22
      ai2_x2 -= 22
      ai2_pos -= 1
    else: ai2_vect='down'
# ^ enemy two animation

  if ai3_y2 < 208 or ai3_y1 > 0 or ai3_x1 > 0 or ai3_x2 < 176:
   if ai3_vect=='down':
    if ai3_y2 < y[6]:
      ai3_y1 += 26
      ai3_y2 += 26
      ai3_pos += 8
    else: ai3_vect='right'
   if ai3_vect=='right':
    if ai3_x2 < 176:
      ai3_x1 += 22
      ai3_x2 += 22
      ai3_pos += 1
    else: ai3_vect='up'
   if ai3_vect=='up':
    if ai3_y1 > y[2]:
      ai3_y1 -= 26
      ai3_y2 -= 26
      ai3_pos -= 8
    else: ai3_vect='left'
   if ai3_vect=='left':
    if ai3_x1 > 0:
      ai3_x1 -= 22
      ai3_x2 -= 22
      ai3_pos -= 1
    else: ai3_vect='down'
# ^ enemy 3 animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

  img.ellipse((ai2_x1+1,ai2_y1+3,ai2_x2-1,ai2_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai2_x1+7,ai2_y1+8), 0x000000,width=4)
  img.point((ai2_x2-9,ai2_y1+8), 0x000000,width=4)

  img.ellipse((ai3_x1+1,ai3_y1+3,ai3_x2-1,ai3_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai3_x1+7,ai3_y1+8), 0x000000,width=4)
  img.point((ai3_x2-9,ai3_y1+8), 0x000000,width=4)

 if level_ == 7:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='right':
    if ai1_x2 < 176:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='left'
   if ai1_vect=='left':
    if ai1_x1 > 0:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='right'
# ^ enemy 1 animation

  if ai2_y2 < 208 or ai2_y1 > 0 or ai2_x1 > 0 or ai2_x2 < 176:
   if ai2_vect=='down':
    if ai2_y2 < 208:
      ai2_y1 += 26
      ai2_y2 += 26
      ai2_pos += 8
    else: ai2_vect='up'
   if ai2_vect=='up':
    if ai2_y1 > 0:
      ai2_y1 -= 26
      ai2_y2 -= 26
      ai2_pos -= 8
    else: ai2_vect='down'
# ^ enemy 2 animation

  if ai3_y2 < 208 or ai3_y1 > 0 or ai3_x1 > 0 or ai3_x2 < 176:
   if ai3_vect=='right':
    if ai3_x2 < 176:
      ai3_x1 += 22
      ai3_x2 += 22
      ai3_pos += 1
    else: ai3_vect='left'
   if ai3_vect=='left':
    if ai3_x1 > 0:
      ai3_x1 -= 22
      ai3_x2 -= 22
      ai3_pos -= 1
    else: ai3_vect='right'
# ^ enemy 3 animation

  if ai4_y2 < 208 or ai4_y1 > 0 or ai4_x1 > 0 or ai4_x2 < 176:
   if ai4_vect=='down':
    if ai4_y2 < 208:
      ai4_y1 += 26
      ai4_y2 += 26
      ai4_pos += 8
    else: ai4_vect='up'
   if ai4_vect=='up':
    if ai4_y1 > 0:
      ai4_y1 -= 26
      ai4_y2 -= 26
      ai4_pos -= 8
    else: ai4_vect='down'
# ^ enemy 4 animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

  img.ellipse((ai2_x1+1,ai2_y1+3,ai2_x2-1,ai2_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai2_x1+7,ai2_y1+8), 0x000000,width=4)
  img.point((ai2_x2-9,ai2_y1+8), 0x000000,width=4)

  img.ellipse((ai3_x1+1,ai3_y1+3,ai3_x2-1,ai3_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai3_x1+7,ai3_y1+8), 0x000000,width=4)
  img.point((ai3_x2-9,ai3_y1+8), 0x000000,width=4)

  img.ellipse((ai4_x1+1,ai4_y1+3,ai4_x2-1,ai4_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai4_x1+7,ai4_y1+8), 0x000000,width=4)
  img.point((ai4_x2-9,ai4_y1+8), 0x000000,width=4)

 if level_ == 8:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='down':
    if ai1_y2 < 208:
      ai1_y1 += 26
      ai1_y2 += 26
      ai1_pos += 8
    else: ai1_vect='right'
   if ai1_vect=='right':
    if ai1_x2 < x[4]:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='up'
   if ai1_vect=='up':
    if ai1_y1 > 0:
      ai1_y1 -= 26
      ai1_y2 -= 26
      ai1_pos -= 8
    else: ai1_vect='left'
   if ai1_vect=='left':
    if ai1_x1 > 0:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='down'
# ^ enemy 1 animation

  if ai2_y2 < 208 or ai2_y1 > 0 or ai2_x1 > 0 or ai2_x2 < 176:
   if ai2_vect=='down':
    if ai2_y2 < 208:
      ai2_y1 += 26
      ai2_y2 += 26
      ai2_pos += 8
    else: ai2_vect='right'
   if ai2_vect=='right':
    if ai2_x2 < x[4]:
      ai2_x1 += 22
      ai2_x2 += 22
      ai2_pos += 1
    else: ai2_vect='up'
   if ai2_vect=='up':
    if ai2_y1 > 0:
      ai2_y1 -= 26
      ai2_y2 -= 26
      ai2_pos -= 8
    else: ai2_vect='left'
   if ai2_vect=='left':
    if ai2_x1 > 0:
      ai2_x1 -= 22
      ai2_x2 -= 22
      ai2_pos -= 1
    else: ai2_vect='down'
# ^ enemy 2 animation

  if ai3_y2 < 208 or ai3_y1 > 0 or ai3_x1 > 0 or ai3_x2 < 176:
   if ai3_vect=='down':
    if ai3_y2 < 208:
      ai3_y1 += 26
      ai3_y2 += 26
      ai3_pos += 8
    else: ai3_vect='right'
   if ai3_vect=='right':
    if ai3_x2 < x[8]:
      ai3_x1 += 22
      ai3_x2 += 22
      ai3_pos += 1
    else: ai3_vect='up'
   if ai3_vect=='up':
    if ai3_y1 > 0:
      ai3_y1 -= 26
      ai3_y2 -= 26
      ai3_pos -= 8
    else: ai3_vect='left'
   if ai3_vect=='left':
    if ai3_x1 > x[4]:
      ai3_x1 -= 22
      ai3_x2 -= 22
      ai3_pos -= 1
    else: ai3_vect='down'
# ^ enemy 3 animation

  if ai4_y2 < 208 or ai4_y1 > 0 or ai4_x1 > 0 or ai4_x2 < 176:
   if ai4_vect=='down':
    if ai4_y2 < 208:
      ai4_y1 += 26
      ai4_y2 += 26
      ai4_pos += 8
    else: ai4_vect='right'
   if ai4_vect=='right':
    if ai4_x2 < x[8]:
      ai4_x1 += 22
      ai4_x2 += 22
      ai4_pos += 1
    else: ai4_vect='up'
   if ai4_vect=='up':
    if ai4_y1 > 0:
      ai4_y1 -= 26
      ai4_y2 -= 26
      ai4_pos -= 8
    else: ai4_vect='left'
   if ai4_vect=='left':
    if ai4_x1 > x[4]:
      ai4_x1 -= 22
      ai4_x2 -= 22
      ai4_pos -= 1
    else: ai4_vect='down'
# ^ enemy 4 animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

  img.ellipse((ai2_x1+1,ai2_y1+3,ai2_x2-1,ai2_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai2_x1+7,ai2_y1+8), 0x000000,width=4)
  img.point((ai2_x2-9,ai2_y1+8), 0x000000,width=4)

  img.ellipse((ai3_x1+1,ai3_y1+3,ai3_x2-1,ai3_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai3_x1+7,ai3_y1+8), 0x000000,width=4)
  img.point((ai3_x2-9,ai3_y1+8), 0x000000,width=4)

  img.ellipse((ai4_x1+1,ai4_y1+3,ai4_x2-1,ai4_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai4_x1+7,ai4_y1+8), 0x000000,width=4)
  img.point((ai4_x2-9,ai4_y1+8), 0x000000,width=4)

 if level_ == 9:
  if ai1_y2 < 208 or ai1_y1 > 0 or ai1_x1 > 0 or ai1_x2 < 176:
   if ai1_vect=='down':
    if ai1_y2 < y[4]:
      ai1_y1 += 26
      ai1_y2 += 26
      ai1_pos += 8
    else: ai1_vect='right'
   if ai1_vect=='right':
    if ai1_x2 < x[4]:
      ai1_x1 += 22
      ai1_x2 += 22
      ai1_pos += 1
    else: ai1_vect='up'
   if ai1_vect=='up':
    if ai1_y1 > 0:
      ai1_y1 -= 26
      ai1_y2 -= 26
      ai1_pos -= 8
    else: ai1_vect='left'
   if ai1_vect=='left':
    if ai1_x1 > 0:
      ai1_x1 -= 22
      ai1_x2 -= 22
      ai1_pos -= 1
    else: ai1_vect='down'
# ^ enemy 1 animation

  if ai2_y2 < 208 or ai2_y1 > 0 or ai2_x1 > 0 or ai2_x2 < 176:
   if ai2_vect=='down':
    if ai2_y2 < 208:
      ai2_y1 += 26
      ai2_y2 += 26
      ai2_pos += 8
    else: ai2_vect='right'
   if ai2_vect=='right':
    if ai2_x2 < x[4]:
      ai2_x1 += 22
      ai2_x2 += 22
      ai2_pos += 1
    else: ai2_vect='up'
   if ai2_vect=='up':
    if ai2_y1 > y[4]:
      ai2_y1 -= 26
      ai2_y2 -= 26
      ai2_pos -= 8
    else: ai2_vect='left'
   if ai2_vect=='left':
    if ai2_x1 > 0:
      ai2_x1 -= 22
      ai2_x2 -= 22
      ai2_pos -= 1
    else: ai2_vect='down'
# ^ enemy 2 animation

  if ai3_y2 < 208 or ai3_y1 > 0 or ai3_x1 > 0 or ai3_x2 < 176:
   if ai3_vect=='down':
    if ai3_y2 < 208:
      ai3_y1 += 26
      ai3_y2 += 26
      ai3_pos += 8
    else: ai3_vect='right'
   if ai3_vect=='right':
    if ai3_x2 < 176:
      ai3_x1 += 22
      ai3_x2 += 22
      ai3_pos += 1
    else: ai3_vect='up'
   if ai3_vect=='up':
    if ai3_y1 > y[4]:
      ai3_y1 -= 26
      ai3_y2 -= 26
      ai3_pos -= 8
    else: ai3_vect='left'
   if ai3_vect=='left':
    if ai3_x1 > x[4]:
      ai3_x1 -= 22
      ai3_x2 -= 22
      ai3_pos -= 1
    else: ai3_vect='down'
# ^ enemy 3 animation

  if ai4_y2 < 208 or ai4_y1 > 0 or ai4_x1 > 0 or ai4_x2 < 176:
   if ai4_vect=='down':
    if ai4_y2 < y[4]:
      ai4_y1 += 26
      ai4_y2 += 26
      ai4_pos += 8
    else: ai4_vect='right'
   if ai4_vect=='right':
    if ai4_x2 < 176:
      ai4_x1 += 22
      ai4_x2 += 22
      ai4_pos += 1
    else: ai4_vect='up'
   if ai4_vect=='up':
    if ai4_y1 > 0:
      ai4_y1 -= 26
      ai4_y2 -= 26
      ai4_pos -= 8
    else: ai4_vect='left'
   if ai4_vect=='left':
    if ai4_x1 > x[4]:
      ai4_x1 -= 22
      ai4_x2 -= 22
      ai4_pos -= 1
    else: ai4_vect='down'
# ^ enemy 4 animation

  img.ellipse((ai1_x1+1,ai1_y1+3,ai1_x2-1,ai1_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai1_x1+7,ai1_y1+8), 0x000000,width=4)
  img.point((ai1_x2-9,ai1_y1+8), 0x000000,width=4)

  img.ellipse((ai2_x1+1,ai2_y1+3,ai2_x2-1,ai2_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai2_x1+7,ai2_y1+8), 0x000000,width=4)
  img.point((ai2_x2-9,ai2_y1+8), 0x000000,width=4)

  img.ellipse((ai3_x1+1,ai3_y1+3,ai3_x2-1,ai3_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai3_x1+7,ai3_y1+8), 0x000000,width=4)
  img.point((ai3_x2-9,ai3_y1+8), 0x000000,width=4)

  img.ellipse((ai4_x1+1,ai4_y1+3,ai4_x2-1,ai4_y2-3),0xff0000,fill=0xff0000,)
  img.point((ai4_x1+7,ai4_y1+8), 0x000000,width=4)
  img.point((ai4_x2-9,ai4_y1+8), 0x000000,width=4)

def _death():
 img.rectangle((x1+3,y1+7,x2-3,y1+11),0xffffff,fill=0xffffff)
 img.rectangle((x1+9,y1+3,x2-9,y2-3),0xffffff,fill=0xffffff)

def _run():
 global field,level_,run_
 can.bind(63557,lambda:None)
 can.bind(63495,lambda:_left())
 can.bind(63496,lambda:_right())
 can.bind(63497,lambda:_up())
 can.bind(63498,lambda:_down())
 can.bind(52,lambda:_left())
 can.bind(54,lambda:_right())
 can.bind(50,lambda:_up())
 can.bind(56,lambda:_down())
 app.exit_key_handler=_menu
 dead_=0
 time_death=10
 first_run=1
 while 1:
  for y_pos in range(0,8):
   for x_pos in range(0,8):
    if field[(y_pos*8)+x_pos] == 0:
     img.rectangle((x[x_pos],y[y_pos],x[x_pos+1],y[y_pos+1]), 0x008000, fill=0x000000)
    if field[(y_pos*8)+x_pos] == 1:
     img.rectangle((x[x_pos],y[y_pos],x[x_pos+1],y[y_pos+1]), 0x008000, fill=0xff8000)
    if field[(y_pos*8)+x_pos] == 2:
     img.rectangle((x[x_pos],y[y_pos],x[x_pos+1],y[y_pos+1]), 0x008000, fill=0x000000)
     img.point(((x[x_pos]+x[x_pos+1])/2,(y[y_pos]+y[y_pos+1])/2), 0x00ff00, width=2)

  if dead_==1:
    can.bind(63557,lambda:None)
    can.bind(63495,lambda:None)
    can.bind(63496,lambda:None)
    can.bind(63497,lambda:None)
    can.bind(63498,lambda:None)
    can.bind(52,lambda:None)
    can.bind(54,lambda:None)
    can.bind(50,lambda:None)
    can.bind(56,lambda:None)
    _death()
    time_death -= 1
    if time_death==0:
      dead_=0
      _level(level_)
      _run()
  else:
    _kolobok()
  _ai()
  _redraw()
  if first_run == 1:
   note(unicode('Level '+str(level_)),'conf')
   first_run = 0
  next_level=0
  for y_pos in range(0,8):
   for x_pos in range(0,8):
    if field[(y_pos*8)+x_pos] == 2:
     next_level += 1
  if next_level == 0:
   if level_<9:
    level_+=1
    _level(level_)
    note(unicode('Level complete :)'),'conf')
    _run()
   else:
    note(u'congratulation, you win! :)','conf')
    run_=0
   _menu()
  if (ai1_pos==pos or ai2_pos==pos or ai3_pos==pos or ai4_pos==pos) and dead_ != 1:
   dead_=1
   time_death=10
   note(u'you are dead :(','error')
  sleep(0.1)

_intro()