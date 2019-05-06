import appuifw,e32
from graphics import *
img=Image.new((320,240),"RGB")
def redraw(rect): 
    canvas.blit(img)

canvas=appuifw.Canvas(redraw_callback=redraw)
appuifw.app.screen="full"
appuifw.app.body=canvas
app_lock = e32.Ao_lock() 

def exit():
    app_lock.signal()

appuifw.app.exit_key_handler = exit
pic=Image.new((320,1),"RGB")

def color(color1, color2, pr, max):
    red = (color1[0]*pr + color2[0]*(max-pr) )/max
    green =(color1[1]*pr + color2[1]*(max-pr) )/max
    blue = (color1[2]*pr + color2[2]*(max-pr) )/max
    return (red,green,blue)

c2=(210,200,100)
c1=(250,250,200)
max=pic.size[0]

for x in range(pic.size[0]):
    col = color(c1,c2, max*(max-x)/max, max)
    pic.point((x,0), col)

for y in range(240):
    img.blit(pic,target=(0,y))
redraw(())
app_lock.wait()