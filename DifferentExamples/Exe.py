import appuifw,os,e32,sys
_chose_points=True
_start=True
_invisible_point=True
appuifw.app.screen='full'
from key_codes import *
def ru(x):return x.decode('utf-8')
pathway=ru(os.path.split(sys.argv[0])[0]+'\\')
fine=ru('Путь к файлу:\n')+unicode(pathway)+u'Your.exe'
_file=open(pathway+'exe.exe')
hex_text=_file.read()
_file.close()
_begining=hex_text[:7508]
_after_picture=hex_text[7697:7700]
_after_top_text=hex_text[7724:7728]
_after_middle_text=hex_text[7746:7748]
_end=hex_text[7794:]
oldposition=[0,0]
position=[0,0]
points=['\x00']*189
def ainfo(x):appuifw.note(ru(x))
def aerror(x):appuifw.note(ru(x),'error')
def input_text():
 global top_text,middle_text,bottom_text,_start
 _start=False
 a=0
 while a==0:
  try:
   top_text=appuifw.query(ru('Текст над картинкой (до 10 символов)'),'text').encode('ascii')
   if top_text==None:top_text=''
   if len(top_text)<11:a=1
   else:ainfo('Введено более 10 символов')
  except:aerror('Встречаются посторонние символы')
 a=0
 while a==0:
  try:
   middle_text=appuifw.query(ru('Текст под картинкой (до 7 символов)'),'text').encode('ascii')
   if middle_text==None:middle_text=''
   if len(middle_text)<8:a=1
   else:ainfo('Введено более 7 символов')
  except:aerror('Встречаются посторонние символы')
 a=0
 while a==0:
  try:
   bottom_text=appuifw.query(ru('Текст снизу (до 21 символов)'),'text').encode('ascii')
   if bottom_text==None:bottom_text=''
   if len(bottom_text)<22:a=1
   else:ainfo('Введено более 21 символов')
  except:aerror('Встречаются посторонние символы')
 appuifw.note(ru('Приступаю к рисованию картинки'),'conf')
 appuifw.app.exit_key_handler=red_point
 make_picture()
appuifw.app.body=can=appuifw.Canvas()
def make_picture():
 global _start
 _start=False
 can.bind(EKeySelect,lambda:nothing())
 can.bind(53,lambda:nothing())
 for i in range(53):
  can.clear()
  can.rectangle((0,208-i*4, 176, 222-i*4), 255, fill = (255))
  can.text((50,219-i*4), ru('Выбор точек'), 0xffffff)
  e32.ao_sleep(.005)
 set_position()
 can.bind(EKeySelect,lambda:select())
 can.bind(53,lambda:select())
 can.bind(EKeyUpArrow,lambda:up())
 can.bind(EKeyDownArrow,lambda:down())
 can.bind(EKeyLeftArrow,lambda:left())
 can.bind(EKeyRightArrow,lambda:right())
 can.bind(63586,lambda:exit())
 for g in range(27):
  for i in range(7):
   can.rectangle((21+5*g,18+5*i, 25+5*g, 22+5*i), 0xdddddd, fill=0xdddddd)
  e32.ao_sleep(.005)
  can.rectangle((19,16, 157, 54), 0)
 for i in range(44):
  can.rectangle((i*2,190,i*2+2,208),255)
  can.rectangle((174-i*2,190,176-i*2,208),255)
  e32.ao_sleep(.005)
 for i in range(16):
  can.text((2,202), ru('Выход'), 255+i*1118464)
  can.text((135,202), ru('Далее'), 255+i*1118464)
  can.text((1,100),ru('Используйте джойстик и "5"'),0xffffff-i*0x111111)
  can.line((45,i+192,133,i+192),0xffffff)
  can.line((45,i+190,133,i+190),0xffffff)
  e32.ao_sleep(.005)
 while _chose_points:chose_pnt()
def chose_pnt():
 can.rectangle((0,0, 176,14), 255, fill = (255))
 can.text((50,11), ru('Выбор точек'), 0xffffff)
 set_position()
 for g in range(27):
  for i in range(7):
   a=27*i+g
   if points[a]=='\x00':b=0xdddddd
   else:b=0
   can.rectangle((21+5*g,18+5*i, 25+5*g, 22+5*i),b, fill=b)
 can.rectangle((19,16, 157, 54), 0)
 can.rectangle((0,190,176,208),255,fill=255)
 can.text((2,202), ru('Выход'),0xffffff)
 can.text((135,202), ru('Далее'),0xffffff)
 can.rectangle((45 ,190,133,208),0xffffff,fill=0xffffff)
 can.text((1,100),ru('Используйте джойстик и "5"'),0)
 e32.ao_sleep(2)
