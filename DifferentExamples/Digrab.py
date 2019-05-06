from appuifw import *
from graphics import *
import urllib,os,e32
#import topwindow
def ru(x):return x.decode('utf-8')
#
app.title=u'DiGrab beta'
set=[]
set_path='e:/system/apps/RunPython/Apps/DiGrab/set.dat'
set_path2='e:/python/app.dat'
content={}
app_set=[]
#~~~~связь с внешним миром~~
def get(url,kament=0):
 if kament==u'1':kam='yes'
 else:kam='no'
 try:
  x=urllib.urlopen('http://python.mirahost.ru/my_projects/digrab.php?kament='+kam+'&url='+url).read().decode('cp1251')
  return x.split(':||:')
 except:return [u'0',u'0',u'none',u'none']

def read_set():
 global set
 file=open(set_path).read()
 set=[j.split(':||:') for j in file.split(':|n|:')]

def update():
 global content
 content={}
 for a in range(len(set)):
  note(ru('идет обновление\n'+str(a+1)+' из '+str(len(set))))
  e32.ao_sleep(0.5)
  dat=set[a]
  m=get(dat[1],dat[2])
  if dat[2]==u'1':content[dat[0]]=m
  else:content[dat[0]]=[m[0],m[1],ru('не включено'),ru('не включено')]

def save():
 file=open(set_path,'w')
 for i in range(len(set)):
  file.write(':||:'.join(set[i]))
  if i<(len(set)-1):file.write(':|n|:')
 file.close()
 note(ru('Настройки сохранены!'),'conf')

def new():
 global set
 name=query(ru('название: (латинскими)'),'text',u'name').encode('utf-8')
 url=query(ru('url:'),'text',u'http://')
 if url.startswith('http://dimonvideo.ru/smart/'):pass
 else:
  note(ru('неправильный адрес'),'error')
  return None
 kam=query(ru('Включить последний камент?'),'query')
 set.append([name,url,str(kam)]) 
 save()
def delete():
 global set
 n=[]
 for a in range(len(set)):
  n.append(set[a][0].decode('utf-8'))
 x=popup_menu(n,ru('удалить:'))
 if (x<>None):
  del set[x]
  save()
  

#~~~~графическая часть~~~~

def show_splash():
 main=Text()
 main.color = 0
 main.font = u'LatinBold17'
 main.style = HIGHLIGHT_ROUNDED
 main.highlight_color = 11184810
 main.add(ru('      DiGrab beta      \r\n'))
 main.font = u'Alp13'
 main.color = 0
 main.style = STYLE_BOLD
 main.add(ru('Автор: Игорь aka kAIST\r\n'))
 main.add(ru('e-mail: igor.kaist@gmail.com\r\n'))
 main.add(ru('ICQ:211141235\r\n'))
 main.add(ru('Сайт: python.mirahost.ru\r\n'))
 main.add(ru('Поддержите мои проекты, выбрав в меню "Отблагодарить автора" :)'))
 main.bind(0xf807,None)
 main.bind(0xf808,None)
 app.body = main
 app.body.focus=False
 app.menu=[(ru('Старт'),show),(ru('Создать url'),new),(ru('Удалить url'),delete)]

main=Text()
def show():
 update()
 show_one()


def show_one():
 main=Text()
 app.menu=[(ru('Обновить'),update),(ru('В главное меню'),show_splash)]
 dag=[]
 for x in content.keys():dag.append(x)
 main.color=0x000000
 main.style = HIGHLIGHT_ROUNDED
 main.highlight_color = 0xdddddd
 main.add(ru('<<      файл:'+dag[kursor]+'      >>>\r\n'))
 main.style=STYLE_BOLD
 ggg=dag[kursor]
 main.add(ru('Скачано: ')+content[ggg][0]+ru(' раз.\r\n'))
 main.add(ru('Каментов: ')+content[ggg][1]+ru(' штук.\r\n'))
 main.add(ru('Последний от: ')+content[ggg][2]+ru('\r\n'))
 j=content[ggg][3].replace(u'<br>',u'')
 main.style=0
 main.add(j) 
 main.bind(0xf807,lambda:left())
 main.bind(0xf808,lambda:pravo())
 app.body=main

def pravo():
 global kursor
 max=len(set)-1
 if kursor<max:kursor=kursor+1
 show_one()
def left():
 global kursor
 max=len(content.keys())-1
 if kursor>0:kursor=kursor-1
 show_one()

kursor=0
read_set()
#show_one()
show_splash()
e32.ao_sleep(30)

