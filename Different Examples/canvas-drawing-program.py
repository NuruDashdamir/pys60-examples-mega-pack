# Draw
# (c) Moises Mariscal 2006
# Shareware software

import appuifw, e32, math, graphics
from key_codes import *
from graphics import Image
import time
import sysinfo
app=appuifw.app
app.screen='full'
c = appuifw.Canvas()
appuifw.app.body=c
draw = graphics.Draw(c)
sip = sysinfo.display_pixels()
global set1, set2
set1 = sip[0]
set2 = sip[1]
x, y = 88, 104
vx, vy =1, 1
fx, fy = 88, 104
huyfdgrf = 1
huyidgrf = 1
huyidgif = 0x0000FF
huyjdgif = 1
hvyjdgif = None
hvyjbgif = 1
global huydgrf
huydgrf = Image.new((set1,set2))
def hvgjbgif():
    c.rectangle([0,0, 16,193], 0x000000)
    c.line([0,64, 16,64], 0x000000)
    c.line([0,128, 16,128], 0x000000)
    c.line([0,193, 14,193], 0x000000)
    c.rectangle([4,3, 9,6], 0x00FF00, fill=0x00FF00)
    c.rectangle([9,3, 13,7], 0xFF0000, fill=0xFF0000)
    c.rectangle([9,6, 13,12], 0xFF8000, fill=0xFF8000)
    c.rectangle([4,6, 10,12], fill=huyidgif)
    c.line([8,18, 8,27], 0xFFFFFF, width=4)
    c.line([8,18, 8,27], huyidgif, width=huyjdgif)
    c.rectangle([4,35, 13,44], huyidgif, fill=hvyjdgif)
    c.line([4,35, 13,44], huyidgif)
    c.line([4,43, 12,35], huyidgif)
    c.line([4,50, 12,58], 0xFFFFFF, width=4)
    c.line([4,50, 12,58], huyidgif, width=huyjdgif)
    c.line([12,67, 10,73], 0xFFFFFF, width=4)
    c.line([10,73, 4,76], 0xFFFFFF, width=4)
    c.line([12,82, 6,85], 0xFFFFFF, width=4)
    c.line([6,85, 4,90], 0xFFFFFF, width=4)
    c.line([12,67, 10,73], huyidgif, width=huyjdgif)
    c.line([10,73, 4,76], huyidgif, width=huyjdgif)
    c.line([12,82, 6,85], huyidgif, width=huyjdgif)
    c.line([6,85, 4,90], huyidgif, width=huyjdgif)
    c.rectangle([4,97, 13,106], 0xFFFFFF, fill=0xFFFFFF, width=4)
    c.rectangle([4,97, 13,106], huyidgif, fill=hvyjdgif, width=huyjdgif)
    c.ellipse([4,113, 13,122], 0xFFFFFF, fill=0xFFFFFF, width=4)
    c.ellipse([4,113, 13,122], huyidgif, fill=hvyjdgif, width=huyjdgif)
    c.line([4,132, 13,132], 0x000000, width=1)
    c.line([9,137, 13,137], 0x000000, width=1)
    c.line([4,141, 10,141], 0x000000, width=1)
    c.line([4,132, 4,141], 0x000000, width=1)
    c.line([9,137, 9,141], 0x000000, width=1)
    c.line([13,132, 13,137], 0x000000, width=1)
    c.line([10,141, 13,138], 0x000000, width=1)
    c.rectangle([4,147, 13,156], 0x000000)
    c.rectangle([4,149, 7,154], 0x000000)
    c.rectangle([9,149, 13,154], 0x000000)
    c.line([11,151, 11,152], 0x000000)
    c.line([8,163, 8,170], 0x000000, width=2)
    c.line([5,166, 12,166], 0x000000, width=2)
    c.line([8,180, 8,187], 0x000000, width=2)
hvgjbgif()
def hvgjbegif():
    global hvyjbgif
    hvyjbgif = 0
def m_stick():       
    global fx, fy
    fx = x
    fy = y
    hvgjbgif()
def hvgjbiegif(ii):
    global vx, vy
    if ii > 1:
        c.line([8,163, 8,170], 0x0000FF, width=2)
        c.line([5,166, 12,166], 0x0000FF, width=2)
    if ii < 1:
        c.line([8,180, 8,187], 0x0000FF, width=2)
    vx = vx*ii
    vy = vy*ii
    hvgjbgif()
def m_dir(dx, dy):
    global x, y
    x = x+dx*vx
    y = y+dy*vy
    c.blit(huydgrf)
    c.point((x, y), huyidgif, width=5)
    hvgjbgif()
