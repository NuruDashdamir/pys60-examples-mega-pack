#by Shrim
#mod to code Sph1nkS

from appuifw import app,Text,query,note
from e32 import Ao_lock,ao_yield as yld
from sysinfo import display_pixels
from topwindow import TopWindow
from graphics import Image
from socket import socket
from struct import unpack
from os import remove
from sys import path

def ru(x):return unicode(x,'utf-8','ignore')
def lenres(sock):
 t=unpack('6B',sock.recv(6))
 return int(hex(t[4])+hex(t[5])[2:],16)
def getdata(x):
 while 1:
  t=query(ru(x),'text')
  if t:
   try:t=str(t);break
   except:note(ru('Некорректный ввод'),'error')
  yld()
 return t
def rega():
 txt.focus=False
 txt.set(ru('коннектимся...\n')),yld()
 sock=socket(2048,1)
 sock.connect(('login.icq.com',5190))
 sock.recv(10)
 sock.send('\x2a\x01\x92\x9a\x00\x04\x00\x00\x00\x01\x2a\x02\x92\x9b\x00\x0c\x00\x17\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00')
 txt.set(ru('загружаю картинку\n')),yld()
 d,l='',lenres(sock)
 while 1:
  d+=sock.recv(l)
  if d.endswith('\xff\xd9')>0:break
 open('d:\\img.jpg','w').write(d[28:])
 top=TopWindow()
 img=Image.open('d:\\img.jpg')
 img=img.resize((display_pixels()[0],int(float(img.size[1])/img.size[0]*display_pixels()[0])))
 top.size=img.size
 top.add_image(img,(0,0)),remove('d:\\img.jpg')
 txt.set(ru('вводим данные\nпароль желательно шесть знаков\nкод с картинки вводите заглавными буквами\n')),yld()
 pwd=getdata('Введите пароль')
 top.show()
 slv=getdata('Введите кодовое слово')
 top.hide(),txt.set(ru('отсылаю данные\n')),yld()
 lpwd=str(33+len(pwd))
 cpwd='0'+str(len(pwd)+1)+'00'+pwd.encode('hex')+10*'0'+'e30700000009000'+str(len(slv))+slv.encode('hex')
 ldat=str(hex((len(lpwd+cpwd)+106)/2))[2:]
 sock.send(('2a02929c00'+ldat+'00170004'+15*'0'+'100'+lpwd+8*'0'+'28'+70*'0'+cpwd).decode('hex'))
 l=lenres(sock)
 if l==66:
  uin=str(unpack('i',sock.recv(l)[56:60])[0])
  open('c:\\icquin.txt','a').write('UIN: '+uin+' PASSWORD: '+pwd+'\r\n')
  txt.focus=True
  txt.set(ru('Ваш UIN: '+uin+'\nВаш пароль:'+pwd+'\nДанные записаны в файл c:\\icquin.txt\nИзменить информацию можно на сайте\nhttp://ruwap.org/service/edit_icq/')),yld()
 else:
  txt.set(ru('регистрация прошла неудачно, попробуйте ещё раз\n')),yld()
 sock.close()

app.body=txt=Text()
txt.focus,txt.color,app.menu,app.screen,app.exit_key_handler,in_console=False,0,[(ru('регистрировать UIN'),rega)],'large',app.set_exit,0
txt.set(ru('Автор программы Sph1nkS\nМодифицировал Shrim\n'))
for i in path:
 if i.lower().find('python')>0:in_console=1;break
if in_console:Ao_lock().wait()
