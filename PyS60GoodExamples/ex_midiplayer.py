# playing Midi  

import appuifw
import e32
import audio


def playsound1():
    S = audio.Sound.open("E:\\sound1.mid")
    S.play()
    menu()
    
def playsound2():
    S = audio.Sound.open("E:\\sound2.mid")
    S.play()
    menu()


def exit_key_handler():
    appuifw.app.set_exit()
    
def quit():
    appuifw.app.set_exit()

L = [u"sound 1", u"sound 2", u"exit"]

def menu():
    index = appuifw.popup_menu(L,u'select')
    if index == 0:
        playsound1()
    if index == 1:
        playsound2()
    if index == 2:
        quit()
        
appuifw.app.title = u"Midi player"

appuifw.app.exit_key_handler = exit_key_handler
menu()
    
    
        
        
    




 

