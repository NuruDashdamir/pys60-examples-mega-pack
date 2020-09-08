# encoding: utf-8
# 3D Tetris
# Author: Elrian (on www.dimonvideo.ru)
version=4.0
UID='fef4153d' #tetris3d

import appuifw, globalui, glcanvas, e32, random, graphics, os
from gles import *
from copy import copy,deepcopy
import key_codes as kc

def u(s):
  return s.decode('utf-8')

class Figure:
  """class for a figure of 1-4 blocks
  
  Attributes:
  pos - list of coordinates of cubes
  """
  def new(self):
    """new(self)->None reinitialises figure as it just started falling"""
    ftype=random.randrange(11)
    self.pos=[(0,-1,app.minz)]              # 0
    if ftype>0:                             # more than 1 cell
      self.pos.append((-1,-1,app.minz))     # 10
      if ftype<5:                           # not less than 3 cells in a line
        self.pos.append((1,-1,app.minz))    # 102
        if ftype==1:                        #
          self.pos.append((-2,-1,app.minz)) # 3102 
        elif ftype==2:                      #          3
          self.pos.append((-1,0,app.minz))  #          102
        elif ftype==3:                      #  3
          self.pos.append((0,0,app.minz))   # 102
      elif ftype>5:                         # not more than 2 cells in a line
        self.pos.append((0,0,app.minz))     #              10
        if ftype==6:                        #  23
          self.pos.append((1,0,app.minz))   # 10
        elif ftype==7:                      #         32
          self.pos.append((-1,0,app.minz))  #         10
        elif ftype==8:                      #  2
          self.pos.append((0,-1,app.minz+1))# 1+
        elif ftype==9:                      #          +
          self.pos.append((0,0,app.minz+1)) #         10
    rng=list(range(6))
    arg=[]
    for i in range(3):
      r=random.choice(rng)
      arg.append(r)
      rng.remove(r%3)
      rng.remove(r%3+3)
    arg.append(True)
    # because self.rotate(*arg,ignorefree=True) is a syntax error
    self.rotate(*arg)
    xs=[cube[0] for cube in self.pos]
    ys=[cube[1] for cube in self.pos]
    d=(((app.minx+app.maxx-1)-(min(xs)+max(xs)))//2,
      ((app.miny+app.maxy-1)-(min(ys)+max(ys)))//2,
      app.minz-min([cube[2] for cube in self.pos]))
    for j in range(len(self.pos)):
      self.pos[j]=list([self.pos[j][i]+d[i] for i in range(3)])
  
  def end(self):
    """end(self)->None prepares instance of class for deletion (breaks reference cycles if any)"""
    self.pos=None
    
  def move(self,dx,dy,dz):
    """move(self,dx,dy,dz)->None moves figure by dx,dy,dz if it is possible"""
    old_pos=self.pos
    self.pos=[(x+dx,y+dy,z+dz) for (x,y,z) in old_pos]
    if self.free(self.pos):
      app.canvas.drawNow()
      del old_pos
      return True
    else:
      self.pos=old_pos
      return False

  def free(self,pos):
    """free(self,pos)->bool rerurns True if pos is a correct position and it is entirely free of cubes otherwise False"""
    for cube in pos:
      if not ((app.minx<=cube[0]<app.maxx)and(app.miny<=cube[1]<app.maxy)and(app.minz<=cube[2]<app.maxz)and(app.isfree(*cube))):
        return False
    return True
  
  def rotate(self,xi,yi,zi,ignorefree=False):
    """rotate(self,xi,yi,zi)->None somehow transforms (may be rotates) figure
    
    0<=xi,yi,zi<=5 are numbers which mean what the corresponding coord will be
    number 0  1  2  3  4  5
    means  x  y  z -x -y -z
    For example, (x,y,z) after rotate(2,5,3) will become (z,-z,-x), however this rotation is useless
    More usefull example is .rotate(1,3,2) which rotates cw around axis z
    """
    old_pos=deepcopy(self.pos)
    abscoord=self.pos[0]
    ci=(xi,yi,zi)
    for j in range(len(self.pos)):
      transf=[self.pos[j][i]-abscoord[i] for i in range(3)]+[abscoord[i]-self.pos[j][i] for i in range(3)]
      self.pos[j]=tuple([abscoord[i]+transf[ci[i]] for i in range(3)])
    if not ignorefree:
      if self.free(self.pos):
        app.canvas.drawNow()
        old_pos=None
      else:
        self.pos=old_pos
  
  def release(self):
    """release(self)->int makes the falling figure part of fallen ones and returns the number of filled planes"""
    for cube in self.pos:
      app.setfree(False,*cube)
    count=0
    bottom=max([z for (x,y,z) in self.pos])
    while self.filled(bottom):
      count+=1
      for z in range(bottom-app.minz,0,-1):
        app.cubes[z]=app.cubes[z-1]
      app.cubes[0]=[[False for i in range(app.dy-1)] for j in range(app.dx-1)]
    return count
    
  def filled(self,n):
    """filled(self,n)->bool returns True if the plane n is all filled with cubes otherwise False"""
    plane=app.cubes[n-app.minz]
    for x in range(app.maxx-app.minx):
      for y in range(app.maxy-app.miny):
        if not plane[x][y]:
          return False
    return True




