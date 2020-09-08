 
import appuifw, e32, camera,time as t
from graphics import *
 
SCRIPT_LOCK = e32.Ao_lock( )
end = False
stopr = False
stopp = False
stack = []
IMG = None
scapsz = None
sviewsz = None

def __exit__( ):
  global end
  global stopp
  global stopr
  stopp = True
  stopr = True
  end = True
  stop( )
  SCRIPT_LOCK.signal( )
  
def selviewsz():
   iitems = [(176,144),(320,240),(640,480)]
   uitems = [u'176x144',u'320x240',u'640x480']
   index = appuifw.selection_list(uitems)
    
   if index == None:
	index = 2

   return iitems[index]
  
def changeviewsz():
   global sviewsz
   stop()
   sviewsz = None
   start()	
 
def start( ):
    global sviewsz
    
    if sviewsz==None:
    	sviewsz = selviewsz()
	
    camera.start_finder( vfCallback, size=sviewsz)
	    
    appuifw.app.menu = mainmenu_live
 
def stop( ):
    global stopp
    global stopr
    stopp=True
    stopr=True
    camera.stop_finder( )
    cnvCallback( )
    appuifw.app.menu = mainmenu_stopped

def vfCallback( aIm ):
    global stack
    global fps
    global tm2
    global tm
    global fpc
    global fps
    global IMG
    global img
    global txt_img
    global textrect
    fpc=fpc+1
    tm2=t.time()
    if(tm2-tm>=1):
	fps=fpc
	fpc=0
	tm = tm2
    if(len(stack)<60):
    	img.blit(aIm,scale=1)
	appuifw.app.body.blit(img)
	IMG = aIm
	text_img.clear(0)
	text_img.text(((-textrect[0],-textrect[1])),
		unicode(str(fps)),fill=0xff0000,font='normal')
	appuifw.app.body.blit(text_img)
	stack.append(IMG)


def displaytxt(txt, timg, trect):
	timg.text(((-trect[0],-trect[1])),
		unicode(txt),fill=0xff0000,font='normal')

def cnvCallback( aRect=None ):
   appuifw.app.body.clear( )
   #if IMG!=None:     
	#img.blit(IMG,scale=1)
        #appuifw.app.body.blit(img)

def selcapsz():
   iitems = camera.image_sizes()
   uitems = []
   for i in iitems:
	uitems.append(unicode(i))    
   index = appuifw.selection_list(uitems)
    
   if index == None:
	index = 0
   return iitems[index]	

def capture( ):
    global img2
    global textrect2
    global scapsz
  
    stop()
    
    bak = appuifw.app.title
    
    appuifw.app.menu = [(u'Exit', __exit__)]
     
    if scapsz==None:
       	scapsz=selcapsz()
    		
    img2.clear()
    displaytxt("capturing ...",img2, textrect2)
    appuifw.app.body.blit(img2)
    
    displaytxt("capturing ...",img2, textrect2)
    appuifw.app.body.blit(img2)
    
    IMG = camera.take_photo(size = scapsz)
    
    img2.clear()
    displaytxt("saving ...",img2, textrect2)
    appuifw.app.body.blit(img2)
    
    IMG.save(u'c:\\data\\images\\'+str(t.time())+".png",bpp=24,quality=100,compression='no') 
    #IMG.save(u"d:\\tx.png",bpp=24,quality=100,compression='no')  
    start()
    
def save():
   global stack
   global stopr
   global img2
   global textrect2
   stop()	
   stopr = False
   appuifw.app.menu = [(u'Stop', stop)]
   f = open(u'd:\\out.mjpeg',mode='w')
   print "writing %d images to mjpeg"%len(stack)
   displaytxt("saving video ...", img2, textrect2)
   i=0
   tot = len(stack)
   f.write(str(len(stack))+"\n")
   while (len(stack)>0) and not stopr:
		aImg = stack.pop()
		aImg.save(u'd:\\t.jpg')
		f2=open(u'd:\\t.jpg',mode='r')
		bz = f2.read()
		f.write(str(len(bz))+"\n")
		f.write(bz)
		f2.close()
		img2.blit(aImg,scale=1)
		displaytxt("saving "+str(i)+"/"+str(tot),img2, textrect2)
		appuifw.app.body.blit(img2)
		i=i+1
   f.close()
   img2.blit(aImg,scale=1)
   displaytxt("saved video!",img2, textrect2)
   appuifw.app.body.blit(img2)
   stack=[]
   start()
 
def play():
   global img2
   global textrect2
   global stack
   global stopp
   
   f = None
   
   try:
   	f = open(u'd:\\out.mjpeg',mode='r')
   except:
	appuifw.note(u'Save video first!', 'info')
	return
   
   stop()
   stopp = False
   appuifw.app.menu = [(u'Stop', stop)]

   images = int(f.readline())
   tot = images
   i=0
   timage=None
   try:	
	while (images>0) and not stopp:
	   imagel = int(f.readline())
	   bz = f.read(imagel)
	   f2=open(u'd:\\t.jpg',mode='w')
	   f2.write(bz)
	   f2.close()
	   timage=Image.open(u'd:\\t.jpg')
	   img2.blit(timage,scale=1)
	   displaytxt("playing "+str(i)+"/"+str(tot),img2, textrect2)
	   appuifw.app.body.blit(img2)
	   #e32.ao_sleep(0.005)
	   images=images-1
	   i=i+1
   except:
	appuifw.note(u'Corrupt vbuffer', 'info')
	
   if(timage!=None):
   	img2.blit(timage,scale=1)
   displaytxt("playing fin!",img2, textrect2)
   f.close()
   stack=[]
   appuifw.app.menu = mainmenu_play
		
		
mainmenu_live = [(u'Play Video', play),(u'Save Video', save), (u'Capture HQ Image', capture), (u'Change View Size', changeviewsz)]
mainmenu_stopped = [(u'Play Video', play),(u'Save Video', save),(u'Capture HQ Image', capture), (u'Live mode', start)] 
mainmenu_play = [(u'Replay', play),(u'Live mode', start)]		
		
appuifw.app.exit_key_handler = __exit__
appuifw.app.title= u'PyS60 ViewFinder'
appuifw.app.body =  appuifw.Canvas( redraw_callback = cnvCallback)
start( )
fpc = 0
tm = t.time()
fps = 0.0
sz = appuifw.app.body.size
img=Image.new((sz[0],sz[1]*0.75))
#img=Image.new((160,120))
textrect=img.measure_text(u'00', font='normal')[0]
text_img=Image.new((textrect[2]-textrect[0],textrect[3]-textrect[1]))

img2=Image.new((sz[0],sz[1]*0.75))
textrect2=img.measure_text(u'Saving video ...', font='normal')[0]
text_img2=Image.new((textrect2[2]-textrect2[0],textrect2[3]-textrect2[1]))

print appuifw.available_fonts()
print sz
txt=u''
while (not end):
	if(len(stack)>30):
		aImg = stack.pop()
		#if aImg!=None:			
		#	aImg.save(u'd:\\.jpg')
 	
	e32.ao_yield()
	
camera.release()
print "exiting app"
SCRIPT_LOCK.wait()