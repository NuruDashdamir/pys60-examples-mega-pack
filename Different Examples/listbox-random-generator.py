# Lottomat 1.00
# 0xe8568866
# kompiler@tlen.pl

import appuifw
import random

lock=appuifw.e32.Ao_lock()
p=49
i=6
los=''

def losowanie():
 global los
 global lista
 global listbox
 k=range(1,p+1)
 random.shuffle(k)
 los=''
 kl=[]
 for q in range(i): 
  try: kl.append(k[q])
  except: kl.append('?')
 kl.sort()
 for q in range(len(kl)): los=los+str(kl[q])+','
 los=los[0:len(los)-1]
 lista=[(u'Random numbers',unicode(los)),(u'Settings',unicode(str(i)+' from '+str(p)))] 
 appuifw.app.body = listbox = appuifw.Listbox(lista, wybierz)

def info():
 appuifw.note(u'Lottomat 2.10'+u'\n'+u'forum.gsmcenter.pl'+u'\n'+u'kompiler@tlen.pl','info')
 appuifw.note(u'English version for'+u'\n'+u'symbian-freak.com','info')

def koniec():
 if appuifw.query(u'Exit ?','query')==True: 
  lock.signal()

def wybierz():
 global lista
 global listbox
 global i
 global p
 index = listbox.current()
 if lista[index][0]==u'Settings':
  g=q=0
  lista=[(u'Random numbers',u''),(u'Settings',u'')] 
  appuifw.app.body = listbox = appuifw.Listbox(lista, wybierz)
  while q<>None:
   q=appuifw.query(u'('+unicode(str(i)+') from '+str(p)),'number',i)
   if q<>None:
    if q>10: appuifw.note(u'Maks (10)','info')
    elif q<1: appuifw.note(u'Min (1)','info')
    else: 
     i=q
     q=None
     g=1
  if g>0:
   while g<>None:
    g=appuifw.query(unicode(str(i)+' from ('+str(p))+u')','number',p-1)
    if g<>None:
     if g>100: appuifw.note(u'Maks (100)','info')
     elif g<1: appuifw.note(u'Min (1)','info')
     else: 
      p=g
      g=None
  losowanie()
 if lista[index][0]==u'Random numbers': losowanie()

lista=[(u'Random numbers',unicode(los)),(u'Settings',unicode(str(i)+' from '+str(p)))] 
appuifw.app.body = listbox = appuifw.Listbox(lista, wybierz)
appuifw.app.exit_key_handler=koniec
appuifw.app.title=u'Lottomat'
appuifw.app.menu=[(u'About',info)]
lock.wait()
appuifw.app.set_exit()