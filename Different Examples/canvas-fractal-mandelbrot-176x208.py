import appuifw
from appuifw import *
import e32
from graphics import *

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
a=0
b=0
img.clear(0x00)
while a<176 and r_var:
  b=0
  while b<208:
    y1=3*a/176.-1.5
    x1=3*b/208.-2.3
    xx=0
    yy=0
    i=-1
    m=0
    run=1
    while i<50 and run:
      x=xx
      xx=x**2.-yy**2+x1
      yy=2.*x*yy+y1
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
    b=b+1
  handle_redraw(())
  e32.ao_yield()
  a=a+1

while r_var:
   handle_redraw(())
   e32.ao_yield()
  





        


 



