import appuifw
import e32

app_lock=e32.Ao_lock()

def exit_key_handler():
    app_lock.signal()

appuifw.app.body=k=appuifw.Canvas()

m=0
c=0
k.point((10,10),0xff0000,width=15)
#рисуем нашу точку
def point():
  global m
  k.point((10+m,10+c),0xff0000,width=15)
#задаем функцию её прорисовки с переменными
def pravo():
  global m
  if m<176:
    m+=1
    k.clear()
  else:pass
  point()
#рассмотрим на примере задания передвижения вниз.Делаем функцию.В ней делаем цикл,который будет изменять глобальную переменную очищаем экран,чтобы не осталось следа.В конце функции возвращаем нашу функцию прорисовки точки через глобальные переменные. остальное делайте по примеру.
def levo():
  global m
  if m>0:
    m-=1
    k.clear()
  else:pass
  point()

def up():
  global c
  if c>0:
    c-=1
    k.clear()
  else:pass
  point()

def down():
  global c
  if c<208:
    c+=1
    k.clear()
  else:pass
  point()

k.bind(63495,levo)
k.bind(63496,pravo)
k.bind(63497,up)
k.bind(63498,down)
appuifw.app.exit_key_handler = exit_key_handler

app_lock.wait()