def m_col():
    global huyfdgrf, huyidgif
    huyfdgrf = huyfdgrf + 1
    if huyfdgrf > 9:
        huyfdgrf = 1
    if huyfdgrf == 1:
        huyidgif = 0x0000FF
        hvgjbgif()
    if huyfdgrf == 2:
        huyidgif = 0xFF0000
        hvgjbgif()
    if huyfdgrf == 3:
        huyidgif = 0x00FF00
        hvgjbgif()
    if huyfdgrf == 4:
        huyidgif = 0xFFFF00
        hvgjbgif()
    if huyfdgrf == 5:
        huyidgif = 0x808080
        hvgjbgif()
    if huyfdgrf == 6:
        huyidgif = 0x800000
        hvgjbgif()
    if huyfdgrf == 7:
        huyidgif = 0xFF00FF
        hvgjbgif()
    if huyfdgrf == 8:
        huyidgif = 0x00FFFF
        hvgjbgif()
    c.point((x, y), huyidgif, width=5)
    hvgjbgif()
def m_gros():
    global huyidgrf, huyjdgif
    huyidgrf = huyidgrf + 1
    if huyidgrf > 3:
        huyidgrf = 1
    if huyidgrf == 1:
        huyjdgif = 1
        hvgjbgif()
    if huyidgrf == 2:
        huyjdgif = 2
        hvgjbgif()
    if huyidgrf == 3:
        huyjdgif = 3
        hvgjbgif()
def hvgjbielgif():
    huydgrf.line([x,y, fx,fy], huyidgif, width=huyjdgif)
    c.blit(huydgrf)
    hvgjbgif()
def m_tool():
    global ix, iy, ex, ey, fx, fy
    if x > fx:
        if y < fy:
            ix, iy = fx, y
            ex, ey = x, fy 
        else:
            ix, iy = fx, fy
            ex, ey = x, y 
    else:
        if y > fy:
            ix, iy = x, fy
            ex, ey = fx, y 
        else:
            ix, iy = x, y
            ex, ey = fx, fy
def m_rell():
    global hvyjdgif
    if hvyjdgif == None:
        hvyjdgif = huyidgif
    else:    
        hvyjdgif = None
        c.rectangle([4,35, 13,44], huyidgif, fill=0xFFFFFF)
        c.line([4,35, 13,44], huyidgif)
        c.line([4,44, 13,35], huyidgif)
    hvgjbgif()
def m_rec():
    m_tool()
    huydgrf.rectangle([ix,iy, ex,ey], outline=huyidgif, fill=hvyjdgif, width=huyjdgif)
    c.blit(huydgrf)
    hvgjbgif()
def hvielgif():
    m_tool()
    huydgrf.ellipse([ix,iy, ex,ey], outline=huyidgif, fill=hvyjdgif, width=huyjdgif)
    c.blit(huydgrf)
    hvgjbgif()
def hvielhurdgif():
    global ix, iy, ex, ey, ai, af, fx, fy
    if x > fx:
        if y > fy:
            ix, iy = fx, fy-(y-fy)
            ex, ey = x+(x-fx), y
            ai, af = math.pi, -(math.pi/2)
        else:
            ix, iy = fx, y
            ex, ey = x+(x-fx), fy+(fy-y)
            ai, af = math.pi/2, math.pi
    if x < fx:
        if y > fy:
            ix, iy = x, fy
            ex, ey = fx+(fx-x), y+(y-fy)
            ai, af = math.pi/2, math.pi
        else:
            ix, iy = x, y-(fy-y)
            ex, ey = fx+(fx-x), fy
            ai, af = math.pi, -(math.pi/2)
    huydgrf.arc(([ix,iy],[ex,ey]),ai,af, huyidgif, fill=hvyjdgif, width=huyjdgif)
    c.blit(huydgrf)
    hvgjbgif()
def hvielhudgif():
    global ix, iy, ex, ey, ai, af, fx, fy
    if x > fx:
        if y < fy:
            ix, iy = fx-(x-fx), y-(fy-y)
            ex, ey = x, fy
            ai, af = -(math.pi/2), 0
        else:
            ix, iy = fx-(x-fx), fy
            ex, ey = x, y-(fy-y)
            ai, af = 0, math.pi/2 
    if x < fx:
        if y > fy:
            ix, iy = x-(fx-x), fy-(y-fy)
            ex, ey = fx, y
            ai, af = -(math.pi/2), 0
        else:
            ix, iy = x-(fx-x), y
            ex, ey = fx, fy+(fy-y)
            ai, af = 0, math.pi/2
    huydgrf.arc(([ix,iy],[ex,ey]),ai,af, huyidgif, fill=hvyjdgif, width=huyjdgif)
    c.blit(huydgrf)
    hvgjbgif()
