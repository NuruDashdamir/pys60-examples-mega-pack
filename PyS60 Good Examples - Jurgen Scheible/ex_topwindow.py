# Copyright (c) 2006 Jurgen Scheible
# This script allows to show a topwindow on the phone's screen
# in which a blue square appears and on top of it a white square smaller in size.
# Using the application menu the topwindow can be switched on and off.
# NOTE: PyS60 version 1.3.14 or higher is needed to run this script.

import topwindow
import graphics
import appuifw
import e32

screen = topwindow.TopWindow()
img = graphics.Image.new((50,50))
screen.add_image(img, (5,5,45,45))
screen.size = (50, 50)
screen.corner_type = 'square'
screen.background_color = 0xff0000
screen.shadow = 2

def show_screen():
    screen.show()

def hide_screen():    
    screen.hide()

def exit_key_handler():
    app_lock.signal()

app_lock = e32.Ao_lock()

appuifw.app.menu = [(u"show", show_screen),
                    (u"hide", hide_screen)]

appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()
