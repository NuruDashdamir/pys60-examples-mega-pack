# Grishberg@rambler.ru

import appuifw
from appuifw import *
from graphics import *
import e32

import math
#init
sin=range(0,360)
cos=range(0,360)
i=0
while i<360:
  sin[i]=math.sin(math.pi*i/180)
  cos[i]=math.cos(math.pi*i/180)
  i+=1
  
h2=208/2
w2=176/2
zcam=-300
ab1=0
ab2=0
ab3=0

matrix=[[0,0,0],
        [0,0,0],
        [0,0,0]]

def multv(m,v):
  xy=v[0]*v[1]
  global ab1
  global ab2
  global ab3
  p=[0,0,0]
  p[0]=(m[0][0]+v[1])*(m[1][0]+v[0])+m[2][0]*v[2]-ab1-xy
  p[1]=(m[0][1]+v[1])*(m[1][1]+v[0])+m[2][1]*v[2]-ab1-xy
  p[2]=(m[0][2]+v[1])*(m[1][2]+v[0])+m[2][2]*v[2]-ab1-xy
  
  return p

def multm(m,v):
  p=[[0,0,0],
       [0,0,0],
       [0,0,0]]
  p[0][0]=m[0][0]*v[0][0]+m[1][0]*v[0][1]+m[2][0]*v[0][2]
  p[0][1]=m[0][1]*v[0][0]+m[1][1]*v[0][1]+m[2][1]*v[0][2]
  p[0][2]=m[0][2]*v[0][0]+m[1][2]*v[0][1]+m[2][2]*v[0][2]

  p[1][0]=m[0][0]*v[1][0]+m[1][0]*v[1][1]+m[2][0]*v[1][2]
  p[1][1]=m[0][1]*v[1][0]+m[1][1]*v[1][1]+m[2][1]*v[1][2]
  p[1][2]=m[0][2]*v[1][0]+m[1][2]*v[1][1]+m[2][2]*v[1][2]

  p[2][0]=m[0][0]*v[2][0]+m[1][0]*v[2][1]+m[2][0]*v[2][2]
  p[2][1]=m[0][1]*v[2][0]+m[1][1]*v[2][1]+m[2][1]*v[2][2]
  p[2][2]=m[0][2]*v[2][0]+m[1][2]*v[2][1]+m[2][2]*v[2][2]
  
  return p

def proj(v):
  global zcam
  a=-10
  t=10
  global h2
  global w2
  z=v[2]-zcam
  xx=v[0]/(z/a+1)*t+w2
  yy=-(v[1])/(z/a+1)*t+h2
  return int(xx),int(yy)

def roty(ang):
  m=[[0,0,0],
       [0,1,0],
       [0,0,0]]
  global ab1
  global ab2
  global ab3
  m[0][0]=cos[ang]
  m[2][0]=-sin[ang]
  m[0][2]=sin[ang]
  m[2][2]=cos[ang]
  ab1=m[0][0]*m[1][0]
  ab2=m[0][1]*m[1][1]
  ab3=m[0][2]*m[1][2]
  return m

def rotx(ang):
  m=[[1,0,0],
       [0,0,0],
       [0,0,0]]
  m[1][1]=cos[ang]
  m[2][1]=-sin[ang]
  m[1][2]=sin[ang]
  m[2][2]=cos[ang]
  return m

def rotz(ang):
  m=[[0,0,0],
       [0,0,0],
       [0,0,1]]
  m[0][0]=cos[ang]
  m[1][0]=-sin[ang]
  m[0][1]=sin[ang]
  m[1][1]=cos[ang]
  return m

def rect3d(v1,v2,v3,v4,n,c):
  global zcam
  d=-(n[0]*v1[0]+n[1]*v1[1]+n[2]*v1[2])
  if (n[2]*zcam+d)> 0:
    a1,b1=proj(v1)
    a2,b2=proj(v2)
    a3,b3=proj(v3)
    a4,b4=proj(v4)
    img.polygon((a1,b1,a2,b2,a3,b3,a4,b4),c)

