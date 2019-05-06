#рисует точку и выводит ее
import time
import appuifw
import e32
from graphics import*

appuifw.app.screen='normal'
appuifw.app.body=canvas=appuifw.Canvas(event_callback=None, redraw_callback=None)
img=Image.new((176,144))

t1=time.clock()
img.clear(0)
for x in range(0,176):
    for y in range(0,144):
        img.point((x,y),0xffffff)
        canvas.blit(img)
img.text((0,9),unicode(str(time.clock()-t1)),0xff0000)
canvas.blit(img)
e32.ao_sleep(3)