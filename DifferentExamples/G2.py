import appuifw
from graphics import *
import e32
from key_codes import *

class Keyboard(object):
    """����� ������ � �����������. ����� ���� � ���������� �� ������-�� ������������ ����������"""
    def __init__(self,onevent=lambda:None):
        self._keyboard_state={}
        self._downs={}
        self._onevent=onevent
    def handle_event(self,event):
        if event['type'] == appuifw.EEventKeyDown:
            code=event['scancode']
            if not self.is_down(code):
                self._downs[code]=self._downs.get(code,0)+1
            self._keyboard_state[code]=1
        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']]=0
        self._onevent()
    def is_down(self,scancode):
        return self._keyboard_state.get(scancode,0)
    def pressed(self,scancode):
        if self._downs.get(scancode,0):
            self._downs[scancode]-=1
            return True
        return False

class mymain:
	"""�������� ������� ����������"""
	def __init__(self):
		appuifw.app.screen='full'
		self.img=None
		appuifw.app.body=self.canvas=appuifw.Canvas(event_callback=keyboard.handle_event,redraw_callback=self.handle_redraw)
		self.img=Image.new(self.canvas.size)
		appuifw.app.exit_key_handler=self.exit
		mymain.runninghelp=0
	def handle_redraw(self, rect):
		if self.img:
			self.canvas.blit(self.img)
    
	def exit(self):
		game.running=0
		self.running=0
		mymain.runninghelp=0
    

class game:
	"""�������� ������� �� ����� ����"""
	def __init__(self):
		self.blobsize=5
		self.location=[mymain.img.size[0]/2,mymain.img.size[1]/2]
		self.xs,self.ys=mymain.img.size[0]-self.blobsize,mymain.img.size[1]-self.blobsize
		self.dvigx=0
		self.dvigy=0
		self.linex1=mymain.img.size[0]/2-15
		self.liney1=mymain.img.size[1]-10
		self.linex2=mymain.img.size[0]/2+15
		self.liney2=mymain.img.size[1]-10
		self.s=0
		self.speed=1
		self.u=0
		self.blocks=0
		mymain.w=0
		keyboard.__init__()
		
	def keyselect(self):
			"""������������ ������� �� ��������"""
			if keyboard.is_down(EScancodeSelect) and self.s==0:
				self.s=1
				self.dvigy=-1
	def border(self):
			"""�� ��� ������ ������� �� ������� ������"""
			if self.location[0]>self.xs:
				self.dvigx=-self.dvigx
			if self.location[0]<self.blobsize/2:
				self.dvigx=abs(self.dvigx)
			if self.location[1]>self.ys:
				self.game_over()
			if self.location[1]<self.blobsize/2:
				self.dvigy=1
				
	def keysleftright(self):
			"""������������ ������� ����-�����"""
			if keyboard.is_down(EScancodeLeftArrow):
				if self.linex1>=0:
					self.linex1-=1
					self.linex2-=1
			if keyboard.is_down(EScancodeRightArrow):
				if self.linex2<=mymain.img.size[0]:
					self.linex1+=1
					self.linex2+=1
	
	def draw(self):
			"""������� ��������� ������ � �������"""
			mymain.img.point((self.location[0],self.location[1]),0x00ff00,width=self.blobsize)
			mymain.img.line((self.linex1,self.liney1,self.linex2,self.liney2),0xff00ee,width=2)
			mymain.handle_redraw(())
			e32.ao_yield()
	def win(self, num, level):
		"""���� ������� �������"""
		if self.blocks==num:
			appuifw.note(u"�� ��������!", "info")
			game.running=0
			mymain.w+=level
	def game_over(self):
		appuifw.note(u"�� ���������", "info")
		game.running=0
		keyboard.__init__()
	def pong(self):
		"""��������� ����� � �������"""
		if self.location[1]+self.blobsize/2==self.liney1 and self.linex1-self.blobsize/2<=self.location[0]<=self.linex2+self.blobsize/2:
			self.dvigy=-1
			delta=(self.linex2-self.linex1)/2+self.linex1
			if delta-1>self.location[0]:
				self.dvigx+=-1
			elif delta+1<self.location[0]:
				self.dvigx+=1
			if delta-5>self.location[0]:
				self.dvigx+=-1
			elif delta+5<self.location[0]:
				self.dvigx+=1
			if delta-10>self.location[0]:
				self.dvigx+=-1
			elif delta+10<self.location[0]:
				self.dvigx+=1
			self.u+=1
	def block(self,x1,y1,x2,y2,i):
		"""��������� ������ � �����"""
		if x1-self.blobsize+1<=self.location[0]<=x2+self.blobsize-1:
			if self.location[1]==self.blobsize/2+y2: self.dvigy=1; self.b[i]+=1; self.blocks+=1
			elif self.location[1]==y1-self.blobsize/2: self.dvigy=-1; self.b[i]+=1; self.blocks+=1
		if self.blobsize/2+y2>=self.location[1]>=y1-self.blobsize/2:
			if self.location[0]==x1-self.blobsize+1: self.dvigx=-1; self.b[i]+=1; self.blocks+=1
			elif self.location[0]==x2+self.blobsize-1: self.dvigx=1; self.b[i]+=1; self.blocks+=1