def cub3d(v,a,matrix,c):
    p1=[a+v[0],a+v[1],a+v[2]]
    p2=[a+v[0],-a+v[1],a+v[2]]
    p3=[a+v[0],a+v[1],-a+v[2]]
    p4=[a+v[0],-a+v[1],-a+v[2]]
    p5=[-a+v[0],a+v[1],a+v[2]]
    p6=[-a+v[0],-a+v[1],a+v[2]]
    p7=[-a+v[0],a+v[1],-a+v[2]]
    p8=[-a+v[0],-a+v[1],-a+v[2]]

    nn1=[10,0,0]
    nn2=[0,0,10]
    nn3=[-10,0,0]
    nn4=[0,0,-10]
    nn5=[0,10,0]
    nn6=[0,-10,0]

    v1=multv(matrix,p1)
    v2=multv(matrix,p2)
    v3=multv(matrix,p3)
    v4=multv(matrix,p4)
    v5=multv(matrix,p5)
    v6=multv(matrix,p6)
    v7=multv(matrix,p7)
    v8=multv(matrix,p8)

    n1=multv(matrix,nn1)
    n2=multv(matrix,nn2)
    n3=multv(matrix,nn3)
    n4=multv(matrix,nn4)
    n5=multv(matrix,nn5)
    n6=multv(matrix,nn6)

    rect3d(v1,v2,v4,v3,n1,c)
    rect3d(v1,v2,v6,v5,n2,c)
    rect3d(v5,v6,v8,v7,n3,c)
    rect3d(v7,v8,v4,v3,n4,c)
    rect3d(v7,v3,v1,v5,n5,c)
    rect3d(v6,v8,v4,v2,n6,c)
  
def tcub3d(v,a,matrix,c):
    p1=[a+v[0],a+v[1],a+v[2]]
    p2=[a+v[0],-a+v[1],a+v[2]]
    p3=[a+v[0],a+v[1],-a+v[2]]
    p4=[a+v[0],-a+v[1],-a+v[2]]
    p5=[-a+v[0],a+v[1],a+v[2]]
    p6=[-a+v[0],-a+v[1],a+v[2]]
    p7=[-a+v[0],a+v[1],-a+v[2]]
    p8=[-a+v[0],-a+v[1],-a+v[2]]

    nn1=[10,0,0]
    nn2=[0,0,10]
    nn3=[-10,0,0]
    nn4=[0,0,-10]
    nn5=[0,10,0]
    nn6=[0,-10,0]

    v1=multv(matrix,p1)
    v2=multv(matrix,p2)
    v3=multv(matrix,p3)
    v4=multv(matrix,p4)
    v5=multv(matrix,p5)
    v6=multv(matrix,p6)
    v7=multv(matrix,p7)
    v8=multv(matrix,p8)

    n1=multv(matrix,nn1)
    n2=multv(matrix,nn2)
    n3=multv(matrix,nn3)
    n4=multv(matrix,nn4)
    n5=multv(matrix,nn5)
    n6=multv(matrix,nn6)

    tring3d(v1,v2,v3,n1,c)
    tring3d(v1,v2,v6,n2,c)
    tring3d(v5,v6,v8,n3,c)
    tring3d(v7,v8,v4,n4,c)
    tring3d(v7,v3,v1,n5,c)
    tring3d(v6,v8,v4,n6,c)

    tring3d(v2,v3,v4,n1,c)
    tring3d(v1,v6,v5,n2,c)
    tring3d(v5,v8,v7,n3,c)
    tring3d(v7,v4,v3,n4,c)
    tring3d(v7,v1,v5,n5,c)
    tring3d(v6,v4,v2,n6,c)
  

def tring3d(v1,v2,v3,n,c):
  global zcam
  d=-(n[0]*v1[0]+n[1]*v1[1]+n[2]*v1[2])
  if n[2]*zcam+d> 0:
    a1,b1=proj(v1)
    a2,b2=proj(v2)
    a3,b3=proj(v3)
    c1=int((-n[1]+10)*12.7)
    img.polygon((a1,b1,a2,b2,a3,b3),c1,c1)

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
b=0
while r_var:
    if a>=360:
     a=0
    img.clear(0xffffff)

    matrix=multm(rotx(a),roty(a))
    v1=[0,50,-50]
    v2=[50,50,-50]
    v3=[50,0,-50]
    n=[0,0,-1]
    a+=1
    tcub3d([0,0,0],70,matrix,0)

    handle_redraw(())
    e32.ao_yield()