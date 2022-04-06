import appuifw
from graphics import *
import e32
import random
import time
from key_codes import *

appuifw.app.screen='full'
backup_img=Image.new((176,208))
draw=Draw(backup_img)

def handle_redraw(param):
    canvas_draw.blit(backup_img)

class Keyboard(object):
    def __init__(self,onevent=lambda:None):
        self._keyboard_state={}
        self._downs={}
        self._onevent=onevent
    def handle_event(self,event):
        if event['type'] == appuifw.EEventKeyDown:
            cod=event['scancode']
            if not self.is_down(cod):
                self._downs[cod]=self._downs.get(cod,0)+1
            self._keyboard_state[cod]=1
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

running=1
def quit():
    global running
    running=0
appuifw.app.exit_key_handler=quit


class Playfield(object):
    def __init__(self,size,draw,bordercolor=0xc0c0c0):
        self._data={}
        self._size=size
        self._draw=draw
        for x in range(0,size[0]):
            for y in range(0,size[1]):
                self[(x,y)]=0
        # Initialize playing field borders
        for y in range(-1,size[1]+1):
            self[(-1,y)]=bordercolor
            self[(size[0],y)]=bordercolor
        for x in range(-1,size[0]+1):
            self[(x,-1)]=bordercolor
            self[(x,size[1])]=bordercolor
        self.draw()
    def __getitem__(self,loc):
        return self._data.setdefault(tuple(loc),0)
    def __setitem__(self,loc,value):
        self._data[loc]=value
        self.update_loc(loc)
    def remove_row(self,row):
        for x in range(0,self._size[0]):
            self[(x,0)]=0
        for y in range(row,0,-1):
            for x in range(0,self._size[0]):
                self[(x,y)]=self[(x,y-1)]
    def row_is_full(self,row):
        for x in range(0,self._size[0]):
            if not self[(x,row)]:
                return False
        return True
    def update_loc(self,loc):
        w=8
        x,y=((loc[0]+1)*w,(loc[1]+1)*w)
        self._draw.rectangle((x,y,x+w,y+w),None,self[loc])
    def draw(self):
        w=8
        for loc in self._data:
            self.update_loc(loc)
# with draw.rectangle((x,y,x+w,y+w),fill=self[loc]) 472 ms
# without 89 ms
# draw.rectangle((x,y,x+w,y+w),fill=0xff0000,outline=0x00ff00) 375 ms
# draw.rectangle((x,y,x+w,y+w)) without params setting, kw parsing 125 ms

class Piece(object):
    def __init__(self,squares,color):
        self._squares=squares
        self._color=color
    def fits_in(self,loc,angle,field):
        for s in self._squares[angle]:
            if field[(s[0]+loc[0],s[1]+loc[1])]:
                return False
        return True
    def put_to(self,loc,angle,field):
        for s in self._squares[angle]:
            field[(s[0]+loc[0],s[1]+loc[1])]=self._color
    def remove_from(self,loc,angle,field):
        for s in self._squares[angle]:
            field[(s[0]+loc[0],s[1]+loc[1])]=0
    
pieces=(
    Piece({0: ((1,0),(0,1),(1,1),(2,1)), # _|_ block
           1: ((1,0),(1,1),(2,1),(1,2)), 
           2: ((0,1),(1,1),(2,1),(1,2)),
           3: ((1,0),(0,1),(1,1),(1,2))}, 0x808080),
    Piece({0: ((1,0),(1,1),(1,2),(1,3)), # ---- block
           1: ((0,1),(1,1),(2,1),(3,1)),
           2: ((1,0),(1,1),(1,2),(1,3)),  
           3: ((0,1),(1,1),(2,1),(3,1))}, 0xff0000),
    Piece({0: ((0,0),(1,0),(0,1),(1,1)), # square block
           1: ((0,0),(1,0),(0,1),(1,1)),
           2: ((0,0),(1,0),(0,1),(1,1)),
           3: ((0,0),(1,0),(0,1),(1,1))}, 0x00ffff),
    Piece({0: ((0,0),(1,0),(1,1),(2,1)), # -_ block
           1: ((2,0),(1,1),(2,1),(1,2)),
           2: ((0,0),(1,0),(1,1),(2,1)),
           3: ((2,0),(1,1),(2,1),(1,2))}, 0x00ff00),
    Piece({0: ((1,0),(2,0),(0,1),(1,1)), # _- block
           1: ((0,0),(0,1),(1,1),(1,2)),
           2: ((1,0),(2,0),(0,1),(1,1)), 
           3: ((0,0),(0,1),(1,1),(1,2))}, 0xff8000),
    Piece({0: ((1,0),(1,1),(1,2),(2,2)), # L-block 
           1: ((1,1),(2,1),(3,1),(1,2)),
           2: ((1,1),(2,1),(2,2),(2,3)),
           3: ((2,1),(0,2),(1,2),(2,2))}, 0x0080ff),
    Piece({0: ((2,0),(2,1),(2,2),(1,2)), # J-block 
           1: ((1,1),(1,2),(2,2),(3,2)),
           2: ((1,1),(2,1),(1,2),(1,3)),
           3: ((0,1),(1,1),(2,1),(2,2))}, 0xffff00))


