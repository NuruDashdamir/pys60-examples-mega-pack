###Seldon86

import os,e32,time,appuifw
aa=appuifw.app

def ru(t):return t.decode('utf-8')
def ur(t):return t.encode('utf-8')

class FileMan:
 def __init__(s,EXT=''):
  s.PATHHISTORY,s.PATHACTIVE,s.ALLFILES,s.SELECTFILES,s.LISTBOX=[['',0]],'',[],[],[u'']
  s.setext(EXT)
 def numbout(s):app.text('Помечено для обработки: '+str(len(s.SELECTFILES))+'.')
 def setext(s,EXT):
  s.FILTEREXT,s.FILTERFILE=[],0
  if len(EXT)!=0:
   s.FILTERFILE=1
   for i in ur(EXT).split(','):s.FILTEREXT.append(i.lower())
 def reset(s):
  s.__init__()
  s.back()
 def exit(s):
  s.PATHHISTORY.append([s.PATHACTIVE,s.BODY.current()])
  aa.screen,aa.menu,aa.body,aa.exit_key_handler=s.OLDSTATE
  s.numbout()
 def run(s):
  s.OLDSTATE=[aa.screen,aa.menu,aa.body,aa.exit_key_handler]
  aa.screen,aa.exit_key_handler='full',s.exit
  s.BODY=aa.body=appuifw.Listbox(s.LISTBOX,s.exchange)
  aa.menu=[
   (ru('Сбросить'),s.reset),
   (ru('Выделение'),
   ((ru('отметить всё'),lambda:s.exchange(1)),
    (ru('снять всё'),lambda:s.exchange(2)),
    (ru('инвертировать всё'),lambda:s.exchange(3)))),
   (ru('Выход'),s.exit)]
  s.BODY.bind(63495,s.back)
  s.BODY.bind(63496,s.forward)
  s.BODY.bind(63499,s.exchange)
  s.BODY.bind(48,s.reset)
  s.BODY.bind(49,lambda:s.exchange(1))
  s.BODY.bind(50,lambda:s.exchange(2))
  s.BODY.bind(51,lambda:s.exchange(3))
  s.back()
 def forward(s):
  pa=s.PATHACTIVE+s.ALLFILES[s.BODY.current()]+'/'
  if not os.path.isdir(pa):return
  af=s.listdir(pa)
  if len(af)==0:return
  s.PATHHISTORY.append([s.PATHACTIVE,s.BODY.current()])
  s.PATHACTIVE,s.ALLFILES=pa,af
  s.setlist()
 def back(s):
  if len(s.PATHHISTORY)==0:return
  ph=s.PATHHISTORY.pop()
  s.PATHACTIVE=ph[0]
  if s.PATHACTIVE=='':s.ALLFILES=['c:','e:']
  else:s.ALLFILES=s.listdir(s.PATHACTIVE)
  s.setlist(ph[1])
 def exchange(s,n=0):
  if n==0:
   f=s.PATHACTIVE+s.ALLFILES[s.BODY.current()]
   if os.path.isfile(f):
    try:s.SELECTFILES.remove(f)
    except:s.SELECTFILES.append(f)
  else:
   for i in s.ALLFILES:
    f=s.PATHACTIVE+i
    if os.path.isfile(f):
     if n==1:
      try:s.SELECTFILES.index(f)
      except:s.SELECTFILES.append(f)
     elif n==2:
      try:s.SELECTFILES.remove(f)
      except:pass
     elif n==3:
      try:s.SELECTFILES.remove(f)
      except:s.SELECTFILES.append(f)
  s.setlist(s.BODY.current())
 def setlist(s,c=0):
  s.LISTBOX=[]
  for i in s.ALLFILES:
   if s.PATHACTIVE+i in s.SELECTFILES:s.LISTBOX.append(ru('+'+i))
   else:s.LISTBOX.append(ru(' '+i))
  s.BODY.set_list(s.LISTBOX,c)
 def listdir(s,DIR):
  if s.FILTERFILE:
   LIST=[]
   for i in os.listdir(DIR):
    if os.path.isfile(DIR+i):
     if os.path.splitext(i)[1][1:].lower() in s.FILTEREXT:LIST.append(i)
    elif os.path.isdir(DIR+i):LIST.append(i)
   return LIST
  else:return os.listdir(DIR)
