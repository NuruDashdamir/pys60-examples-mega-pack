import sys
import e32
import appuifw
import os

start_timer = e32.Ao_timer()
screensaver_on = True

def u(x):
    return x.decode('utf8')
   
def handle_screensaver():
    global g_screensaver_on
    if screensaver_on:
        e32.reset_inactivity()
        start_timer.cancel()
        start_timer.after(4, handle_screensaver)
    else:
        start_timer.cancel()
   
def bye():
    os.abort()

def main():
    body.color = (0,0,255)
    body.set(u"\n    Your Screensaver now is disable. Do not close this application if you still want the Screensaver disable.\n\n To close this app, please select 'Close Me' from menu.\n\n  Compile by MightyGhost")
        
def help():
    body.color = (0,0,255)
    body.set(u"1. This program is used to pause the screensaver that currently active. That mean,after this program is run, the screensaver will automatically turn off.\n2. The screensaver will be off until this program is close. This mean this program need to be run in background so it will continue working.\n3. The 'Close Me' is use to close this program because the 'Exit' did'nt work.\n4. This program tested on N95-1 and maybe will work on other S60v3 or FP1 phone.\n5. This program is used with other python application that need the screensaver off.")
    body.color = (255,0,0)
    body.add(u"\n\nAuto Return to Menu after 20seconds")
    e32.ao_sleep(20)
    main()
        
def info():
    body.color = (200,0,0)
    body.set(u"\n        Screensaver Killer")
    body.color = (0,150,0)
    body.add(u"\n           Version 1.50")
    body.color = (150,0,0)
    body.add(u"\n        by Mighty Ghost")
    body.color = (0,0,255)
    body.add(u"\n\n   I create this application because I can't find any better solution for disable the screensaver.")
    body.color = (255,0,0)
    body.add(u"\n\n          Have Fun All!")
    e32.ao_sleep(10)
    main()
    
def quit():
    start_timer.cancel()
    app_lock.signal()
   
body = appuifw.Text()
main()
appuifw.app.screen = "full"
appuifw.app.body = body
appuifw.app.exit_key_handler = quit
appuifw.app.menu = [
    (u'Close Me!', bye),
    (u'Help', help),
    (u'About', info),    
    (u"Exit", quit)]
appuifw.app.title = u"ScreenSaver Killer";

handle_screensaver()
app_lock = e32.Ao_lock()
app_lock.wait()