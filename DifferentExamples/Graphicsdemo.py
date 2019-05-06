#script by Albert927
#Ôóíêöèè èç äâèæêà engine ìîæèòå èñïîëüçîâàòü è ó ñåáÿ, êîíå÷íî íåçàáûâàÿ ññûëàòüñÿ íà ðàçðàáîò÷èêà:)

import appuifw
from appuifw import *
import e32
from graphics import *

line_position_x=[]
line_position_y=[]
line_position_t_set=-1
line_position_t_get=-1
#################begin engine
def line_clear():#î÷èùàåì áóôåðû
    global line_position_x
    global line_position_y 
    global line_position_t_set
    global line_position_t_get
    line_position_x=[]
    line_position_y=[]
    line_position_t_set=-1
    line_position_t_get=-1

def set_line_position(x,y):#êèäàåò íîâóþ âû÷åñëåííóþ òî÷êó â áóôåð
    global line_position_x
    global line_position_y 
    global line_position_t_set

    line_position_t_set+=1
    line_position_x.append(x)
    line_position_y.append(y)

def get_line_position():#èçâëåêàåò íîâóþ òî÷êó èç áóôåðà, è âîçâðàùàåò åãî êîîðäèíàòû
    global line_position_x
    global line_position_y 
    global line_position_t_set
    global line_position_t_get

    line_position_t_get+=1
    if line_position_t_get>line_position_t_set:
        line_position_t_get=0
    return line_position_x[line_position_t_get],line_position_y[line_position_t_get]