def exit():appuifw.app.set_exit()
def set_position():
 can.rectangle((5*oldposition[0]+20,5*oldposition[1]+17, 5*oldposition[0]+26,5*oldposition[1]+23), 0xffffff)
 can.rectangle((5*position[0]+20,5*position[1]+17, 5*position[0]+26,5*position[1]+23), 16711680)
def up():
 position[1]-=1
 if position[1]<0:position[1]=6
 set_position()
 oldposition[1]=position[1]
def down():
 position[1]+=1
 if position[1]>6:position[1]=0
 set_position()
 oldposition[1]=position[1]
def left():
 position[0]-=1
 if position[0]<0:position[0]=26
 set_position()
 oldposition[0]=position[0]
def right():
 position[0]+=1
 if position[0]>26:position[0]=0
 set_position()
 oldposition[0]=position[0]
def select():
 what_color=position[0]+27*position[1]
 if points[what_color]=='\x00':
  can.rectangle((21+5*position[0],18+5*position[1], 25+5*position[0], 22+5*position[1]), 0, fill=0)
  points[what_color]='\x01'
 else:
  can.rectangle((21+5*position[0],18+5*position[1], 25+5*position[0], 22+5*position[1]), 0xdddddd, fill=0xdddddd)
  points[what_color]='\x00'
def nothing():pass
def select_red():
 global _invisible_point
 _invisible_point=False
 appuifw.app.exit_key_handler=exit
 can.bind(EKeySelect,lambda:nothing())
 can.bind(53,lambda:nothing())
 can.bind(EKeyUpArrow,lambda:nothing())
 can.bind(EKeyDownArrow,lambda:nothing())
 can.bind(EKeyLeftArrow,lambda:nothing())
 can.bind(EKeyRightArrow,lambda:nothing())
 can.bind(63586,lambda:nothing())
 points[position[0]+27*position[1]]='\x02'
 make_exe()
def red_point():
 global _chose_points
 appuifw.app.exit_key_handler=nothing
 _chose_points=False
 can.bind(EKeySelect,lambda:select_red())
 can.bind(53,lambda:select_red())
 for i in range(150):
  can.rectangle((0,0, 176, 14), 255, fill = (255))
  can.text((50-i,11), ru('Выбор точек              Исчезающая точка'), 0xffffff)
  if i<70:
   can.line((132+i,190, 132+i, 208), 0xffffff)
   can.rectangle((133+i,190, 176, 208), 255, fill = (255))
   can.text((135+i,202), ru('Далее'), 0xffffff)
  elif 69<i<86:
   can.text((1,100),ru('Используйте джойстик и "5"'),(i-70)*0x111111)
   can.text((50,111), ru('Выбор исчезающей'), 0xffffff-0x111111*(i-70))
   can.text((140,123), ru('точки'), 0xffffff-0x111111*(i-70))
  e32.ao_sleep(.005)
 while _invisible_point:invisible_point()
def invisible_point():
 can.rectangle((0,0, 176, 14), 255, fill = (255))
 can.text((-100,11), ru('Выбор точек              Исчезающая точка'), 0xffffff)
 set_position()
 for g in range(27):
  for i in range(7):
   a=27*i+g
   if points[a]=='\x00':b=0xdddddd
   else:b=0
   can.rectangle((21+5*g,18+5*i, 25+5*g, 22+5*i),b, fill=b)
  can.rectangle((19,16, 157, 54), 0)
 can.text((50,111), ru('Выбор исчезающей'),0)
 can.text((140,123), ru('точки'),0)
 can.rectangle((0,190,45,208),255,fill=255)
 can.text((2,202), ru('Выход'),0xffffff)
 e32.ao_sleep(2)
def len_scan(x):
 global le
 if x==0:le='\x00'
 elif x==1: le='\x01'
 elif x==2: le='\x02'
 elif x==3: le='\x03'
 elif x==4: le='\x04'
 elif x==5: le='\x05'
 elif x==6: le='\x06'
 elif x==7: le='\x07'
 elif x==8: le='\x08'
 elif x==9: le='\x09'
 elif x==10: le='\x0a'
 elif x==11: le='\x0b'
 elif x==12: le='\x0c'
 elif x==13: le='\x0d'
 elif x==14: le='\x0e'
 elif x==15: le='\x0f'
 elif x==16: le='\x10'
 elif x==17: le='\x11'
 elif x==18: le='\x12'
 elif x==19: le='\x13'
 elif x==20: le='\x14'
 elif x==21: le='\x15'
