import appuifw
import e32


app_lock=e32.Ao_lock()
def exit_key_handler():
    app_lock.signal()
#делаем выход на правый софт
appuifw.app.exit_key_handler = exit_key_handler
#возвращаем функцию на правый софт
def ru(x):
  return x.decode('utf-8')
#пишем на русском языке

def windows1():

  appuifw.app.body=k=appuifw.Canvas()
#задаем графическое окно
  k.clear(0x000000)
#задаем цвет фона
  k.text((5,15),ru('первое окно'),0xffffff,font=u'alp13')
#пишем надпись
windows1()

def windows2():
  appuifw.app.body=k=appuifw.Canvas()
#задаем графическое окно
  k.clear(0x000000)
#задаем цвет фона
  k.text((5,15),ru('второе окно'),0xffffff,font=u'alp13')
#пишем надпись
  def nazad():
    windows1()
  appuifw.app.menu=[(ru('назад'),windows1)]

appuifw.app.menu=[(ru('вперед'),windows2)]

app_lock.wait()


