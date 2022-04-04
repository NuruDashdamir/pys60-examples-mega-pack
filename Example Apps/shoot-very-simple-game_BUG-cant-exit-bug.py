import appuifw,e32
from graphics import *

img=Image.new((320,240))
map=Image.new((320,240))

appuifw.app.screen='full'
appuifw.app.body=k=appuifw.Canvas()
global x,y,x1,y1,fire
x,y=5,50 
x1,y1=13,53 
fire=0 
map.clear((200,200,200))
map.rectangle((100,30,170,150),0x0000ff,0x0000ff)
def draw():
  global x,y,x1,y1,fire
  img.blit(map) 
  img.rectangle((x,y,x+10,y+10),0x000000,0x000000) 
  img.point((x1,y1),0x000000,0x000000,width=5) 
  k.blit(img) 
def pula_letit():
  global x,y,x1,y1,fire
  if fire==1: 
    x1+=1   
    if map.getpixel((x1,y1))[0]==(0,0,255): 
      map.point((x1,y1),(200,200,200),(200,200,200),width=20) 
      fire=0 
      x1,y1=x+3,y+3 
    if x1>176: 
      fire=0 
      x1,y1=x+3,y+3
def down():
  global x,y,x1,y1,fire
  y+=3
  if fire==0:y1+=3 
def up():
  global x,y,x1,y1,fire
  y-=3
  if fire==0:y1-=3
def f(): 
  global x,y,x1,y1,fire
  fire=1 
  while fire==1:
    draw()
    pula_letit()
    k.bind(50,up)
    k.bind(56,down)
    e32.ao_sleep(0.01)
    
while 1: 
 draw()
 k.bind(50,up)
 k.bind(53,f)
 k.bind(56,down)
 pula_letit()
 e32.ao_sleep(0.01)
