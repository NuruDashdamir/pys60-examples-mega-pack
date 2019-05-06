# Grishberg
# функции для преобразования rgb в hls
# я нашей этот алгоритм в нете, написанный на паскале, вот посидел и переделал под питон.
# пользуйтесь наздоровье!
# Grishberg@rambler.ru

import appuifw
from appuifw import *
from graphics import *
import e32
#from d3d import *

import math
h2=208/2
w2=176/2

def proj(x,y,z):
  a=60.5
  b=50
  global h2
  global w2
  z=z+b
  xx=x/(z/a+1)+w2
  yy=-(y)/(z/a+1)+h2
  return int(xx),int(yy)

def roty(x,y,z,x0,y0,z0,ang):
  xx=x*math.cos(ang)-z*math.sin(ang)+x0
  zz=x*math.sin(ang)+z*math.cos(ang)+z0
  return xx,y,zz

def rotx(x,y,z,x0,y0,z0,ang):
  yy=y*math.cos(ang)-z*math.sin(ang)+y0
  zz=y*math.sin(ang)+z*math.cos(ang)+z0
  return x,yy,zz

def rotz(x,y,z,x0,y0,z0,ang):
  xx=x*math.cos(ang)-y*math.sin(ang)+x0
  yy=x*math.sin(ang)+y*math.cos(ang)+y0
  return xx,yy,z

r_var=1
def quit():
    global r_var
    r_var=0

appuifw.app.screen='full'
img=Image.new((176,208))
def handle_redraw(rect):
    canvas.blit(img)

r_var=1
canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)
appuifw.app.body=canvas
app.exit_key_handler=quit
img.clear(0xffffff)
a=0
while r_var:
    a=a+0.1
    if a>6.28:
     a=0
    img.clear(0xffffff)
    x1,y1,z1=roty(50,50,50,0,0,0,a)
    x2,y2,z2=roty(50,-50,50,0,0,0,a)
    x3,y3,z3=roty(50,50,-50,0,0,0,a)
    x4,y4,z4=roty(50,-50,-50,0,0,0,a)
    x5,y5,z5=roty(-50,50,50,0,0,0,a)
    x6,y6,z6=roty(-50,-50,50,0,0,0,a)
    x7,y7,z7=roty(-50,50,-50,0,0,0,a)
    x8,y8,z8=roty(-50,-50,-50,0,0,0,a)
    a1,b1=proj(x1,y1,z1)
    a2,b2=proj(x2,y2,z2)
    a3,b3=proj(x3,y3,z3)
    a4,b4=proj(x4,y4,z4)
    a5,b5=proj(x5,y5,z5)
    a6,b6=proj(x6,y6,z6)
    a7,b7=proj(x7,y7,z7)
    a8,b8=proj(x8,y8,z8)
    img.line((a1,b1,a2,b2),250)
    img.line((a1,b1,a3,b3),250)
    img.line((a1,b1,a5,b5),250)
    img.line((a6,b6,a2,b2),250)
    img.line((a6,b6,a5,b5),250)
    img.line((a6,b6,a8,b8),250)
    img.line((a7,b7,a8,b8),250)
    img.line((a7,b7,a3,b3),250)
    img.line((a7,b7,a5,b5),250)
    img.line((a4,b4,a2,b2),250)
    img.line((a4,b4,a3,b3),250)
    img.line((a4,b4,a8,b8),250)
    img.text((10,10),u'Grishberg')
    handle_redraw(())
    e32.ao_yield()
 