import e32
from appuifw import *

app.screen = 'full'
app.body = canvas = Canvas()
width, height = canvas.size

xaxis = width/2
yaxis = height/1.5
scale = 60
iterations = 25

for y in range(height):
  for x in range(width):
    magnitude = 0
    z = 0+0j
    c = complex(float(y-yaxis)/scale, float(x-xaxis)/scale)
    for i in range(iterations):
      z = z**2+c
      if abs(z) > 2:
        v = 765*i/iterations
        if v > 510:
          color = (255, 255, v%255)
        elif v > 255:
          color = (255, v%255, 0)
        else:
          color = (v%255, 0, 0)
        break
    else:
      color = (0, 0, 0)
    canvas.point((x, y), color)
  e32.ao_yield()
 
lock = e32.Ao_lock()
app.exit_key_handler = lock.signal
lock.wait()
