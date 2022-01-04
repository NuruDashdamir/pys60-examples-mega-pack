# Copyright (c) 2006 Jurgen Scheible
# Sound recording / playing script 

import appuifw, e32, audio

filename = 'e:\\boo.wav'

def recording():
    global S
    S=audio.Sound.open(filename)
    S.record()
    print "Recording on! To end it, select stop from menu!"

def playing():
    global S
    try:
        S=audio.Sound.open(filename)
        S.play()
        print "Playing"
    except:
        print "Record first a sound!"

def closing():
    global S
    S.stop()
    S.close()
    print "Stopped"

def quit():
    script_lock.signal()
    appuifw.app.set_exit()

appuifw.app.menu = [(u"play", playing),
                    (u"record", recording),
                    (u"stop", closing)]

appuifw.app.title = u"Sound recorder"

appuifw.app.exit_key_handler = quit
script_lock = e32.Ao_lock()
script_lock.wait()


 