def encode_text(x,y,z):
 global text
 text=''
 for i in range(len(x)):
  text+=(x[i]+'\x00')
 t='\x00'*z
 text+=' \x00'*(y-len(x))+t
def make_exe():
 global _begining,all_points,_after_picture,len_top_text,top_text,_after_top_text,len_middle_text,middle_text,_after_middle_text,len_bottom_text,bottom_text,_end
 len_scan(len(top_text))
 len_top_text=le
 len_scan(len(middle_text))
 len_middle_text=le
 len_scan(len(bottom_text))
 len_bottom_text=le
 encode_text(top_text,10,4)
 top_text=text
 encode_text(middle_text,7,2)
 middle_text=text
 encode_text(bottom_text,21,0)
 bottom_text=text
 all_points=''
 for i in points:
  all_points+=i
 t='\x00'*3
 all=_begining+all_points+_after_picture+len_top_text+t+top_text+len_middle_text+t+middle_text+len_bottom_text+t+bottom_text+_end
 _file=open(pathway+'Your.exe','w')
 _file.write(all)
 _file.close()
 outro()
def outro():
 for i in range(27):
  can.clear()
  can.rectangle((0,i*4, 176, 14+i*4), 255, fill = (255))
  can.text((45,12+i*4), ru('Your.exe создан!'),0xffffff)
  e32.ao_sleep(.005)
 e32.ao_sleep(1)
 for i in range(160):
  can.rectangle((0,104, 176, 118), 255, fill = (255))
  can.text((45-i,116), ru('Your.exe создан!                До встречи!'),0xffffff)
  e32.ao_yield()
 e32.ao_sleep(1)
 if appuifw.query(fine+ru('\nЗапустить?'),'query'):e32.start_exe(pathway+'Your.exe',pathway+'Your.exe')
 exit()
def intro():
 global temp_points
 temp_points='\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x01\x01\x00\x01\x01\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x00\x00\x01\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x00\x00\x01\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x00\x00\x01\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x01\x01\x00\x01\x01\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00'
 for g in range(27):
  for i in range(7):
   a=27*i+g
   if temp_points[a]=='\x00':b=0xffffff
   else:b=180
   can.rectangle((21+5*g,18+5*i, 25+5*g, 22+5*i),b, fill=b)
  e32.ao_sleep(.005)
 can.bind(EKeySelect,lambda:input_text())
 can.bind(53,lambda:input_text())
 start()
def start():
 while _start:
  can.text((98,140),ru('Dimontyay'),65280)
  can.text((25,140),ru('Создатель:'),0xff0000)
  can.text((55,160),ru('СПАСибо'),65280)
  can.text((110,160),u'MVM',0xff0000)
  a=3342335
  can.rectangle((60,191, 110, 205),0, fill=0xcccccc)
  can.text((65,203),ru('Начать'),0xffffff)
  for i in range(9):
   can.rectangle((16,13+5*i, 20, 17+5*i),a, fill=a)
   e32.ao_sleep(.005)
  for i in range(27):
   for g in range(7):
    s=27*g+i
    if temp_points[s]=='\x00':b=0xffffff
    else:b=180
    can.rectangle((21+5*i,18+5*g, 25+5*i, 22+5*g),b, fill=b)
   can.rectangle((16+i*5,53, 20+i*5, 57),a, fill=a)
   e32.ao_sleep(.005)
  for i in range(9):
   can.rectangle((151,53-5*i, 155,57-5*i),a, fill=a)
   e32.ao_sleep(.005)
  for i in range(26):
   can.rectangle((146-i*5,13, 150-i*5, 17),a, fill=a)
   e32.ao_sleep(.005)
  a=0xffffff
  for i in range(9):
   can.rectangle((16,13+5*i, 20, 17+5*i),a, fill=a)
   e32.ao_sleep(.005)
  for i in range(27):
   can.rectangle((16+i*5,53, 20+i*5, 57),a, fill=a)
   e32.ao_sleep(.005)
  for i in range(9):
   can.rectangle((151,53-5*i, 155,57-5*i),a, fill=a)
   e32.ao_sleep(.005)
  for i in range(26):
   can.rectangle((146-i*5,13, 150-i*5, 17),a, fill=a)
   e32.ao_sleep(.005)
appuifw.app.exit_key_handler=nothing
intro()

