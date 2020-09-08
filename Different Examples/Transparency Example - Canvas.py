import e32,appuifw
from graphics import *

canvas=appuifw.Canvas()
appuifw.app.screen="full"
appuifw.app.body=canvas

img=Image.new((30,30))
img_mask=Image.new((30,30),'L')

img.ellipse((5,5,25,25),0x5555ee,0x5555ee)
img_mask.clear(0)
img_mask.ellipse((5,5,25,25),0x888888,0x888888)

canvas.line((30,0,0,30),0x00dd00,width=5)
canvas.line((0,0,30,30),0xdd0000,width=5)

canvas.blit(img,mask=img_mask)

app_lock = e32.Ao_lock() 
def exit():
  app_lock.signal()
appuifw.app.exit_key_handler = exit

app_lock.wait()