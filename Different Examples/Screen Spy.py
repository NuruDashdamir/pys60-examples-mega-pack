# screenspy v0.1 for s60, a simple screenshoter, (c) Einhander

import appuifw
import graphics

import e32

running=1
switch = 0
appuifw.app.screen='normal'

def quit():
    global running
    running=0
    appuifw.app.set_exit()


interval = appuifw.query(u"Interval:", "number", 10)

maxscreen = appuifw.query(u"Screenshot number:", "number" ,20)

print "starting"
while running:
    
    if switch < maxscreen:
        
        e32.ao_sleep(interval)
        image = graphics.screenshot()
        switch = switch + 1
        numer = switch
                 
        filename="e:\\python\\picture"+str(numer)+".jpg"
        image.save(filename,quality=25)
        numer = int(0)
    else:    
        print "done"
        quit()