c.line([87,189, 107,94], 0xADD8E6, width=1)
c.line([87,189, 118,63], 0xADD8E6, width=1)
c.line([87,189, 127,86], 0xADD8E6, width=1)
c.line([87,189, 134,110], 0xADD8E6, width=1)
c.line([87,189, 139,135], 0xADD8E6, width=1)
c.line([107,94, 111,94], 0xADD8E6, width=1)
c.line([118,63, 127,86], 0xADD8E6, width=1)
c.line([121,101, 134,110], 0xADD8E6, width=1)
c.line([134,110, 139,135], 0xADD8E6, width=1)
c.arc(([145,17],[171,68]), math.pi/2, math.pi, 0x0000FF, width=2)
c.arc(([138,44],[158,61]), 0, math.pi/2, 0xADD8E6, width=2)
c.arc(([138,44],[158,61]), -(math.pi/2), 0, 0xADD8E6, width=2)
c.arc(([130,47],[165,132]), math.pi/2, math.pi, 0xADD8E6, width=2)
c.arc(([64,3],[93,72]), -(math.pi/2), 0, 0x0000FF, width=2)
c.arc(([50,10],[106,73]), math.pi, -(math.pi/2), 0x0000FF, width=2)
c.arc(([40,82],[78,99]), 0, math.pi/2, 0x0000FF, width=2)
c.arc(([63,92],[79,108]), -(math.pi/2), 0, 0x0000FF, width=2)
c.line([96,43, 56,59], 0x0000FF, width=3)
c.line([56,83, 74,77], 0x0000FF, width=3)
c.line([61,106, 73,106], 0x0000FF, width=3)
c.ellipse([59,95, 72,105], outline=0x0000FF, width=3)
c.line([74,114, 62,122], 0x0000FF, width=3)
c.line([62,122, 74,126], 0x0000FF, width=3)
c.line([74,126, 62,133], 0x0000FF, width=3)
c.line([62,133, 78,144], 0x0000FF, width=3)
c.arc(([3,37],[47,230]), 0, math.pi/2, 0xFF8C00, width=2)
from graphics import *
def pantalla():
    c.rectangle([4,147, 13,156], 0x0000FF)
    c.rectangle([4,149, 7,154], 0x0000FF)
    c.rectangle([9,149, 13,154], 0x0000FF)
    c.line([11,151, 11,152], 0x0000FF)
    im = graphics.screenshot()
    name = unicode(time.strftime("%d%m%y%H%M%S",time.localtime()))
    im.save(u"C:\\Nokia\\Images\\ %s .jpg" %name)
    hvgjbgif()
def limp():
    c.line([4,132, 13,132], 0x0000FF, width=1)
    c.line([9,137, 13,137], 0x0000FF, width=1)
    c.line([4,141, 10,141], 0x0000FF, width=1)
    c.line([4,132, 4,141], 0x0000FF, width=1)
    c.line([9,137, 9,141], 0x0000FF, width=1)
    c.line([13,132, 13,137], 0x0000FF, width=1)
    c.line([10,141, 13,138], 0x0000FF, width=1)
    huydgrf.rectangle([1,1, set1,set2], 0xFFFFFF, fill=0xFFFFFF)
    hvgjbgif()
app.exit_key_handler= hvgjbegif
c.bind(EKey7,lambda:hvgjbiegif(2)) 			
c.bind(EKeyStar,lambda:hvgjbiegif(0.5)) 
c.bind(EKeyRightArrow,lambda:m_dir(1, 0))
c.bind(EKeyLeftArrow,lambda:m_dir(-1, 0))
c.bind(EKeyUpArrow,lambda:m_dir(0, -1))
c.bind(EKeyDownArrow,lambda:m_dir(0, 1))
c.bind(EKeyHash,lambda:hvgjbielgif())
c.bind(EKey4,lambda:pantalla())
c.bind(EKeySelect,lambda:m_stick())
c.bind(EKey1, lambda:limp())
c.bind(EKey8,lambda:m_rec())
c.bind(EKey0,lambda:hvielgif())
c.bind(EKey3,lambda:m_col())
c.bind(EKey6,lambda:m_gros())
c.bind(EKey5,lambda:hvielhurdgif())
c.bind(EKey2,lambda:hvielhudgif())
c.bind(EKey9,lambda:m_rell())
while hvyjbgif:
    e32.ao_sleep(0.5)



