#DEMOBILIZATION VER 0.5
#Gavrishev Alexandr (anod)
#mailto: alex.gavrishev@gmail.com
#SYMBIANUID=0x10201516

import appuifw
import e32
import time
from graphics import *

#SETTINGS:
#[DAY,MONTH,YEAR]#
#DEFAULT: dmb=[6,11,2007]
dmb=[6,11,2007]
#LEFT BUTTON NAME
#DEFAULT: btn_name=u'CHONG'
btn_name=u'CHONG'
#SCREENSHOT FILE NAME
#DEFAULT: scr_name=u'e:\\dmb_screen.jpg'
scr_name=u'e:\\dmb_screen.jpg'
#########################

dmb=[dmb[2],dmb[1],dmb[0],0,0,0,5,1,-1]

class Popupw:
    def __init__(self):
        self.ptext=[]
        self.posy=0
        self.htime=0
        self.tflag=0
        self.ct=0
        self.show=0
    def show_popup(self,pt,py=0,ht=0):
        self.ptext=pt
        self.posy=py
        self.htime=ht
        self.show=1
    def hide_popup(self):
        self.show=0
    def timeout(self):
        nt=0
        if (self.htime>0):
           if (self.tflag==0):
               self.ct=time.time()
               self.tflag=1
           else:
               nt=time.time()-self.ct
               if (nt==self.htime):
                   self.hide_popup()
                   self.tflag=0
    #draw
    def draw(self):
        global img
        self.timeout()
        if (self.show==1):
            img.rectangle([1,self.posy,173,self.posy+len(self.ptext)*12+10],0xffffff,0x000000)
            j=1
            for str in self.ptext:
                img.text((4,self.posy+j*12+3),unicode(self.ptext[j-1]),0xffffff)                
                j=j+1
#count of days in the year
def day_numb(year):
   res=time.localtime(time.mktime([year,12,31,0,0,0,5,1,-1]))
   return res[7]
#count of days from now to dmb
def calc_days(dmb):
    i=0
    cyear=time.localtime()
    ynow=int(cyear[0])
    if (ynow<>dmb[0]):
        i=day_numb(ynow)-cyear[7]
        n=(dmb[0]-ynow)
        if n>1:
            for k in range(1,n):
                i=i+day_numb(ynow+k)
        i=i+dmb[7]
    else:
        i=dmb[7]-cyear[7]
    return i

def calc_months(dmb):
    i=0
    cyear=time.localtime()
    ynow=int(cyear[0])
    i=(int(dmb[0])-ynow)*12+int(dmb[1])-int(cyear[1])
    return i

def redraw():
    global dmb
    global chong
    global btn_name
    mkrest=time.mktime(dmb)
    dmb=time.localtime(mkrest)
    ascrest=time.asctime(dmb)
    secrest=mkrest-time.time()
    daterest=time.localtime(secrest)
    monthrest=calc_months(dmb)
    dayrest=calc_days(dmb)
    img.clear(0)
    pt=[]
    pt.append(u'Now:')
    pt.append(unicode(time.ctime()))
    pt.append(u'Dmb day:')
    pt.append(unicode(ascrest))
    pt.append(u'Months: '+unicode(monthrest))
    pt.append(u'Weeks: '+unicode(dayrest/7))
    pt.append(u'Days: '+unicode(dayrest))
    pt.append(u'Hours: '+zadd(dayrest*24+daterest[3])+':'+zadd(daterest[4])+':'+zadd(daterest[5]))
    pt.append(u'Seconds: '+unicode(int(secrest)))
    mainw.show_popup(pt,0,0)
    if (mainw.show==1):
      mainw.draw()
    if not chong:
        #time
        nowt=unicode(int(secrest))
        xnowt=int((176-len(nowt)*13)/2)
        img.text((xnowt,160),nowt,0xffffff,u"Acalc21")
    elif chong>time.time(): 
        #chong
        chsecrest=chong-time.time()
        chongarr=time.localtime(chong)
        chdrest=time.localtime(chsecrest)
        chascrest=time.asctime(chongarr)
        chdayrest=calc_days(chongarr)
        chmonthrest=calc_months(chongarr)
        pt=[]
        pt.append(unicode(chascrest))
        pt.append(u'Months: '+unicode(chmonthrest)+' Weeks: '+unicode(chdayrest/7))
        pt.append(u'Days: '+unicode(chdayrest))
        pt.append(u'Hours: '+zadd(chdayrest*24+chdrest[3])+':'+zadd(chdrest[4])+':'+zadd(chdrest[5]))
        pt.append(u'Seconds: '+unicode(int(chsecrest)))
        chongw.show_popup(pt,115,0)
    else:
        chong=None    
    #buttons
    img.rectangle([2,188,57,203],0xffffff)
    img.text((5,200),btn_name,0xffffff)
    img.rectangle([119,188,174,203],0xffffff)
    img.text((148,200),u'EXIT',0xffffff)
    if (chongw.show==1):
      chongw.draw()
    if (popup.show==1):
      popup.draw()
#add zero before number
def zadd(i):
    res=unicode(i)
    if int(i)<10: res='0'+unicode(i)
    return res
#enter chong date
def chong_enter():
    global chong
    chong=appuifw.query(u"Enter DMB date:", 'date',time.time())
#clear chong date
def chong_clear():
    global chong
    chong=None
    chongw.hide_popup()

def take_shot():
    global img
    global scr_name
    img.save(scr_name)
    pt=[]
    pt.append(u'Screenshot saved:')
    pt.append(scr_name)
    popup.show_popup(pt,60,3)
    
def exit():
    global eflag
    eflag=1 
    app_lock.signal()
    appuifw.app.set_exit()

img=None
chong=None
#screen redraw function
def handle_redraw(rect):
    if img:
        canvas.blit(img)

mainw=Popupw()
chongw=Popupw()
popup=Popupw()
appuifw.app.title=u"DMB"
appuifw.app.screen='full'
appuifw.app.body=canvas=appuifw.Canvas(redraw_callback=handle_redraw)
appuifw.app.menu = [(u"Enter date", lambda:chong_enter()),(u"Clear date", lambda:chong_clear()),(u"Take a screenshot", lambda:take_shot())]
appuifw.app.exit_key_handler = exit

img=Image.new(canvas.size)

app_lock = e32.Ao_lock()
eflag=0
while not eflag:
    redraw()
    handle_redraw(())
    e32.ao_yield()

app_lock.wait()