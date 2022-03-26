#436372

import struct
import math
import e32
import audio 
import os
import appuifw

lock=e32.Ao_lock()

frequency=duration=volume=lista=listbox=0
p='d:\\au.au'

def koniec():
 if appuifw.query(u'Exit ?','query')==True: lock.signal()

def ton():
 f = open(p,'wb')
 f.write('.snd'+struct.pack('>5L',16,8*duration,2,8000,1))
 for i in range(duration*8):
  sin_i=math.sin(i*2*math.pi*frequency/8000)
  f.write(struct.pack('b', volume*127*sin_i))
 f.close()
 s=audio.Sound.open(p)
 s.play()
 while s.state()==2: e32.ao_yield()
 s.close()
 os.remove(p)

def wybierz():
 global frequency
 global duration
 global volume
 index=listbox.current()
 if lista[index][0]==u'Frequency (Hz)':
  q=appuifw.query(u'Frequency (Hz)','number',frequency)
  if q<>None: frequency=q; start()
 elif lista[index][0]==u'Duration (ms)':
  q=appuifw.query(u'Duration (ms)','number',duration)
  if q<>None: duration=q; start()
 elif lista[index][0]==u'Volume (1-10)':
  q=appuifw.query(u'Volume (1-10)','number',int(volume*10))
  if 0<=q<=10: volume=float(q)/float(10); start()
 elif lista[index][0]==u'Generate tone':
  ton()

def info():
 appuifw.note(u'pyGenerator 1.00'+u'\n'+'forum.gsmcenter.pl'+u'\n'+'kompiler@tlen.pl','info')

def start():
 global lista
 global listbox
 lista=[
(u'Generate tone',u''),(u'Frequency (Hz)',unicode(frequency)),(u'Duration (ms)',unicode(duration)),(u'Volume (1-10)',unicode(int(volume*10)))]
 appuifw.app.body=listbox=appuifw.Listbox(lista,wybierz)
 appuifw.app.exit_key_handler=koniec
 appuifw.app.menu=[(u'About',info)]

start()
lock.wait()
appuifw.app.set_exit()