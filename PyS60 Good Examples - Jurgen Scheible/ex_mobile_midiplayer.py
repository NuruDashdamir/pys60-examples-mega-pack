# Copyright (c) 2007 Jurgen Scheible www.mobilenin.com
# play piano on your mobile using keys 1 to 5

import appuifw, key_codes, e32, audio

S1 = audio.Sound.open("E:\\Python\\midi\\c.mid")
S2 = audio.Sound.open("E:\\Python\\midi\\d.mid")
S3 = audio.Sound.open("E:\\Python\\midi\\e.mid")
S4 = audio.Sound.open("E:\\Python\\midi\\f.mid")
S5 = audio.Sound.open("E:\\Python\\midi\\g.mid")

def playsC():
    S1.play(1,0)

def playsD():
    S2.play(1,0)
    
def playsE():
    S3.play(1,0)

def playsF():
    S4.play(1,0)
    
def playsG():
    S5.play(1,0)

def keys(event):
    if event['keycode'] == key_codes.EKey1: playsC()
    if event['keycode'] == key_codes.EKey2: playsD()
    if event['keycode'] == key_codes.EKey3: playsE()
    if event['keycode'] == key_codes.EKey4: playsF()
    if event['keycode'] == key_codes.EKey5: playsG()

def quit():
    S1.close()
    S2.close()
    S3.close()
    S4.close()
    S5.close()
    app_lock.signal()
    appuifw.app.set_exit()

appuifw.app.body = canvas =appuifw.Canvas(event_callback=keys)
appuifw.app.title = u"MidiPlayer"
appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()