class level2(game):
	"""����� ��������� ������ �� �� �������� 5� �������."""
	def __init__(self):
		game.__init__(self)
		game.running=1
		self.b=range(17)
		while game.running:
			game.keyselect(self)
			game.keysleftright(self)
			i=0
			game.win(self,17,5)
			if abs(self.dvigx)>3: self.dvigx=3
			game.border(self)
			game.pong(self)
			mymain.img.clear(0)
			self.location[0]+=self.dvigx*self.speed
			self.location[1]+=self.dvigy*self.speed
    
			while 17>i:
				if self.b[i]==i:
					x1=i*10+1
					y1=1
					x2=i*10+10
					y2=10
					mymain.img.rectangle([x1,y1,x2,y2] ,outline=0x0000ff, fill=0x0000ff)
					game.block(self,x1,y1,x2,y2,i)
				i+=1
			game.draw(self)

class level1(game):
	"""����� ��������� ������. �� �� ��������� ������ 1-4."""
	def __init__(self, bloksss, rows, plusx, plusy, level):
		game.__init__(self)
		game.running=1
		self.b=range(bloksss)
		cols=bloksss/rows
		x=0
		while game.running:
			e32.ao_sleep(float((24-bloksss))/800.0)
			game.keyselect(self)
			game.keysleftright(self)
			i=0
			game.win(self,bloksss,level)
			if abs(self.dvigx)>3: self.dvigx=3
			game.border(self)
			game.pong(self)
			mymain.img.clear(0)
			self.location[0]+=self.dvigx*self.speed
			self.location[1]+=self.dvigy*self.speed
			
			row=1
			while bloksss>i:
				if i>=row*cols:
					row+=1
				if self.b[i]==i:
					x1=i*10+plusx+1-(row-1)*cols*10
					x2=i*10+plusx+10-(row-1)*cols*10
					y1=row*10+plusy+1
					y2=row*10+plusy+10
					mymain.img.rectangle([x1,y1,x2,y2] ,outline=0x0000ff, fill=0x0000ff)
					game.block(self,x1,y1,x2,y2,i)
				i+=1
			game.draw(self)			

class mymenu:
	"""����� ����"""
	def __init__(self):
		m=1
		r=0; g=0; b=0
		check=0
		bg=(0,0,0)
		mymain.running=1
		array=[u"\u041d\u0430\u0447\u0430\u0442\u044c \u0438\u0433\u0440\u0443", u"\u041f\u043e\u043c\u043e\u0449\u044c", u"\u0412\u044b\u0445\u043e\u0434"]
		while mymain.running:
			if check==0: r+=5
			elif check==1: r-=5
			elif check==2: g+=5
			elif check==3: g-=5
			elif check==4: b+=5
			elif check==5: b-=5
			if r==70: check=1
			elif r==0 and check==1: check=2
			elif g==70: check=3
			elif g==0 and check==3: check=4
			elif b==70: check=5
			elif b==0 and check==5: check=0			
			bg=(r,g,b)
			mymain.img.clear(bg)
			mymain.img.line((30,25,150,25),0xffffff,width=2)
			mymain.img.line((30,25,30,90),0xffffff,width=2)
			mymain.img.line((150,25,150,90),0xffffff,width=2)
			mymain.img.line((30,90,150,90),0xffffff,width=2)
			mymain.img.rectangle((32,27,148,88) ,outline=0x000000, fill=0x000000)
			if m==1:
				self.text(array, 1)
			elif m==2:
				self.text(array, 2)
			elif m==3:
				self.text(array, 3)
			if keyboard.is_down(EScancodeUpArrow):
				if m>1: m-=1
				e32.ao_sleep(0.2)
			if keyboard.is_down(EScancodeDownArrow):
				if m<3: m+=1
				e32.ao_sleep(0.2)
			if keyboard.is_down(EScancodeSelect):
				if m==1:
					level=level1(1, 1, mymain.img.size[0]/2-(3*11/2), 20,1)
					if mymain.w>=1: level=level1(4, 1, mymain.img.size[0]/2-(3*11/2), 20,2)
					if mymain.w>=2: level=level1(8, 2, mymain.img.size[0]/2-(3*11/2), 20,3)
					if mymain.w>=3: level=level1(16, 4, mymain.img.size[0]/2-(3*11/2), 20,4)
					if mymain.w>=4: level=level2()
				elif m==2:
					help()
					e32.ao_sleep(0.1)
				elif m==3: mymain.exit()
			mymain.handle_redraw(())
			e32.ao_yield()	
	def text(self, text, select):
		"""����� ������ � ����"""
		i=1
		for string in text:
			y=i*20+20
			if i==select: f=u"LatinBold13"
			else: f=u"LatinPlain12"
			mymain.img.text((35,y), string, 0xffffff, font=f)
			i+=1
class help:
	"""����� ����������� ������"""
	def __init__(self):
		mymain.runninghelp=1
		e32.ao_sleep(0.5)
		while mymain.runninghelp:
			if keyboard.is_down(EScancodeSelect):
				mymain.runninghelp=0
			mymain.img.clear(0)
			mymain.img.text((0,10), u"(c) Cyxapeff",0xffffff)
			mymain.handle_redraw(())
			e32.ao_yield()	
keyboard=Keyboard()
mymain=mymain()
mymenu=mymenu()