fileman=FileMan()

class Rename:
 def __init__(s):
  s.SETPATH=':/system/apps/Rename/setting.txt'
  s.setload()
 def setload(s):
  try:
   try:FILE=open('c'+s.SETPATH,'r',4098)
   except:FILE=open('e'+s.SETPATH,'r',4098)
   FILE=open('e'+s.SETPATH,'r',4098)
   EVENTS=FILE.read().splitlines()
   FILE.close()
   s.setevents(EVENTS)
  except:s.setevents()
 def setsave(s):
  fileman.setext(s.FILTEREXT)
  try:FILE=open('c'+s.SETPATH,'w',4098)
  except:FILE=open('e'+s.SETPATH,'w',4098)
  FILE.write(ur(s.MASKNAME)+'\n'+ur(s.MASKEXT)+'\n'+str(s.REGNAME)+'\n'+str(s.REGEXT)+'\n'+str(s.SPACE)+'\n'+ur(s.SEARCH)+'\n'+ur(s.REPLACE)+'\n'+str(s.COUNTSTART)+'\n'+str(s.COUNTSTEP)+'\n'+str(s.COUNTDIGITS)+'\n'+str(s.FORMAT)+'\n'+str(s.WIDTH)+'\n'+ur(s.FILTEREXT)+'\n'+str(s.LITEADDFUNC)+'\n'+ur(s.LITENEWNAME)+'\n'+ur(s.DIVSIMVOL)+'\n')
  FILE.close()
  fileman.numbout()
 def setevents(s,e=['!N','!E',0,0,0,'','',0,1,1,0,0,'',1,'','_']):
  s.MASKNAME,s.MASKEXT,s.REGNAME,s.REGEXT,s.SPACE,s.SEARCH,s.REPLACE,s.COUNTSTART,s.COUNTSTEP,s.COUNTDIGITS,s.FORMAT,s.WIDTH,s.FILTEREXT,s.LITEADDFUNC,s.LITENEWNAME,s.DIVSIMVOL=ru(e[0]),ru(e[1]),int(e[2]),int(e[3]),int(e[4]),ru(e[5]),ru(e[6]),int(e[7]),int(e[8]),int(e[9]),int(e[10]),int(e[11]),ru(e[12]),int(e[13]),ru(e[14]),ru(e[15])
  fileman.setext(s.FILTEREXT)
 def setstand(s):
  s.setevents()
  s.setsave()
 def setfull(s):
  s.setload()
  FORM=appuifw.Form([
  (ru('Маска имени'),'text',s.MASKNAME),
  (ru('Маска расш-ия'),'text',s.MASKEXT),
  (ru('Регистр имени'),'combo',([
   ru('Без изменений'),
   ru('Всё в нижнем'),
   ru('Всё в ВЕРХНЕМ'),
   ru('Первая буква в верхнем'),
   ru('Начало Слов В Верхнем'),
   ru('Инвертировать')],s.REGNAME)),
  (ru('Регистр расш-ия'),'combo',([
   ru('Без изменений'),
   ru('Всё в нижнем'),
   ru('Всё в ВЕРХНЕМ'),
   ru('Первая буква в верхнем'),
   ru('Инвертировать')],s.REGEXT)),
  (ru('Удаление пробелов'),'combo',([
   ru('Отключено'),
   ru('Все'),
   ru('В начале'),
   ru('В конце'),
   ru('В начале и в конце')],s.SPACE)),
  (ru('Найти'),'text',s.SEARCH),
  (ru('Заменить на'),'text',s.REPLACE),
  (ru('Начало счётчика'),'number',s.COUNTSTART),
  (ru('Шаг счётчика'),'number',s.COUNTSTEP),
  (ru('Кол-во цифр в счётчике'),'number',s.COUNTDIGITS),
  (ru('Выравнивание'),'combo',([
   ru('Отключено'),
   ru('По левому краю'),
   ru('По центру'),
   ru('По правому краю')],s.FORMAT)),
  (ru('Ширина строки'),'number',s.WIDTH),
  (ru('Расш-ие для фильтр-ии'),'text',s.FILTEREXT)],
  appuifw.FFormEditModeOnly|appuifw.FFormDoubleSpaced)
  FORM.execute()
  s.MASKNAME,s.MASKEXT,s.REGNAME,s.REGEXT,s.SPACE,s.SEARCH,s.REPLACE,s.COUNTSTART,s.COUNTSTEP,s.COUNTDIGITS,s.FORMAT,s.WIDTH,s.FILTEREXT=FORM[0][2],FORM[1][2],FORM[2][2][1],FORM[3][2][1],FORM[4][2][1],FORM[5][2],FORM[6][2],FORM[7][2],FORM[8][2],FORM[9][2],FORM[10][2][1],FORM[11][2],FORM[12][2]
  s.setsave()
 def setlite(s):
  s.setload()
  FORM=appuifw.Form([
  (ru('Разделитель'),'text',s.DIVSIMVOL),
  (ru('Новое имя'),'text',s.LITENEWNAME),
  (ru('Дополнительно'),'combo',([
   ru('Отключено'),
   ru('Счётчик'),
   ru('Время'),
   ru('Дата')],s.LITEADDFUNC)),
  (ru('Начало счётчика'),'number',s.COUNTSTART),
  (ru('Шаг счётчика'),'number',s.COUNTSTEP),
  (ru('Кол-во цифр в счётчике'),'number',s.COUNTDIGITS),
  (ru('Расш-ие для фильтр-ии'),'text',s.FILTEREXT)],
  appuifw.FFormEditModeOnly|appuifw.FFormDoubleSpaced)
  FORM.execute()
  s.DIVSIMVOL,s.LITENEWNAME,s.LITEADDFUNC,s.COUNTSTART,s.COUNTSTEP,s.COUNTDIGITS,s.FILTEREXT=FORM[0][2],FORM[1][2],FORM[2][2][1],FORM[3][2],FORM[4][2],FORM[5][2],FORM[6][2]
  if len(s.LITENEWNAME)==0:s.MASKNAME='!N'
  else:s.MASKNAME=s.LITENEWNAME
  if s.LITEADDFUNC==1:s.MASKNAME+=','+s.DIVSIMVOL+',!C'
  elif s.LITEADDFUNC==2:s.MASKNAME+=','+s.DIVSIMVOL+',!T'
  elif s.LITEADDFUNC==3:s.MASKNAME+=','+s.DIVSIMVOL+',!D'
  s.MASKEXT='!E'
  s.setsave()
 def start(s):
  app.text('Идет обработка.')
  s.OLDSELECTFILES,s.NEWSELECTFILES,s.ERRORFILES,I,YMD,HMS,COUNTFLAG=[],[],[],0,time.strftime('%Y%m%d%'),time.strftime('%H%M%S'),0
  if (s.MASKNAME.find('!C')!=-1)|(s.MASKEXT.find('!C')!=-1):COUNTNUMBER,COUNTFLAG=s.COUNTSTART-s.COUNTSTEP,1
  while len(fileman.SELECTFILES)!=0:
   i=fileman.SELECTFILES[0]
   del fileman.SELECTFILES[0]
   if COUNTFLAG:
    COUNTNUMBER+=s.COUNTSTEP
    COUNTTEXT=str(COUNTNUMBER).rjust(s.COUNTDIGITS).replace(' ','0')
   t1=os.path.split(i)
   t2=os.path.splitext(t1[1])
   PATH,OLDNAME,OLDEXT,NEWNAME,NEWEXT=ru(t1[0]),ru(t2[0]),ru(t2[1][1:]),'',''
   for j in s.MASKNAME.split(','):
    if j.find('!')!=-1:
     if j[1]=='N':
      d=j[2:].split('-')
      if len(d)==2:
       NEWNAME+=OLDNAME[int(d[0]):int(d[1])]
      else:NEWNAME+=OLDNAME
     elif j=='!D':NEWNAME+=YMD
     elif j=='!T':NEWNAME+=HMS
     elif j=='!C':NEWNAME+=COUNTTEXT
    else:NEWNAME+=j
   for j in s.MASKEXT.split(','):
    if j.find('!')!=-1:
     if j[1]=='E':
      d=j[2:].split('-')
      if len(d)==2:
       NEWEXT+=OLDEXT[int(d[0]):int(d[1])]
      else:NEWEXT+=OLDEXT
     elif j=='!C':NEWEXT+=COUNTTEXT
    else:NEWEXT+=j
   if len(s.SEARCH)!=0:NEWNAME=NEWNAME.replace(s.SEARCH,s.REPLACE)
   if s.REGNAME==1:NEWNAME=NEWNAME.lower()
   elif s.REGNAME==2:NEWNAME=NEWNAME.upper()
   elif s.REGNAME==3:NEWNAME=NEWNAME[0].upper()+NEWNAME[1:]
   elif s.REGNAME==4:
    if len(NEWNAME)!=0:
     nn=''
     for k in NEWNAME.split(' '):
      nn+=k[0].upper()+k[1:]+' '
     NEWNAME=nn[:-1]
   elif s.REGNAME==5:NEWNAME=NEWNAME.swapcase()
   if s.REGEXT==1:NEWEXT=NEWEXT.lower()
   elif s.REGEXT==2:NEWEXT=NEWEXT.upper()
   elif s.REGEXT==3:NEWEXT=NEWEXT[0].upper()+NEWEXT[1:]
   elif s.REGEXT==4:NEWEXT=NEWEXT.swapcase()
   if s.SPACE==1:NEWNAME=NEWNAME.replace(' ','')
   elif s.SPACE==2:NEWNAME=NEWNAME.lstrip()
   elif s.SPACE==3:NEWNAME=NEWNAME.rstrip()
   elif s.SPACE==4:NEWNAME=NEWNAME.strip()
   if s.FORMAT==1:NEWNAME=NEWNAME.ljust(s.WIDTH)
   elif s.FORMAT==2:NEWNAME=NEWNAME.center(s.WIDTH)
   elif s.FORMAT==3:NEWNAME=NEWNAME.rjust(s.WIDTH)
   p=ur(PATH+'/'+NEWNAME+'.'+NEWEXT)
   try:
    os.rename(i,p)
    s.OLDSELECTFILES.append(i)
    s.NEWSELECTFILES.append(p)
    I+=1
    app.text('Обработано: '+str(I)+'.')
   except:s.ERRORFILES.append(i)
  fileman.SELECTFILES=s.ERRORFILES
  if len(s.ERRORFILES)==0:app.text('Успешно обработано: '+str(len(s.NEWSELECTFILES))+'.')
  else:app.text('Успешно обработано: '+str(len(s.NEWSELECTFILES))+'.\nНеудалось обработать: '+str(len(s.ERRORFILES))+'.\nВозможные причины: отсутствие доступа к файлу, наличие файлов с одинаковыми именами и расширениями.')
 def cancel(s):
  app.text('Идет обработка.')
  I=0
  for i in xrange(len(s.OLDSELECTFILES)):
   os.rename(s.NEWSELECTFILES[i],s.OLDSELECTFILES[i])
   I+=1
   app.text('Обработано: '+str(I)+'.')
  fileman.SELECTFILES+=s.OLDSELECTFILES
  fileman.numbout()
rename=Rename()

class Exit:
 def __init__(s):s.AOLOCK=e32.Ao_lock()
 def wait(s):s.AOLOCK.wait()
 def call(s):
  s.AOLOCK.signal()
  aa.set_exit()
exit=Exit()

class App:
 def __init__(s):
  aa.screen,aa.exit_key_handler='normal',exit.call
  aa.menu=[
  (ru('Файлменеджер'),fileman.run),
  (ru('Настройки'),(
   (ru('полные'),rename.setfull),
   (ru('облегченные'),rename.setlite),
   (ru('стандартные'),rename.setstand))),
  (ru('Начать'),rename.start),
  (ru('Откат'),rename.cancel),
  (ru('Выход'),exit.call)]
  aa.body=appuifw.Text()
  aa.body.color=(0,0,0)
  s.text('Программа готова к работе.')
 def text(s,t,f=False):
  aa.body.set(ru(t))
  aa.body.set_pos(0)
  aa.body.focus=f
  e32.ao_sleep(0.001)
app=App()

exit.wait()