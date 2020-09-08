#  graph_plus.py
#
#  MACTEP3230
#
__version__='1.09'
import graphics

def fill(self,(x,y),color,callback=lambda:False):
  def check(image,(x,yu,yd),c,label,queue):
    iu=yu
    if image.getpixel((x,iu))[0]==c and label[x][iu]: f=0
    else: f=1
    while iu>=0 and label[x][iu] and image.getpixel((x,iu))[0]==c: iu-=1
    iu+=1
    i=iu
    id=yu
    for id in range(yu,yd):
      if label[x][id] and image.getpixel((x,id))[0]==c:
        if f: f=0; i=id
      else:
        if f==0:
          queue.append((x,i,id))
          f=1
    if f==0:
      while id<image.size[1] and label[x][id] and image.getpixel((x,id))[0]==c: id+=1
      queue.append((x,i,id))
    label[x][iu:id]=(id-iu)*[False]

  label=[]
  queue=[]
  width=self.size[0]
  if not(0<=x<width and 0<=y<self.size[1]):
    return
  if type(color)==type(1):
    cr=(color>>16)&255
    cg=(color>>8)&255
    cb=color&255
    color=(cr,cg,cb)
  c=self.getpixel((x,y))[0]
  if color==c:
    return
  for i in range(width):
    label.append([True]*self.size[1])
  check(self,(x,y,y+1),c,label,queue)
  while len(queue)>0 and not callback():
    x,yu,yd=queue.pop(0)
    self.line((x,yu,x,yd),color)
    if x>0: check(self,(x-1,yu,yd),c,label,queue)
    if x<width-1: check(self,(x+1,yu,yd),c,label,queue)
  queue=[]
  label=[]

graphics.Image.fill=fill

def scroll(self,n,c=0xffffff):
  if n<0:
    if n<=-self.size[1]:
      self.clear(c)
    else:
      temp=graphics.Image.new(self.size)
      temp.clear(c)
      temp.blit(self,(0,0,self.size[0],self.size[1]-n),(0,-n))
      self.blit(temp)
  elif n>0:
    if n>=self.size[1]:
      self.clear(c)
    else:
      temp=graphics.Image.new(self.size)
      temp.clear(c)
      temp.blit(self,(0,n,self.size[0],self.size[1]),(0,0))
      self.blit(temp)

graphics.Image.scroll=scroll

def printxt(self,(x,y),text,color=0,fnt=u"latinbold12"):

  class font:
    def __init__(self,name=u'latinplain12'):
      par=graphics.Image.new((0,0)).measure_text(u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,\'?!"-()@/:_;+&%*=<>$[]{}\\~^#| ',fnt)[0]
      self.name=name
      self.size=-par[1]
      self.height=par[3]-par[1]

  def new_line(img,(x,y),f):
      x=1
      y+=f.height+1
      n=img.size[1]-f.height+f.size
      if y>n:
        img.scroll(y-n)
        y=n
      return (x,y)
    
  def find_len(img,s,x,f):
      i=0
      for i in range(len(s)):
        l=img.measure_text(s[:i+1],f.name)[1]
        if l+x>img.size[0]:
          return (i,l)
      return (len(s),img.measure_text(s,f.name)[1])
        
  def print_string(img,(x,y),string,color,font):
    while string!='':
      n,l=find_len(img,string,x,font)
      if n==0:
        x,y=new_line(img,(x,y),font)
        n,l=find_len(img,string,x,font)
      img.text((x,y),string[:n],color,font.name)
      x+=l
      string=string[n:]
    return (x,y)

  f=font(fnt)
  txt=text[:]
  while txt!='':
    max=txt.find(u'\n')
    if max==-1:
      return print_string(self,(x,y),txt,color,f)
    x,y=print_string(self,(x,y),txt[:max],color,f)
    x,y=new_line(self,(x,y),f)
    txt=txt[max+1:]
  return (x,y)
  
graphics.Image.printxt=printxt
