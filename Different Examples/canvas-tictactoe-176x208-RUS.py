# -*- coding: utf-8 -*-
# by Ash_Rockit
#*------------------------------*#
from appuifw import *
from graphics import Image
from e32 import *
#*------------------------------*#
def _set():
 global pos_x,pos_y,w,o,pole,figura,s,win,nichya
 pole = [
     [9,9,9],
     [9,9,9],
     [9,9,9]] # ïoëe(9-ïycòaÿ êëeòêa/0-íoëü/1-êpecò)
 pos_x,pos_y=0,0 # ïoçèöèÿ yêaçaòeëÿ
 figura=1 # ía÷aëüíaÿ ôèãypa(0-íoëü/1-êpecò)
 w=58 # øèpèía êëeòêè
 s=28 # cäâèã ïoëÿ ïo ocè y
 o=4 # oòcòyï ôèãypû oò êpaÿ êëeòêè
 win=2 # ôëaã ïoáeäèòeëÿ(0-íoëü/1-êpecò)
 nichya=9
#
_set()
run=1 # 
krest_win=0 # c÷eò÷èê ïoáeä êpecòèêa
zero_win=0 # c÷eò÷èê ïoáeä íoëèêa
sleep = ao_sleep
app.screen = 'full'
#*------------------------------*#
def _redraw():
 can.blit(img)
app.body = can = Canvas(redraw_callback=_redraw)
img = Image.new((176,208))
#*------------------------------*#
def _krest((x,y),c,wd): # pècyeì êpecò
  img.line(
 ((x*w)+o,((y*w)+s)+o,((x+1)*w)-o,(((y+1)*w)+s)-o),
 c,width=wd)
  img.line(
 (((x+1)*w)-o,((y*w)+s)+o,(x*w)+o,(((y+1)*w)+s)-o),
 c,width=wd)
#*------------------------------*#
def _zero((x,y),c,wd): # pècyeì íoëü
  img.ellipse(
 ((x*w)+o,((y*w)+s)+o,((x+1)*w)-o,(((y+1)*w)+s)-o),
 c,width=wd)
#*------------------------------*#
def _enter():
 global figura
 if pole[pos_y][pos_x] == 9:
# ecëè ÿ÷eéêa pole[pos_y][pos_x] ïycòaÿ(9) òo
   pole[pos_y][pos_x] = figura
# â ýòy ÿ÷eéêy còaâèì ôèãypy
   if figura == 0: figura = 1
# ecëè ôèãypa paâíÿëacü íoëèêy(0), òo òeïepü oía = êpecòèêy(1)
   else: figura = 0
# èía÷e ôèãypa = íoëèêy(0)
#*------------------------------*#
def _move(vect):
 global pos_x,pos_y
 if vect==2 and pos_y>0: pos_y-=1
 if vect==8 and pos_y<2: pos_y+=1
 if vect==4 and pos_x>0: pos_x-=1
 if vect==6 and pos_x<2: pos_x+=1
#*------------------------------*#
def _stat():
 global win,nichya
 nichya=9
 for a in range(0,3):
  for b in range(0,3):
   try:
    if pole[a][b]==1 and pole[a+1][b]==1 and pole[a+2][b]==1: win=1
   except:None
# 3 êpecòa ïo âepòèêaëè
   try:
    if pole[a][b]==1 and pole[a][b+1]==1 and pole[a][b+2]==1: win=1
   except:None
# 3 êpecòa ïo ãopèçoíòaëè
   try:
    if pole[a][b]==1 and pole[a+1][b+1]==1 and pole[a+2][b+2]==1: win=1
   except:None
# 3 êpecòa ïo äèaãoíaëè 1
   try:
    if pole[a][b+2]==1 and pole[a+1][b+1]==1 and pole[a+2][b]==1: win=1
   except:None
# 3 êpecòa ïo äèaãoíaëè 2
   try:
    if pole[a][b]==0 and pole[a+1][b]==0 and pole[a+2][b]==0: win=0
   except:None
# 3 íyëÿ ïo âepòèêaëè
   try:
    if pole[a][b]==0 and pole[a][b+1]==0 and pole[a][b+2]==0: win=0
   except:None
# 3 íyëÿ ïo ãopèçoíòaëè
   try:
    if pole[a][b]==0 and pole[a+1][b+1]==0 and pole[a+2][b+2]==0: win=0
   except:None
# 3 íyëÿ ïo äèaãoíaëè 1
   try:
    if pole[a][b+2]==0 and pole[a+1][b+1]==0 and pole[a+2][b]==0: win=0
   except:None
# 3 íyëÿ ïo äèaãoíaëè 2
   if pole[a][b]!=9: nichya-=1
#*------------------------------*#
def _end():
 global run
 run=0
#*------------------------------*#
can.bind(63497,lambda:_move(2))
can.bind(63498,lambda:_move(8))
can.bind(63495,lambda:_move(4))
can.bind(63496,lambda:_move(6))
can.bind(63557,lambda:_enter())
app.exit_key_handler=_end
#*------------------------------*#
def _run():
 global krest_win,zero_win,nichya
 _set()
 while run:
  img.clear(0)
  for i in range(0,3):
   for j in range(0,3):
    if pos_x==j and pos_y==i:
     img.rectangle((j*w,(i*w)+s,(j+1)*w,((i+1)*w)+s),0xffffff,width=3)
    else:
     img.rectangle((j*w,(i*w)+s,(j+1)*w,((i+1)*w)+s),0x008000)
# pècyeì ïoëe
    if pole[i][j] == 0:
     _zero((j, i), 0xff5555,wd=3)
    if pole[i][j] == 1:
     _krest((j, i), 0x99ccff,wd=3)
# còaâèì ôèãypû
  if figura==1:
    col_k=(150,200,255)
    col_z=(50,50,50)
  if figura==0:
    col_z=(255,80,80)
    col_k=(50,50,50)
  img.text((20,18),unicode('krest'),col_k)
  img.text((130,18),unicode('zero'),col_z)
  img.text((80,18),unicode(str(krest_win)+' : '+str(zero_win)),0xffffff)

  if win==1:
    note(u'Win Krest','conf')
    krest_win+=1
    _run()
  if win==0:
    note(u'Win Zero','conf')
    zero_win+=1
    _run()
  if nichya==0:
    note(u'Ni4ya','conf')
    krest_win+=1
    zero_win+=1
    _run()

  _stat()
  _redraw()
  sleep(0.1)
#*------------------------------*#
_run()
#*------------------------------*#