class Engine:
  """Main class containing most of functions and variables"""
  # almost all fields of class Engine:
  # screensize, screenaspect
  running=0    # 0-game not initialized or error happened, 1-game is running
  delay=1.0    # pause between figure falls one more cube down
  canvas=None  # canvas for drawing
  #minx, maxx = -3, 3 # min and max coordinates for points 
  #miny, maxy = -3, 3 # (but cubes must have coords less than max
  #minz, maxz = 3, 13 # (as there are n-1 gaps between n points))
  #dx, dy, dz=maxx-minx+1, maxy-miny+1, maxz-minz+1 # x,y,z dimensions. But the well is (dx-1)*(dy-1)*(dz-1) cubes
  #rx, ry, rz=range(minx,maxx+1), range(miny,maxy+1), range(minz,maxz+1)
  #points=array(GL_BYTE,3,[[x,y,-z] for z in rz for y in ry for x in rx]) # z needs to be actually negative because of glFrustumpf()
  #colortable=[((random.randrange(0x100)),(random.randrange(0x100)),(random.randrange(0x100)),0xff) for i in range(dz)]
  # colortable[i]=color used for all points with coord z=i
  #colors=array(GL_UNSIGNED_BYTE,4,[colortable[i] * (dx*dy) for i in range(dz)])
  lines=None # initialised at initgraphics() as it needs method xyz2ind()
  cubes=None # initialised at initgame(). cubes is a list of lists of lists of bool which shows is cube free
  # Use methods isfree() and setfree() rather than field cubes
  figure=[None,None]#[Figure() for i in range(2)] # falling and next figures
  score=0
  scoretable=(1,10,30,60,100)
  exit_type=0 # 0-exit 1-restart 2-show score
  
  def __init__(self):
    if self.optionsmenu():
      self.initgraphics()
      self.initgame()
  
  def optionsmenu(self):
    """self.optionsmenu(self)->shows self.options menu which lets user to change self.options, returns True if user presses play"""
    self.old_body=appuifw.app.body
    self.old_exit_key_handler=appuifw.app.exit_key_handler
    self.path='c:\\Private\\'+UID+'\\'
    self.needsave=0
    class OptionError(Exception):
      pass
    class Option:
      keynames={kc.EKeyLeftArrow:   'влево',
                kc.EKeyRightArrow:  'вправо',
                kc.EKeyUpArrow:     'вверх',
                kc.EKeyDownArrow:   'вниз',
                kc.EKeySelect:      'OK',
                kc.EKeyStar:        '*',
                kc.EKeyHash:        '#',
                kc.EKeyYes:         'зеленая',
                kc.EKeyNo:          'красная',
                kc.EKeyLeftSoftkey: 'левый софт',
                kc.EKeyRightSoftkey:'правый софт',
                kc.EKeyMenu:        'меню',
                kc.EKeyBackspace:   '<-',
                kc.EKeyEdit:        'карандаш',
                0:                  'нет клавиши'}
      def __init__(self,title,init,lst=None,func=lambda self:str(self.value)):
         self.title=title
         self.value=init
         self.lst=lst
         self.f=func
      def keyname(self):
        x=self.value
        if kc.EKey0<=x<=kc.EKey9:
          return str(x-kc.EKey0)
        if self.keynames.has_key(x):
          return self.keynames[x]
        else:
          return '#'+str(x)

    def play():
      self.running=1
      lock.signal()
    def default():
      try:
        if os.path.exists(self.path+'config.txt'):
          os.remove(self.path+'config.txt')
      except OSError:
        appuifw.note(u('Не вышло'),'error')
      else:
        self.needsave=0
        exit(1)
    def about():
      global version
      globalui.global_msg_query(u('3D Тетрис\nАвтор: Elrian\nВерсия: %s\nwww.dimonvideo.ru')%str(version),u('Об игре'),0)
    def thanks():
      globalui.global_msg_query(u(
'''Спасибо всем следующим людям:\n\
Elrian - куда ж без меня:)\n\
motix и vlad007700 - за дельные советы и замечания;\n\
REDNBLACK.sk, werton, K.U, Abdolban, Drfss07, keytujd, maxel85, Ithan, atrant и всем остальным (чьи ники, к сожалению, не сохранились), \
писавшим в комментариях к версиям 1.0-3.2 - за предложения и поддержку;\n\
Всем, еще напишущим в комментарии к версиям >= 4.0 - за  помощь в улучшении программы;\n\
Всем, качавшим файл с http://www.dimonvideo.ru/smart/uploader/4/208942/0/0 - за тестирование;\n\
Неизвестному программисту, еще давно написавшему 3D Tetris под DOS - за идею тетриса в 3D;\n\
DimonVideo - за замечательный сайт;\n\
Гвидо Ван Россуму - за создание языка программирования Python \
(который вообще-то читается как "пайтон" и не имеет никакого отношения к змеям, а только к шоу Monty Python’s Flying Circus);\n\
Персонально ТЕБЕ - за то, что читал все эти благодарности'''),u('Благодарности'),0)
    def exit(type=0):
      self.exit_type=type
      wanttoplay=0
      lock.signal()
    def change():
      c=self.canvas.current()
      if self.cur_tab==0:
        if c==0:
          r=appuifw.query(self.options[c].title,'float',self.options[c].value)
          if r!=None:
            if (0<=r<1.5):
              self.options[c].value=r
            else:
              appuifw.note(u('Скорость должна быть в пределах:\n0<=v<1.5'),'error')
        elif c==1:
          r=appuifw.query(self.options[c].title,'number',self.options[c].value)
          if r!=None:
            if (4<=r<=20)and(r%2==0):
              self.options[c].value=r
            else:
              appuifw.note(u('Ширина должна быть четной и в пределах:\n4<=x<=20'),'error')
        elif c==2:
          r=appuifw.query(self.options[c].title,'number',self.options[c].value)
          if r!=None:
            if (4<=r<=20)and(r%2==0):
              self.options[c].value=r
            else:
              appuifw.note(u('Длина должна быть четной и в пределах:\n4<=y<=20'),'error')
        elif c==3:
          r=appuifw.query(self.options[c].title,'number',self.options[c].value)
          if r!=None:
            if (4<=r<=20):
              self.options[c].value=r
            else:
              appuifw.note(u('Глубина должна быть в пределах:\n4<=z<=20'),'error')
      elif self.cur_tab==1:
        appuifw.app.body=appuifw.Canvas(event_callback=catch_key)
        appuifw.app.body.clear(0)
        appuifw.app.body.text((5,40),u('Нажми клавишу для:'),fill=0x00ff00)
        appuifw.app.body.text((40,80),self.keyopt[c].title,fill=0xff0000)
        appuifw.app.body.text((5,120),u('(не софткей и красную кнопку)'),fill=0x00ff00)
        appuifw.app.body.text((5,160),u('Очистка через 3 секунды'),fill=0x00ff00)
        appuifw.app.set_tabs([],None)
        self.options[c].value=0
        self.timer=e32.Ao_timer()
        self.timer.after(3,self.lock2.signal)
        self.lock2.wait()
        self.timer.cancel()
        appuifw.app.body=self.canvas
        appuifw.app.set_tabs([u('Игра'),u('Управление'),u('Экран')],tab_cb)
        appuifw.app.activate_tab(self.cur_tab)
      elif self.cur_tab==2:
        if c==0:
          orients=['automatic','portrait','landscape']
          r=appuifw.popup_menu([u(i) for i in self.options[c].lst],self.options[c].title)
          if r!=None:
            try:
              appuifw.app.orientation=orients[r]
              self.options[c].value=r
            except:
              appuifw.note(u('Смартфон не поддерживает смену ориентации!'),'error')
        elif c==1:
          r=appuifw.query(self.options[c].title,'number',self.options[c].value)
          if r!=None:
            if (0<=r<=255):
              self.options[c].value=r
            else:
              appuifw.note(u('Непрозрчачность должна быть в пределах от 0 до 255'),'error')
      self.needsave=1
      self.canvas.set_list([(opt.title,u(opt.f(opt))) for opt in self.options],c)
    def catch_key(event):
      if event['type']==appuifw.EEventKey:
        r=event['keycode']
        c=self.canvas.current()
        self.options[c].value=r
        self.lock2.signal()
    def tab_cb(n):
      self.cur_tab=n
      if n==0:
        self.options=self.gameopt
      elif n==1:
        self.options=self.keyopt
      elif n==2:
        self.options=self.screenopt
      self.canvas.set_list([(opt.title,u(opt.f(opt))) for opt in self.options],0)
    
    def saveoptions():
      # Why does most users have python 1.4.5? It doesn't even normally understand try-except-finally
      def x(s):
        return s.encode('utf-8')
      try:
        try:
          f=open(self.path+'config.txt','w')
          f.write('\xef\xbb\xbf') # BOM mark
          f.write('3D Tetris configuration\n')
          f.write('version/'+str(version)+'\n')
          for opt in self.gameopt:
            f.write('game/'+x(opt.title)+'/'+str(opt.value)+'\n')
          for opt in self.keyopt:
            f.write('key/'+x(opt.title)+'/'+str(opt.value)+'\n')
          for opt in self.screenopt:
            f.write('screen/'+x(opt.title)+'/'+str(opt.value)+'\n')
        except:
          appuifw.note(u('Настройки сохранить не удалось!'),'error')
      finally:
        try:
          f.close()
        except:
          pass
    
    def loadoptions():
      # Why does most users have python 1.4.5? It doesn't even normally understand try-except-finally
      try:
        try:
          f=open(self.path+'config.txt','r')
          s=f.readline()
          if s[:3]=='\xef\xbb\xbf': # BOM mark
            s=s[3:]
          if s!='3D Tetris configuration\n':
            raise OptionError('Ошибка в заголовке')
          s=f.readline()
          if s.split('/')[0]!='version':
            raise OptionError('Не указана версия')
          while 1:
            s=f.readline()
            if s=='':
              break
            else:
              s=s[:-1] # [:-1] is cool smile! Seriously I cut off \n
            s=u(s)
            p=s.split(u('/'))
            if len(p)!=3:
              raise OptionError('Не 2 слэша в строке')
            if p[0]==u('game'):
              self.options=self.gameopt
            elif p[0]==u('key'):
              self.options=self.keyopt
            elif p[0]==u('screen'):
              self.options=self.screenopt
            else:
              raise OptionError('Неизвестный префикс')
            for opt in self.options:
              if opt.title==p[1]:
                break
            else:
              raise OptionError('Атрибут не найден')
            try:
              if p[2].find('.')==-1:
                opt.value=int(p[2])
              else:
                opt.value=float(p[2])
            except:
              raise OptionError('Неверное значение')
        finally:
          f.close()
      except OptionError,e:
        appuifw.note(u('Плохой файл настроек: %s\nИсправлено.'%e),'conf')
        self.needsave=1
    
    self.gameopt=[Option(u('Скорость'),0.5),
                  Option(u('Ширина'),  6),
                  Option(u('Длина'),   6),
                  Option(u('Глубина'), 10)]
    
    self.keyopt= [Option(u('влево'),                kc.EKeyLeftArrow ,lambda:self.figure[0].move(-1,0,0),       lambda self:self.keyname()),
                  Option(u('вправо'),               kc.EKeyRightArrow,lambda:self.figure[0].move( 1,0,0),       lambda self:self.keyname()),  
                  Option(u('вверх'),                kc.EKeyUpArrow,   lambda:self.figure[0].move(0, 1,0),       lambda self:self.keyname()),
                  Option(u('вниз'),                 kc.EKeyDownArrow, lambda:self.figure[0].move(0,-1,0),       lambda self:self.keyname()),
                  Option(u('опустить'),             kc.EKeySelect,    lambda:self.figure[0].move(0,0, 1),       lambda self:self.keyname()),
                 #Option(u('скастовать магию'),     kc.EKeyBackspace, lambda:self.figure[0].move(0,0,-1),       lambda self:self.keyname()), # cheat!
                  Option(u('вращать пр ч. стрелки'),kc.EKey1,         lambda:self.figure[0].rotate(4,0,2),      lambda self:self.keyname()),
                  Option(u('вращать по ч. стрелке'),kc.EKey3,         lambda:self.figure[0].rotate(1,3,2),      lambda self:self.keyname()),
                  Option(u('вращать вперед'),       kc.EKey2,         lambda:self.figure[0].rotate(0,5,1),      lambda self:self.keyname()),
                  Option(u('вращать назад'),        kc.EKey5,         lambda:self.figure[0].rotate(0,2,4),      lambda self:self.keyname()),
                  Option(u('вращать налево'),       kc.EKey4,         lambda:self.figure[0].rotate(2,1,3),      lambda self:self.keyname()),
                  Option(u('вращать направо'),      kc.EKey6,         lambda:self.figure[0].rotate(5,1,0),      lambda self:self.keyname()),
                  #Option(u('подстройка управления'),kc.EKeyBackspace, lambda:self.resetwell(),                  lambda self:self.keyname()),
                  Option(u('камера пр ч. стрелки'), kc.EKey7,         lambda:self.rotatecam(+10.0,0.0,0.0,+1.0),lambda self:self.keyname()),
                  Option(u('камера по ч. стрелке'), kc.EKey9,         lambda:self.rotatecam(-10.0,0.0,0.0,+1.0),lambda self:self.keyname()),
                  Option(u('камера вперед'),        kc.EKey8,         lambda:self.rotatecam(+10.0,+1.0,0.0,0.0),lambda self:self.keyname()),
                  Option(u('камера назад'),         kc.EKey0,         lambda:self.rotatecam(-10.0,+1.0,0.0,0.0),lambda self:self.keyname()),
                  Option(u('камера налево'),        kc.EKeyStar,      lambda:self.rotatecam(+10.0,0.0,+1.0,0.0),lambda self:self.keyname()),
                  Option(u('камера направо'),       kc.EKeyHash,      lambda:self.rotatecam(-10.0,0.0,+1.0,0.0),lambda self:self.keyname()),
                  Option(u('камера сброс'),         kc.EKeyYes,       lambda:self.resetcam(),                   lambda self:self.keyname()),
                  Option(u('скриншот'),             kc.EKeyEdit,
                     lambda:graphics.screenshot().save('c:\\data\\Images\\3Dtetris'+str(random.randrange(10000))+'.jpg'),lambda self:self.keyname())]
    
    self.screenopt=[Option(u('Ориентация экрана'),0,  ['автоматически','портрет','ландшафт'], lambda self:self.lst[self.value]),
                    Option(u('Непрозрачн следующей'),127)]
    appuifw.app.screen='normal'
    lock=e32.Ao_lock()
    self.lock2=e32.Ao_lock()
    appuifw.app.title=u('3D Тетрис. Настройки.')
    appuifw.app.set_tabs([u('Игра'),u('Управление'),u('Экран')],tab_cb)
    appuifw.app.menu=[ (u('Играть'),play),(u('Стандартные настройки'),default),(u('Об игре'),about),(u('Благодарности'),thanks),(u('Выход'),exit)]
    appuifw.app.exit_key_handler=exit
    try:
      if not os.path.exists(self.path):
        os.mkdir(self.path)
      if os.path.exists(self.path+'config.txt'):
        try:
          loadoptions()
        except e:
          appuifw.note(u('Настройки загрузить не удалось!'),'error')
      else:
        needsave=1
    except:
      appuifw.note(u('Ошибка при создании каталога '+self.path+'. Не будет загрузки/сохранения настроек!'),'error')
    self.options=self.gameopt
    appuifw.app.body=self.canvas=appuifw.Listbox([(opt.title,u(opt.f(opt))) for opt in self.options], change)
    self.cur_tab=0
    appuifw.app.activate_tab(self.cur_tab)
    lock.wait()
    appuifw.app.set_tabs([],None)
    appuifw.app.menu=[]
    if self.needsave:
      saveoptions()
    if self.running==1:
      self.running=0
      appuifw.app.screen='full'
      self.delay=1.5-self.gameopt[0].value
      self.maxx=self.gameopt[1].value//2
      self.minx=-self.maxx
      self.dx=self.maxx-self.minx+1
      self.rx=range(self.minx,self.maxx+1)
      self.maxy=self.gameopt[2].value//2
      self.miny=-self.maxy
      self.dy=self.maxy-self.miny+1
      self.ry=range(self.miny,self.maxy+1)
      self.minz=3
      self.maxz=self.minz+self.gameopt[3].value
      self.dz=self.maxz-self.minz+1
      self.rz=range(self.minz,self.maxz+1)
      self.nextalpha=self.screenopt[1].value
      self.points=array(GL_BYTE,3,[[x,y,-z] for z in self.rz for y in self.ry for x in self.rx])
      self.colortable=[((random.randrange(0x100)),(random.randrange(0x100)),(random.randrange(0x100)),0xff) for i in range(self.dz)]
      self.colors=array(GL_UNSIGNED_BYTE,4,[self.colortable[i] * (self.dx*self.dy) for i in range(self.dz)])
      self.triangles=[array(GL_UNSIGNED_SHORT,3,  (i+self.dx*self.dy+1,i+1,i, i+self.dx*self.dy,i+self.dx*self.dy+1,i, i+self.dx*self.dy+self.dx,i+self.dx*self.dy,i, i+self.dx,i+self.dx*self.dy+self.dx,i, i+1,i+self.dx,i, i+self.dx*self.dy+self.dx,i+self.dx,i+self.dx+1, i+self.dx*self.dy+self.dx+1,i+self.dx*self.dy+self.dx,i+self.dx+1, i+self.dx*self.dy+1,i+self.dx*self.dy+self.dx+1,i+self.dx+1, i+1,i+self.dx*self.dy+1,i+self.dx+1, i+self.dx,i+1,i+self.dx+1)  )for i in range(self.dx*self.dy*self.dz)]
      #self.cubelines=[array(GL_UNSIGNED_SHORT,2,  [[j,j+self.dx] for j in (i,i+1,i+self.dx*self.dy,i+self.dx*self.dy+1)]+[[j,j+self.dx*self.dy] for j in (i,i+1,i+self.dx,i+self.dx+1)]+[[j,j+1] for j in (i,i+self.dx,i+self.dx*self.dy,i+self.dx*self.dy+self.dx)]  )for i in range(self.dx*self.dy*self.dz)]
      self.cubes=[[[False for i in range(self.dy-1)] for j in range(self.dx-1)] for k in range(self.dz-1)]
      return True
  
  def initgraphics(self):
    """initgraphics(self)->None initialises graphic part of the engine"""
    appuifw.app.title=u('3D Tetris')
    appuifw.app.body=self.canvas=glcanvas.GLCanvas(redraw_callback=self.redraw)
    appuifw.app.exit_key_handler=self.set_exit
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepthf(self.maxz+1.0)
    self.screensize=self.canvas.size
    #self.screenmin=min(self.screensize)
    self.screendif=self.screensize[1]-self.screensize[0] # >0 if vertical screen
    self.screenaspect=float(self.screensize[1])/float(self.screensize[0])
    self.resetcam()    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glVertexPointerb(self.points)
    glColorPointerub(self.colors)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glLineWidth(2.0)
    glShadeModel(GL_FLAT)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA) # to make transparency, rtfm opengl es specs!
    glViewport(0,0,*self.screensize)
    l0=[ (self.xyz2ind(self.minx,y, z),self.xyz2ind(self.maxx,y, z)) for z in self.rz for y in self.ry \
                                     if (y==self.miny)or(y==self.maxy)or(z==self.maxz)]  # lines parallel to OX
    l1=[ (self.xyz2ind(x,self.miny, z),self.xyz2ind(x,self.maxy, z)) for z in self.rz for x in self.rx \
                                     if (x==self.minx)or(x==self.maxx)or(z==self.maxz)]  # lines parallel to OY
    l2=[ (self.xyz2ind(x,y,self.minz),self.xyz2ind(x,y,self.maxz)) for y in self.ry for x in self.rx \
                                     if (x==self.minx)or(x==self.maxx)or(y==self.miny)or(y==self.maxy)] # to OZ
    #l0=[ (self.xyz2ind(self.minx,y, z),self.xyz2ind(self.maxx,y, z)) for z in self.rz for y in self.ry \
    #                                 if ((y==self.miny)or(y==self.maxy))and(z==self.maxz)]  # lines parallel to OX
    #l1=[ (self.xyz2ind(x,self.miny, z),self.xyz2ind(x,self.maxy, z)) for z in self.rz for x in self.rx \
    #                                 if ((x==self.minx)or(x==self.maxx))and(z==self.maxz)]  # lines parallel to OY
    #l2=[ (self.xyz2ind(x,y,self.minz),self.xyz2ind(x,y,self.maxz)) for y in self.ry for x in self.rx \
    #                                 if ((x==self.minx)or(x==self.maxx))and((y==self.miny)or(y==self.maxy))] # to OZ
    self.lines=array(GL_UNSIGNED_SHORT,2,l0+l1+l2)
  
  def initgame(self):
    """initgame(self)->None initialises non-graphical part of the engine"""
    for opt in self.keyopt:
      if opt.value!=0:
        self.canvas.bind(opt.value, opt.lst)
    self.figure=[Figure() for i in range(2)]
    self.running=1
  
  def end(self):
    """end(self)->None prepares instance of class for deletion (breaks reference cycles if any)"""
    appuifw.app.body=self.old_body
    appuifw.app.exit_key_handler=self.old_exit_key_handler
    self.canvas=None
    self.screensize=None
    self.points=None
    self.colortable=None
    self.colors=None
    self.lines=None
    self.cubelines=None
    self.cubes=None
    for i in range(2):
      if self.figure[i]:
        self.figure[i].end()
        self.figure[i]=None
    self.figure=None
  
  def isfree(self,x,y,z):
    """isfree(self,x,y,z)->bool returns True if there is no cube at (x,y,z) else False
    
    raises ValueError if not   minx<=x<maxx, miny<=y<maxy, minz<=z<maxz
    """
    if (self.minx<=x<self.maxx)and(self.miny<=y<self.maxy)and(self.minz<=z<self.maxz):
      return not self.cubes[z-self.minz][x-self.minx][y-self.miny] 
      # yes, [z][x][y], but not [x][y][z]. Becaus I use cubes[z] in isfilled()
    else:
      self.set_exit()
      raise ValueError('Invalid args for isfree(): %i,%i,%i'%(x,y,z))
  
  def setfree(self,value,x,y,z):
    """setfree(self,value,x,y,z)->None marks cube at (x,y,z) as free if value==True else marks it as not free
    
    raises ValueError if not   minx<=x<maxx, miny<=y<maxy, minz<=z<maxz
    """
    if (self.minx<=x<self.maxx)and(self.miny<=y<self.maxy)and(self.minz<=z<self.maxz):
      self.cubes[z-self.minz][x-self.minx][y-self.miny]=not value # see isfree()
    else:
      self.set_exit()
      raise ValueError('Invalid args for setfree(): %i,%i,%i,%i'%(x,y,z,value))
    
  
  def xyz2ind(self,x,y,z):
    """xyz2ind(self,x,y,z)->int returns index of a point (x,y,z) in points array
    
    raises ValueError if not   minx<=x<=maxx, miny<=y<=maxy, minz<=z<=maxz
    """
    if (self.minx<=x<=self.maxx)and(self.miny<=y<=self.maxy)and(self.minz<=z<=self.maxz):
      return (z-self.minz)*self.dx*self.dy + (y-self.miny)*self.dx + (x-self.minx)
    else:
      self.set_exit()
      raise ValueError('Invalid args for xyz2ind(): %i,%i,%i'%(x,y,z))
  
  def resetwell():
    pass
  
  def rotatecam(self,alpha,x,y,z):
    """rotatecam(self,a,x,y,z)->None rotates camera by alpha degrees, (x,y,z) is vector of rotation"""
    glMatrixMode(GL_PROJECTION)
    glTranslatef(0,0,-(self.minz+self.maxz)/2.0)
    glRotatef(alpha,x,y,z)
    glTranslatef(0,0,+(self.minz+self.maxz)/2.0)
    glMatrixMode(GL_MODELVIEW)
    app.canvas.drawNow()
  
  def resetcam(self):
    """resetcam(self)->None resets camera to its default position and angle"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #if self.screendif>0:
    #  glFrustumf(-1.0, 1.0, -1.0*(2*self.screenaspect-1.0), 1.0, self.minz-2, self.perspective) # TODO moar far edge!
    #  self.status[1]+=self.miny
    #else:
    #  glFrustumf(-1.0, 1.0*(2/self.screenaspect-1.0), -1.0, 1.0, self.minz-2, self.perspective) # TODO moar far edge!
    #  self.status=[self.maxx-self.status[1]-1,-self.status[0]-1,self.status[2]]
    glFrustumf(-1.0, 1.0, -1.0*self.screenaspect, 1.0*self.screenaspect, self.minz-2, 25.0)
    glMatrixMode(GL_MODELVIEW)
    self.canvas.drawNow()
    
  def drawcube(self,x,y,z):
    glDrawElementsus(GL_TRIANGLES,self.triangles[self.xyz2ind(x,y,z)])
    #glDrawElementsus(GL_LINE_STRIP,array(GL_UNSIGNED_SHORT,1,(a,b,c,d,h,g,f,e)))
    #glDrawElementsus(GL_LINES,array(GL_UNSIGNED_SHORT,2,(a,e, b,f, c,g)))
  
  def redraw(self,frame):
    """redraw(self,frame)->None redraws things on canvas"""
    if self.running==0:
      return
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glDrawElementsus(GL_LINES,self.lines)
    try:
      for (x,y,z) in self.figure[0].pos:
        self.drawcube(x,y,z)
    except Exception,e:
      appuifw.note(u"Exception inside redraw (figure.draw): %s" %(e))
      self.set_exit()
    try:
      for x in range(self.minx,self.maxx):
        for y in range(self.miny,self.maxy):
          for z in range(self.minz,self.maxz):
            if not self.isfree(x,y,z):
              self.drawcube(x,y,z)
    except Exception,e:
      appuifw.note(u"Exception inside redraw (cubes draw): %s" %(e))
      self.set_exit()
    try:
      for (x,y,z) in self.figure[1].pos:
        self.colors[self.xyz2ind(x,y,z)*4+3]=self.nextalpha
        self.colors[(self.xyz2ind(x,y,z)+self.dx+1)*4+3]=self.nextalpha
        self.drawcube(x,y,z)
        self.colors[self.xyz2ind(x,y,z)*4+3]=255
        self.colors[(self.xyz2ind(x,y,z)+self.dx+1)*4+3]=255
        pass
    except Exception,e:
      appuifw.note(u"Exception drawing next figure: %s" %(e))
      self.set_exit()
    
  def set_exit(self,type=0):
    """set_exit(self)->None marks that application needs to exit"""
    self.running=0
    self.exit_type=type
    #self.timer.cancel()
    # with previous line commented it takes about 1 sec for application to exit
    # but if you uncomment it it would take forever to exit - strange
    
  
  def run(self):
    """run(self)->None main application cycle"""
    try:
      if self.running==0:
        return
      self.timer=e32.Ao_timer()
      for i in range(2):
        self.figure[i].new()
      self.canvas.drawNow()
      while self.running==1:
        if not self.figure[0].move(0,0,1):
          self.score+=self.scoretable[self.figure[0].release()]
          self.figure[0].new()
          self.figure[0],self.figure[1]=self.figure[1],self.figure[0]
          self.canvas.drawNow()
          if not self.figure[0].free(self.figure[0].pos):
            self.set_exit(2)
        self.delay*=0.999
        self.timer.after(self.delay)
    finally:
      self.end()


while 1:
  try:
    app=Engine()
  except Exception,e:
    appuifw.note(u"Exception initializing 3D engine: %s" %(e))
    raise
  else:
    try:
      app.run()
    except Exception,e:
      appuifw.note(u"Error:%s%s"%(e,str(e.args)))
    if app.exit_type==0:
      break
    elif app.exit_type==2:
      if not appuifw.query(u('Ты набрал очков: %i\nХочешь еще одну попытку?')%app.score,'query'):
        break
app=None
appuifw.app.set_exit()