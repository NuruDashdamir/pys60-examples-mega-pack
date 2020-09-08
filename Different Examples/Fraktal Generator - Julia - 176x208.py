import appuifw
from appuifw import *
import e32
from graphics import *
import time

def quit():
    global r_var
    r_var=0
#    appuifw.app.set_exit()

appuifw.app.screen='full'
x=10
d=3
img=Image.new((176,208))


def handle_redraw(rect):
    canvas.blit(img)
   
r_var=1

canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)

appuifw.app.body=canvas

app.exit_key_handler=quit

tm1= time.clock()
a=0
b=0
img.clear(0x00)
while b<208 and r_var:
  a=0
  while a<176:
    y1=3*a/176.-1.5
    x1=3*b/208.-1.5
    xx=x1
    yy=y1
    i=-1
    m=0
    run=1
    while i<50 and run:
      x=xx
      xx=x**2.-yy**2+0.32
      yy=2.*x*yy+0.042
      m=xx*xx+yy*yy
      if m>20:
       run=0
      i=i+1
    if m>20:
     rd=i*5
     gr=i*6*256
     bl=i*4*65536
     c=rd+gr+bl
     img.point((a,b),c,width=1)
    a=a+1
  handle_redraw(())
  e32.ao_yield()
  b=b+1
tm2=time.clock()
print u'time=',tm2-tm1
while r_var:
   handle_redraw(())
   e32.ao_yield()
  





        


 



