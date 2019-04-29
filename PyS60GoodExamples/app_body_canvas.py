# This script draws different shapes and text to the canvas


import appuifw
from appuifw import *
import e32
# import graphics
from graphics import *



# create an exit handler
def quit():
    global running
    running=0
    appuifw.app.set_exit()

# set the screen size to large
appuifw.app.screen='large'

# define an initial image (white)
img=Image.new((176,208))

# add different shapes and text to the image
# coord. sequence x1,x2,y1,y2
img.line((20,20,20,120),0xff00ee)
img.rectangle((40,60,50,80),0xff0000)
img.point((50.,150.),0xff0000,width=40)
img.ellipse((100,150,150,180),0x0000ff)
img.text((100,80), u'hello')


# define your redraw function (that redraws the picture on and on)
# in this case we redraw the image named img using the blit function
def handle_redraw(rect):
    canvas.blit(img)

running=1

# define the canvas, include the redraw callback function
canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)

# set the app.body to canvas
appuifw.app.body=canvas

app.exit_key_handler=quit


# create a loop to redraw the the screen again and again until the exit button is pressed
while running:
    # redraw the screen
    handle_redraw(())
    # yield needs to be here in order that key pressings can be noticed
    e32.ao_yield()







        


 



