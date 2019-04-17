# Copyright (c) 2007 Jurgen Scheible
# This script allows setting a default Access Point for connecting to the internet 
# which omits the task of always manually selecting an Access Point each time when you 
# open a Python script that connects to the internet.

import appuifw, socket, urllib, e32

def unset_accesspoint():
    f = open('e:\\apid.txt','w')
    f.write(repr(None))
    f.close()
    appuifw.note(u"Default access point is unset ", "info")


def set_accesspoint():
    apid = socket.select_access_point()
    if appuifw.query(u"Set as default access point","query") == True:
        f = open('e:\\apid.txt','w')
        f.write(repr(apid))
        f.close()
        appuifw.note(u"Saved default access point ", "info")
        apo = socket.access_point(apid)
        socket.set_default_access_point(apo)

def download():
    #---------------------- copy from here ---------------------------------------
    try:
        f=open('e:\\apid.txt','rb')
        setting = f.read()
        apid = eval(setting)
        f.close()
        if not apid == None :
            apo = socket.access_point(apid)
            socket.set_default_access_point(apo)
        else:
            set_accesspoint()
    except:
        set_accesspoint()
    #------------------------- copy till here --------------------------------------
    # and put it before the line of code in your script that invokes a connection to the internet
    # like here with urllib.urlretrieve(url, tempfile)

    # your own code here
    url = "http://www.leninsgodson.com/courses/pys60/resources/vid001.3gp"
    tempfile = 'e:\\Videos\\video.3gp'
    urllib.urlretrieve(url, tempfile)
    appuifw.note(u"Video downloaded" , "info")


def quit():
    app_lock.signal()
    appuifw.app.set_exit()

appuifw.app.menu = [(u"unset ap",unset_accesspoint),(u"download",download)]
appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()




