from socket import *
import appuifw,random,e32
run,rnd=1,random.Random()
def ru(x):return x.decode('utf-8')
def ext():
  global run
  fish.run=0
  lock.signal()
#  appuifw.app.set_exit()
appuifw.app.exit_key_handler=ext
class fishing:
  stat=''
  def __init__(self):
    self.s = socket(AF_BT, SOCK_STREAM)
    self.allfish=0
    self.S=False
    self.run=1
  def bind(self):
    if self.S:
      self.start()
      return
    try:
      self.s.bind(("", 9))
      self.stat=ru('Начинаем слушать порт...')
      self.S=True
      self.start()
    except:
      appuifw.note(ru('Ошибка запуска сначала убейте процесс obexmtmuiserver'),'error')
  def start(self):
    print ru('запуск рыбалки')
    while 1:
      nmb=rnd.uniform(0,9999999)
      lnd=rnd.uniform(0,99999999)
      sn=u"OBEX Object Push"
      print ru('Жду прихода сообщения')
      bt_advertise_service(sn, self.s, True, OBEX)
      print ru('Сервис OBEX включен ')
      try: 
         set_security(self.s, AUTH)
         receive_path = u"e:\\fishing\\obex.%s-%s"%(nmb,lnd)
         print ru('Прием идет в файл'), receive_path
         bt_obex_receive(self.s, receive_path)
         print ru('Принят файл %s'%receive_path)
         e32.ao_sleep(1)
         self.allfish+=1
      finally:
         bt_advertise_service(service_name, self.s, False, OBEX)
fish=fishing()
appuifw.app.menu=[(ru('Запуск'),lambda:e32.ao_sleep(0,fish.bind))]
lock=e32.Ao_lock()
lock.wait()
