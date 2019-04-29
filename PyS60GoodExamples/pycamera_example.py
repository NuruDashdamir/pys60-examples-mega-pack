#PyCamera
#A PyS60 application that can capture images and video
 
#The resolutions, zoom levels and quality of content captured with this application depend on the device that is used
#and on the way certain functions work in PyS60, so don't expect to get top-notch results, as this is only a prototype.
 
 
import appuifw, e32, camera, os
from graphics import *
from key_codes import *
 
app_lock=e32.Ao_lock()
def quit():
	global running
	running=0
	camera.stop_finder()   #Close the viewfinder
	camera.release()       #Release the camera so that other programs can use it
	app_lock.signal()
	appuifw.app.set_exit()
appuifw.app.exit_key_handler=quit
 
def vf(im):appuifw.app.body.blit(im)  #This is used when starting the viewfinder
 
#This function is used when starting to record a video
def video_callback(err, current_state):
    	global control_light   
    	if current_state==camera.EPrepareComplete:control_light=1
 
appuifw.app.title=u"PyCamera"
appuifw.app.orientation="portrait"  #Set the UI orientation
 
#We define the Keyboard class so we can detect keypresses and react accordingly
class Keyboard(object):
	def __init__(self,onevent=lambda:None):
        	self._keyboard_state={}
        	self._downs={}
        	self._onevent=onevent
    	def handle_event(self,event):
        	if event['type']==appuifw.EEventKeyDown:
            		code=event['scancode']
            		if not self.is_down(code):
                		self._downs[code]=self._downs.get(code,0)+1
            		self._keyboard_state[code]=1
        	elif event['type']==appuifw.EEventKeyUp:
            		self._keyboard_state[event['scancode']]=0
        	self._onevent()
    	def is_down(self,scancode):
        	return self._keyboard_state.get(scancode,0)
    	def pressed(self,scancode):
        	if self._downs.get(scancode,0):
            		self._downs[scancode]-=1
            		return True
        	return False
keyboard=Keyboard()
 
 
def photocamera():
	global keyboard, z1, z2, z3, zoom, r1, r2, resolution, q, q1, q2
 
	#We set the tabs of the application
	def handle_tabs(index):
		global lb, videocamera
		if index==0:photocamera()
		if index==1:videocamera()
	appuifw.app.set_tabs([u"Photo", u"Video"], handle_tabs)
 
	#In order to be able to take several pictures and videos, we add a number to the end of their filenames.
	#This number is obtained by checking how many files of that type are saved on the device
	i=len(os.listdir("E:\\Images\\"))
	photo_savepath=u"E:\\Images\\pic%d.jpg" % i
 
	#Make the background a canvas; needed for key capturing
	canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=None)
	appuifw.app.body=canvas
 
	#The default resolution is 0.8 megapixels and the default zoom level is 0
	resolution=(1024, 768)
	r1="X 1024x768"
	r2="640x480"
	zoom=0
	z1="X 0"
	z2=str(camera.max_zoom()/4)
	z3=str(camera.max_zoom()/2)
 
	#These functions set the resolution, zoom and image quality to the selected value
	def set_res_vga():
		global resolution, r1, r2
		resolution=(640, 480)
		r1="1024x768"
		r2="X 640x480"
	def set_res_08():
		global resolution, r1, r2
		resolution=(1024, 768)
		r1="X 1024x768"
		r2="640x480"
 
	def set_zoom_0():
		global zoom, z1, z2, z3
		zoom=0
		z1="X 0"
		z2=str(camera.max_zoom()/4)
		z3=str(camera.max_zoom()/2)
		pic=camera.take_photo('RGB', resolution, zoom)
		camera.stop_finder()
		camera.start_finder(vf, size=(240,180))
	def set_zoom_quarter_max():
		global zoom, z1, z2, z3
		zoom=camera.max_zoom()/4
		z1="0"
		z2="X " + str(camera.max_zoom()/4)
		z3=str(camera.max_zoom()/2)
		pic=camera.take_photo('RGB', resolution, zoom)
		camera.stop_finder()
		camera.start_finder(vf, size=(240,180))
	def set_zoom_half_max():
		global zoom, z1, z2, z3
		zoom=camera.max_zoom()/2
		z1="0"
		z2=str(camera.max_zoom()/4)
		z3="X " + str(camera.max_zoom()/2)
		pic=camera.take_photo('RGB', resolution, zoom)
		camera.stop_finder()
		camera.start_finder(vf, size=(240,180))
 
	def set_qual_50():
		global q, q1, q2
		q=50
		q1="High"
		q2="X Low"
	def set_qual_100():
		global q, q1, q2
		q=100
		q1="X High"
		q2="Low"
 
	#In order for the viewfinder to correspond to the zoom level, we must take a picture (without saving it), close and open the viewfinder
	#These steps are necessary because of the way the functions are currently defined in PyS60, and have a slight impact on performance
	#Future releases of PyS60 may have optimized functions
	pic=camera.take_photo('RGB', resolution, zoom)
	camera.stop_finder()
	camera.start_finder(vf, size=(240,180))
 
	#We now create a loop that "waits" for keys to be pressed
	running=True
	while running:
		if keyboard.pressed(EScancodeSelect):
			pic=camera.take_photo('RGB', resolution, zoom)  #Take the picture
			pic.save(photo_savepath, quality=q)             #Save it
			photocamera()                                   #Restart camera in photo mode
		if keyboard.pressed(EScancodeRightSoftkey):quit()
		appuifw.app.menu=[(u"Zoom", ((u"%s" % z1, set_zoom_0), (u"%s" % z2, set_zoom_quarter_max), (u"%s" % z3, set_zoom_half_max))), (u"Resolution", ((u"%s" % r1, set_res_08), (u"%s" % r2, set_res_vga))), (u"Quality", ((u"%s" % q1, set_qual_100), (u"%s" % q2, set_qual_50))), (u"Exit", quit)]
		e32.ao_yield()
 
def videocamera():
	global keyboard
 
	i=len(os.listdir("E:\\Videos\\"))
	video_savepath=u"E:\\Videos\\vid%d.mp4" % i
 
	canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=None)
	appuifw.app.body=canvas
 
	camera.stop_finder()
	camera.start_finder(vf, size=(240,196))
 
	recording=False
	running=True
	while running:
		if keyboard.pressed(EScancodeSelect):
			if not recording:
				vid=camera.start_record(video_savepath, video_callback)   #Start recording the video
				recording=True
			else:
				camera.stop_record()    #Stop recording
				videocamera()	        #Restart the camera in video mode
		if keyboard.pressed(EScancodeRightSoftkey) and recording:
			camera.stop_record()
			quit()
		appuifw.app.menu=[(u"Exit", quit)]
		e32.ao_yield()
 
#Tell the program to start in photo mode by default, and the default image quality is 100 (best)
q=100
q1="X High"
q2="Low"
photocamera()
 
app_lock.wait()
