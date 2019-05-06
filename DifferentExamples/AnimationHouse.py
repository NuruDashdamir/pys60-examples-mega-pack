#script by Albert927

import appuifw
from appuifw import *
import e32
from graphics import *

line_position_x=[]
line_position_y=[]
line_position_t_set=-1
line_position_t_get=-1
#################begin engine
def line_clear():
    global line_position_x
    global line_position_y 
    global line_position_t_set
    global line_position_t_get
    line_position_x=[]
    line_position_y=[]
    line_position_t_set=-1
    line_position_t_get=-1

def set_line_position(x,y):
    global line_position_x
    global line_position_y 
    global line_position_t_set

    line_position_t_set+=1
    line_position_x.append(x)
    line_position_y.append(y)

def get_line_position():
    global line_position_x
    global line_position_y 
    global line_position_t_set
    global line_position_t_get

    line_position_t_get+=1
    if line_position_t_get>line_position_t_set:
        line_position_t_get=0
    return line_position_x[line_position_t_get],line_position_y[line_position_t_get]

def line_add(x1,y1,x2,y2):
    d=0
    t=0
    t1=0
    t2=0
    td=0
    dx=0
    dy=0
    eps=0

    if x1==x2:
        for dy in range(y1,y2+1):
            set_line_position(x1,dy)
        return
    if y1==y2:
        for dx in range(x1,x2+1):
            set_line_position(dx,y1)
        return

    dx=abs(x1-x2)
    dy=abs(y1-y2)

    if dx>=dy:
        if x1<x2:
            t1=x1
            t2=x2
            td=y1
            if y1<y2:
                eps=1
            else: 
                eps=-1
        else:
            t1=x2
            t2=x1
            td=y2
            if y1<y2:
                eps=-1 
            else:
                eps=1

        d=-dx
        for t in range(t1,t2+1):
            set_line_position(t,td)
            d=d+dy
            if d>=0:
                d=d-dx
                td=td+eps
    else:
        if y1<y2:
            t1=y1
            t2=y2
            td=x1
            if x1<x2: 
                eps=1 
            else:
                eps=-1
        else:
            t1=y2
            t2=y1
            td=x2 
            if x1<x2:
                eps=-1 
            else:
                eps=1
        d=-dy
        for t in range(t1,t2+1):
            set_line_position(td,t)
            d=d+dx
            if d>=0:
                d=d-dy
                td=td+eps
#################begin engine
appuifw.app.screen='full'

img=None
def handle_redraw(rect):
    if img:
        canvas.blit(img)
appuifw.app.body=canvas=appuifw.Canvas(event_callback=None,redraw_callback=handle_redraw)
img=Image.new(canvas.size) 

running=1
def quit():
    global running
    running=0
appuifw.app.exit_key_handler=quit

line_clear()
line_add(0,0,175,207)
line_add(175,0,0,207)

razmer=90
razmer_flag=0
while running:
    if razmer_flag==0:
         razmer+=2
    if razmer_flag==1:
         razmer-=2 
    if razmer>90:
         razmer_flag=1
    if razmer<60:
         razmer_flag=0   
    img.clear(0) 
    [x,y]=get_line_position()
    img.line((x,y,15,175,),(razmer**3,x*5,y*5,),width=25)
    img.point((x,y,),(250,250,y*5,),width=25)
    img.line((y/3,x*3,170,185,),(razmer**3,x*6,y*5,),width=25)
    img.point((y/3,x*3,),(250,250,y*5,),width=25)
#    img.point((x+5+5+2,y+5+2+5,),0x999911,width=razmer+2+2+2+2)
    img.point((98,134,118,163),(x*5,y**2,razmer*3),width=razmer/2.5)
    img.rectangle((66,100,135,170),(250,150,3),width=razmer/1.5)
    img.line((50,95,105,15),0xfee999,width=razmer/3.4)
    img.line((150,95,105,15),0xfee999,width=razmer/3.4)
    img.rectangle((90,120,110,150),(x*5,y**2,razmer*3),width=razmer/4.5)
    img.point((98,128,118,158),(x*5,y**2,razmer*3),width=razmer/2.5)
    handle_redraw(())
    e32.ao_yield()
