# Copyright (c) 2005 Jurgen Scheible
# simple pop-up menu


import appuifw

L = [u"Python", u"Symbian", u"Mlab"]

test = appuifw.popup_menu(L, u"Select + press OK:")

if test == 0 :
    appuifw.note(u"Python, yeah", "info")
elif test == 1 :
    appuifw.note(u"Symbian, ok", "info")
elif test == 2 :
    appuifw.note(u"Mlab, cool students", "info")