def line_add(x1,y1,x2,y2):#âû÷èñëÿåì êîîðäèíàòû âñåõ òî÷åê, íàõîäÿùèåñÿ ìåæäó òî÷êàìè ñ êîîðäèíàòàìè x1,y1 è x2,y2, è êèäàåì èõ â áóôåð.
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
line_add(0,0,20,75)
line_add(23,77,57,100)
line_add(59,103,145,145)
line_add(148,148,176,208)


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
    img.point((razmer-155,x-155),0xff9999,width=2)
    img.point((razmer+155,x-140),0x9999ff,width=5)
    img.point((razmer+160,x-150),0x99ff99,width=3)
    img.point((razmer+145,x-136),0xffff99,width=4)
    img.point((razmer-139,x-139),0xff9999,width=2)
    img.point((razmer-150,x-168),0x9999ff,width=5)
    img.point((razmer-120,x-140),0x99ff99,width=3)
    img.point((razmer-149,x-179),0xffff99,width=4)
    img.point((razmer-100,x+25),0xff9999,width=2)
    img.point((razmer+150,x+145),0x9999ff,width=5)
    img.point((razmer+150,x+130),0x99ff99,width=3)
    img.point((razmer+140,x+196),0xffff99,width=4)
    img.point((razmer,x+39),0xff9999,width=2)
    img.point((razmer-150,x+168),0x9999ff,width=5)
    img.point((razmer-150,x-110),0x99ff99,width=3)
    img.point((razmer-140,x-160),0xffff99,width=4)
   
    img.point((razmer,x-155),0xff9999,width=2)
    img.point((razmer+50,x-140),0x9999ff,width=5)
    img.point((razmer+100,x-150),0x99ff99,width=3)
    img.point((razmer+40,x-136),0xffff99,width=4)
    img.point((razmer,x-139),0xff9999,width=2)
    img.point((razmer-50,x-168),0x9999ff,width=5)
    img.point((razmer-100,x-140),0x99ff99,width=3)
    img.point((razmer-40,x-179),0xffff99,width=4)
    img.point((razmer,x+25),0xff9999,width=2)
    img.point((razmer+50,x+140),0x9999ff,width=5)
    img.point((razmer+100,x+110),0x99ff99,width=3)
    img.point((razmer+40,x+126),0xffff99,width=4)
    img.point((razmer,x+39),0xff9999,width=2)
    img.point((razmer-50,x+148),0x9999ff,width=5)
    img.point((razmer+20,x-110),0x99ff99,width=3)
    img.point((razmer+60,x-160),0xffff99,width=4)
    img.point((razmer,x+135),0xff9999,width=1)
    img.point((razmer,x+140),0x9999ff,width=2)
    img.point((razmer,x-110),0x99ff99,width=1)
    img.point((razmer,x-160),0xffff99,width=2)
    img.point((razmer,x+120),0xff9999,width=2)
    img.point((razmer,x+120),0x9999ff,width=2)
    img.point((razmer,x-45),0x99ff99,width=1)
    img.point((razmer,x-75),0xffff99,width=2)
    img.point((razmer+15,x),0xff9999,width=2)
    img.point((razmer,x+40),0x9999ff,width=5)
    img.point((razmer,x+10),0x99ff99,width=3)
    img.point((razmer,x+60),0xffff99,width=4)
    img.point((razmer,x),0xff9999,width=2)
    img.point((razmer,x+40),0x9999ff,width=5)
    img.point((x-100,razmer),0x99ff99,width=3)
    img.point((x-40,razmer),0xffff99,width=4)
    img.point((x,razmer),0xff9999,width=1)
    img.point((x+70,razmer),0x9999ff,width=2)
    img.point((x+88,razmer),0x99ff99,width=1)
    img.point((x+58,razmer),0xffff99,width=2)
    img.point((x,razmer),0xff9999,width=2)
    img.point((x-30,razmer),0x9999ff,width=2)
    img.point((x-25,razmer),0x99ff99,width=1)
    img.point((x-46,razmer),0xffff99,width=2)
    img.point((y-125,y-155),0xff9999,width=2)
    img.point((y+155,y-140),0x9999ff,width=5)
    img.point((y+165,y-150),0x99ff99,width=3)
    img.point((y+145,y-136),0xffff99,width=4)
    img.point((y-133,y-139),0xff9999,width=2)
    img.point((y-150,y-168),0x9999ff,width=5)
    img.point((y-120,y-140),0x99ff99,width=3)
    img.point((y-119,y-179),0xffff99,width=4)
    img.point((y-103,y+25),0xff9999,width=2)
    img.point((y+153,y+145),0x9999ff,width=5)
    img.point((y+110,y+130),0x99ff99,width=3)
    img.point((y+148,y+196),0xffff99,width=4)
    img.point((y,y+32),0xff9999,width=2)
    img.point((y-150,y+168),0x9999ff,width=5)
    img.point((y-150,y-110),0x99ff99,width=3)
    img.point((y-140,y-160),0xffff99,width=4)
   
    img.point((y,y-155),0xff9999,width=2)
    img.point((y+50,y-140),0x9999ff,width=5)
    img.point((y+100,y-150),0x99ff99,width=3)
    img.point((y+40,y-136),0xffff99,width=4)
    img.point((y,y-139),0xff9999,width=2)
    img.point((y-50,y-168),0x9999ff,width=5)
    img.point((y-100,y-140),0x99ff99,width=3)
    img.point((y-40,y-179),0xffff99,width=4)
    img.point((y,y+25),0xff9999,width=2)
    img.point((y+50,y+140),0x9999ff,width=5)
    img.point((y+100,y+110),0x99ff99,width=3)
    img.point((y+40,y+126),0xffff99,width=4)
    img.point((y,y+39),0xff9999,width=2)
    img.point((y-50,y+148),0x9999ff,width=5)
    img.point((y-100,y-110),0x99ff99,width=3)
    img.point((y-40,y-160),0xffff99,width=4)
    img.point((y,y+135),0xff9999,width=1)
    img.point((y+70,y+140),0x9999ff,width=2)
    img.point((y+88,y-110),0x99ff99,width=1)
    img.point((y+58,y-160),0xffff99,width=2)
    img.point((y,y+120),0xff9999,width=2)
    img.point((y-30,y+120),0x9999ff,width=2)
    img.point((y-25,y-45),0x99ff99,width=1)
    img.point((y-46,y-75),0xffff99,width=2)
    img.point((y+41,y),0xff9999,width=2)
    img.point((y+50,y+45),0x9999ff,width=5)
    img.point((y+100,y+20),0x99ff99,width=3)
    img.point((y+40,y+30),0xffff99,width=4)
    img.point((y,y+8),0xff9999,width=2)
    img.point((y-50,y+49),0x9999ff,width=5)
    img.point((y-100,y-17),0x99ff99,width=3)
    img.point((y-40,y-66),0xffff99,width=4)
    img.point((y,y+58),0xff9999,width=1)
    img.point((y+70,y+48),0x9999ff,width=2)
    img.point((y+88,y-15),0x99ff99,width=1)
    img.point((y+58,y-65),0xffff99,width=2)
    img.point((y+5,y),0xff9999,width=2)
    img.point((y-30,y+25),0x9999ff,width=2)
    img.point((y-25,y-48),0x99ff99,width=1)
    img.point((y-46,y-65),0xffff99,width=2)
    img.point((x-155,x-155),0xff9999,width=2)
    img.point((x+155,x-140),0x9999ff,width=5)
    img.point((x+160,x-150),0x99ff99,width=3)
    img.point((x+145,x-136),0xffff99,width=4)
    img.point((x-139,x-139),0xff9999,width=2)
    img.point((x-150,x-168),0x9999ff,width=5)
    img.point((x-120,x-140),0x99ff99,width=3)
    img.point((x-149,x-179),0xffff99,width=4)
    img.point((x-100,x+25),0xff9999,width=2)
    img.point((x+150,x+145),0x9999ff,width=5)
    img.point((x+150,x+130),0x99ff99,width=3)
    img.point((x+140,x+196),0xffff99,width=4)
    img.point((x,x+39),0xff9999,width=2)
    img.point((x-150,x+168),0x9999ff,width=5)
    img.point((x-150,x-110),0x99ff99,width=3)
    img.point((x-140,x-160),0xffff99,width=4)
   
    img.point((x,x-155),0xff9999,width=2)
    img.point((x+50,x-140),0x9999ff,width=5)
    img.point((x+100,x-150),0x99ff99,width=3)
    img.point((x+40,x-136),0xffff99,width=4)
    img.point((x,x-139),0xff9999,width=2)
    img.point((x-50,x-168),0x9999ff,width=5)
    img.point((x-100,x-140),0x99ff99,width=3)
    img.point((x-40,x-179),0xffff99,width=4)
    img.point((x,x+25),0xff9999,width=2)
    img.point((x+50,x+140),0x9999ff,width=5)
    img.point((x+100,x+110),0x99ff99,width=3)
    img.point((x+40,x+126),0xffff99,width=4)
    img.point((x,x+39),0xff9999,width=2)
    img.point((x-50,x+148),0x9999ff,width=5)
    img.point((x-100,x-110),0x99ff99,width=3)
    img.point((x-40,x-160),0xffff99,width=4)
    img.point((x,x+135),0xff9999,width=1)
    img.point((x+70,x+140),0x9999ff,width=2)
    img.point((x+88,x-110),0x99ff99,width=1)
    img.point((x+58,x-160),0xffff99,width=2)
    img.point((x,x+120),0xff9999,width=2)
    img.point((x-30,x+120),0x9999ff,width=2)
    img.point((x-25,x-45),0x99ff99,width=1)
    img.point((x-46,x-75),0xffff99,width=2)
    img.point((x,x),0xff9999,width=2)
    img.point((x+50,x+40),0x9999ff,width=5)
    img.point((x+100,x+10),0x99ff99,width=3)
    img.point((x+40,x+60),0xffff99,width=4)
    img.point((x,x),0xff9999,width=2)
    img.point((x-50,x+40),0x9999ff,width=5)
    img.point((x-100,x-10),0x99ff99,width=3)
    img.point((x-40,x-60),0xffff99,width=4)
    img.point((x,x+50),0xff9999,width=1)
    img.point((x+70,x+40),0x9999ff,width=2)
    img.point((x+88,x-10),0x99ff99,width=1)
    img.point((x+58,x-60),0xffff99,width=2)
    img.point((x,x),0xff9999,width=2)
    img.point((x-30,x+20),0x9999ff,width=2)
    img.point((x-25,x-38),0x99ff99,width=1)
    img.point((x-46,x-60),0xffff99,width=2)
    img.point((y-155,x-155),0xff9999,width=2)
    img.point((y+155,x-140),0x9999ff,width=5)
    img.point((y+160,x-150),0x99ff99,width=3)
    img.point((y+145,x-136),0xffff99,width=4)
    img.point((y-139,x-139),0xff9999,width=2)
    img.point((y-150,x-168),0x9999ff,width=5)
    img.point((y-120,x-140),0x99ff99,width=3)
    img.point((y-149,x-179),0xffff99,width=4)
    img.point((y-100,x+25),0xff9999,width=2)
    img.point((y+150,x+145),0x9999ff,width=5)
    img.point((y+150,x+130),0x99ff99,width=3)
    img.point((y+140,x+196),0xffff99,width=4)
    img.point((y,x+39),0xff9999,width=2)
    img.point((y-150,x+168),0x9999ff,width=5)
    img.point((y-150,x-110),0x99ff99,width=3)
    img.point((y-140,x-160),0xffff99,width=4)
   
    img.point((y,x-155),0xff9999,width=2)
    img.point((y+50,x-140),0x9999ff,width=5)
    img.point((y+100,x-150),0x99ff99,width=3)
    img.point((y+40,x-136),0xffff99,width=4)
    img.point((y,x-139),0xff9999,width=2)
    img.point((y-50,x-168),0x9999ff,width=5)
    img.point((y-100,x-140),0x99ff99,width=3)
    img.point((y-40,x-179),0xffff99,width=4)
    img.point((y,x+25),0xff9999,width=2)
    img.point((y+50,x+140),0x9999ff,width=5)
    img.point((y+100,x+110),0x99ff99,width=3)
    img.point((y+40,x+126),0xffff99,width=4)
    img.point((y,x+39),0xff9999,width=2)
    img.point((y-50,x+148),0x9999ff,width=5)
    img.point((y-100,x-110),0x99ff99,width=3)
    img.point((y-40,x-160),0xffff99,width=4)
    img.point((y,x+135),0xff9999,width=1)
    img.point((y+70,x+140),0x9999ff,width=2)
    img.point((y+88,x-110),0x99ff99,width=1)
    img.point((y+58,x-160),0xffff99,width=2)
    img.point((y,x+120),0xff9999,width=2)
    img.point((y-30,x+120),0x9999ff,width=2)
    img.point((y-25,x-45),0x99ff99,width=1)
    img.point((y-46,x-75),0xffff99,width=2)
    img.point((y,x),0xff9999,width=2)
    img.point((y+50,x+40),0x9999ff,width=5)
    img.point((y+100,x+10),0x99ff99,width=3)
    img.point((y+40,x+60),0xffff99,width=4)
    img.point((y,x),0xff9999,width=2)
    img.point((y-50,x+40),0x9999ff,width=5)
    img.point((y-100,x-10),0x99ff99,width=3)
    img.point((y-40,x-60),0xffff99,width=4)
    img.point((y,x+50),0xff9999,width=1)
    img.point((y+70,x+40),0x9999ff,width=2)
    img.point((y+88,x-10),0x99ff99,width=1)
    img.point((y+58,x-60),0xffff99,width=2)
    img.point((y,x),0xff9999,width=2)
    img.point((y-30,x+20),0x9999ff,width=2)
    img.point((y-25,x-38),0x99ff99,width=1)
    img.point((y-46,x-60),0xffff99,width=2)
    handle_redraw(())
    e32.ao_yield()







        


 



