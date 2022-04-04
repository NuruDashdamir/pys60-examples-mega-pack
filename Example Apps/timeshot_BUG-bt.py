import e32, time
import socket
import appuifw
import graphics
from time import sleep



index = 2
    
if index == 2 :

    nameOfProject = appuifw.query(u"Set name for the (.jpg) file: ", "text")
    numImages = 1
    delay = appuifw.query(u"Set Time Trigger(after how many seconds screenshot is taken):", "number")


    ImagequalityDisplay = [u'Low Quality',u'Medium Quality',u'High Quality']
    Imagequality = [(85),(92),(100)]
    ImagequalitySelect = appuifw.selection_list(choices=ImagequalityDisplay)
    appuifw.note(u"OK time is running, press Symbian button to return in menu!","info")
    
    x =  0
    while x != numImages:
            sleep(delay)
            image = graphics.screenshot() 
            file ='C:\\Data\\Images\\'+nameOfProject+'.jpg'
            image.save(file,quality=Imagequality[ImagequalitySelect])
            appuifw.note(u"Screenshot saved in C:\u005CData\u005CImages\u005C","conf",1)
            appuifw.note(u"Return in TimeShot to send picture using bluetooth.","conf",1)  
            x +=1
           
           


    def quit():  
        app_lock.signal()
        appuifw.app.exit_key_handler = quit  
        app_lock = e32.Ao_lock()  
        app_lock.wait()
  
      
      
def bt_send():
    device=socket.bt_obex_discover()
    print 'device:', device 
    address=device[0]
    print 'address:', address 
    channel=device[1][u'OBEX Object Push']
    print 'channel:', channel 
    socket.bt_obex_send_file(address,channel,file)
    appuifw.note(u"Image sent!","info")
 

app_lock = e32.Ao_lock()
appuifw.app.title = u"Send screenshot by bluetooth!"
appuifw.app.menu = [(u"Start sending...!", bt_send)]
app_lock.wait()        


