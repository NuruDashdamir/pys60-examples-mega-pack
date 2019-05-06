import e32
import appuifw
appuifw.app.screen='large'
appuifw.app.title=u'FMaker'
ao=e32.Ao_lock()
def ru(x):return x.decode('utf-8')
appuifw.app.body=txt=appuifw.Text()
txt.color=0x000000
txt.focus=False
txt.add(ru('    FMaker by kAIST ver.1.0\nВыберите в меню диапазон размеров файла и введите нужное значение!\nВНИМАНИЕ!!! При больших значениях скрипт будет выполняться долго\n\nРеквезиты автора:\ne-mail:igor.kaist@gmail.com\nICQ:211141235\nСпасибо сайту:\n www.dimonvideo.ru'))
def kb(numb):
 for x in range(0,numb*1024):
  tf.write('x')
def mb(numb):
 for x in range(0,numb*1024):
  kb(1)
def b(numb):
 for x in range(0,numb):
  tf.write('x')
def kilo():
 global tf
 tf=open('e:/fmaker.file','w')
 da=appuifw.query(ru('Число килобайт:'),'number')
 if da<=1024:
  kb(da)
  appuifw.note(ru('Выполнено\nВаш файл:\ne:/fmaker.file'),'info')
 if da>1024:
  appuifw.note(ru('Размер больше 1024kb,выберите "мегабайты"'),'error')

 tf.close()

def mega():
 global tf
 tf=open('e:/fmaker.file','w')
 da=appuifw.query(ru('Число мегабайт:'),'number')
 if da<=10:
  mb(da)
  appuifw.note(ru('Выполнено\nВаш файл:\ne:/fmaker.file'),'info')

 if da>10:
  appuifw.note(ru('Размер больше 10mb,выберите меньше'),'error')
 tf.close()

def b():
 global tf
 tf=open('e:/fmaker.file','w')
 da=appuifw.query(ru('Число байт:'),'number')
 if da<=1024:
  for x in range(0,da):
   tf.write('x')
  appuifw.note(ru('Выполнено\nВаш файл:\ne:/fmaker.file'),'info')

 if da>1024:
  appuifw.note(ru('Размер больше 1024b, выберите килобайты'),'error')
 tf.close()

appuifw.app.menu=[(ru('Байты (до 1k)'),b),(ru('Килобайты (до 1mb)'),kilo),(ru('Мегабайты (до 10mb)'),mega)]
ao.wait()