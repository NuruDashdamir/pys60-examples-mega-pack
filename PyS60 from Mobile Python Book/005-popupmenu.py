
import appuifw

choices = [u"Symbian", u"PyS60", u"MobileArt"]

index = appuifw.popup_menu(choices, u"Select:") 

if index == 0 : 
    appuifw.note(u"Symbian, aha")
elif index == 1 : 
    appuifw.note(u"PyS60 - yeah")
elif index == 2 : 
    appuifw.note(u"I love MobileArt")

