# simple pop-up menu


import appuifw

# create a list with the content of the pop-up note
L = [u"Python", u"Symbian", u"Mlab"]

# create the pop-up menu including the list of content and a label
# -> appuifw.popup_menu(list , label)
test = appuifw.popup_menu(L, u"Select + press OK:")

# the variable test holds the indicator which list item (position in the list)
# has been selected
# trigger some action (here we print something)
if test == 0 :
    appuifw.note(u"Python, yeah", "info")
if test == 1 :
    appuifw.note(u"Symbian, ok", "info")
if test == 2 :
    appuifw.note(u"Mlab, cool students", "info")