lock=e32.Ao_lock()
keyboard=Keyboard(onevent=lock.signal)
canvas=appuifw.Canvas(event_callback=keyboard.handle_event,
                      redraw_callback=handle_redraw)
canvas_draw=Draw(canvas)
appuifw.app.body=canvas
draw_time=0
draw_count=0
fieldsize=(10,20)
playing=1
def draw_score(draw):
    draw.rectangle((102,6,169,31),None,0x103010)
    draw.text((107,26),u'Lines: %d'%lines,0xc0ffc0,font=u'LatinBold19')
    draw.rectangle((102,31,169,56),None,0x103010)
    draw.text((107,51),u'Level: %d'%level,0xc0ffc0,font=u'LatinBold19')

try:
    logo=Image.open(u'e:\\system\\apps\\python\\pythonpowered.png')
except:
    logo=Image.new((100,16))
    drl=Draw(logo)
    drl.clear(0)

while playing:
    lines=0
    level=1
    x,y=3,0
    angle=0
    piece=pieces[random.randint(0,len(pieces)-1)]
    drop_interval=0.5
    draw.clear(0x000000)
    draw.blit(logo,target=(106,100))
    draw_score(draw)
    field=Playfield(fieldsize,draw)
    previous_drop=time.clock()
    e32.ao_sleep(drop_interval,lock.signal)
    running=1
    while running:
        piece.remove_from((x,y),angle,field)
        while keyboard.pressed(EScancodeLeftArrow) and piece.fits_in((x-1,y),angle,field):
            x-=1
            lock.signal()
        while keyboard.pressed(EScancodeRightArrow) and piece.fits_in((x+1,y),angle,field):
            x+=1
            lock.signal()
        while keyboard.pressed(EScancodeUpArrow) and piece.fits_in((x,y),(angle-1)%4,field):
            angle=(angle-1)%4    
        if keyboard.pressed(EScancodeDownArrow):
            while piece.fits_in((x,y+1),angle,field):
                y+=1
        if time.clock()-previous_drop >= drop_interval:
            if piece.fits_in((x,y+1),angle,field):
                y+=1
            else:
                piece.put_to((x,y),angle,field)
                removed_lines=0
                for y in range(fieldsize[1]):
                    if field.row_is_full(y):
                        field.remove_row(y)
                        removed_lines += 1
                if removed_lines:
                    lines += removed_lines
                    level=int(lines/10)+1
                    drop_interval=0.5*(0.85**(level-1))
                    draw_score(draw)
                x,y=3,0
                angle=0
                piece=pieces[random.randint(0,len(pieces)-1)]
                if not piece.fits_in((x,y),angle,field):
                    appuifw.note(u'Game over!','info')
                    running=0
            previous_drop=time.clock()
            e32.ao_sleep(drop_interval,lock.signal)            
        piece.put_to((x,y),angle,field)
        start_draw=time.clock()
        handle_redraw(())
        end_draw=time.clock()
        draw_time += end_draw-start_draw
        draw_count += 1
        e32.ao_yield()
        lock.wait()
    playing=appuifw.query(u'Play again?','query')
    
print "%d draws, %f s total, avg time %f ms"%(draw_count,
                                              draw_time,
                                              draw_time/draw_count*1000)
appuifw.app.screen='normal'