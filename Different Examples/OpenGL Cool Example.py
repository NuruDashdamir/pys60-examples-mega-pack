#script by kule
#pergerk@gmail.com
#ICQ 198540475
import e32
import appuifw, glcanvas, graphics
from gles import *
import random
rnd=random.Random()
class GL:
  running = 1
  points=[
   1.0,0.0,0.0, 0.0,1.0,0.0, 0.0,0.0,1.0,
   -1.0,0.0,0.0, 0.0,-1.0,0.0, 0.0,0.0,-1.0,
   0.5,0.0,0.0, 0.0,0.5,0.0, 0.0,0.0,0.5,
   -0.5,0.0,0.0, 0.0,0.5,0.0, 0.0,0.0,0.5
    ]
  for j in xrange(500):
      points.append(rnd.uniform(-4.0,4.0))
      points.append(rnd.uniform(-4.0,4.0))
      points.append(rnd.uniform(-4.0,4.0))
  vertices = array(GL_FLOAT, 3, points )
  points = array(GL_UNSIGNED_BYTE, 1, [j for j in xrange(12,500)])
  line=[]
  for j in xrange(6):
    for i in xrange(6):
       if j<=i:
          line.append(j)
          line.append(i)
  lines = array(GL_UNSIGNED_BYTE, 2, line)
  col=[
    0,255,0,255,  255,0,0,255,
    0,0,255,255,  255,255,0,255,
    0,255,255,255,  0,255,0,255
    ]
  for j in xrange(506):
      col.append(255)
      col.append(255)
      col.append(255)
      col.append(255)
  colors = array(GL_UNSIGNED_BYTE, 4,col)
  def resize(self):
      glViewport(0, 0, self.canvas.size[0], self.canvas.size[1])
      aspect = float(self.canvas.size[1]) / float(self.canvas.size[0])
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glFrustumf(-1.0,1.0,-1.0*aspect,1.0*aspect,3.0,1000.0)
  def initgl(self):
    glClearColor(0.0,0.0,0.0,1.0)
    glEnable(GL_CULL_FACE)
    self.resize()
    glMatrixMode(GL_MODELVIEW)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointerf(self.vertices)
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointerub(self.colors)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_FASTEST)
  def redraw(self,frame):
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    F=frame
    glPushMatrix()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatex(0,0,-100<<16)
    glRotatex(F<<16,1<<16,0,0)
    glRotatex(F<<16,0,1<<16,0)
    glRotatex(F<<16,0,0,1<<16)
    glScalef(30.0,15.0,30.0)
    glDrawElementsub(GL_POINTS, self.points)
    glPopMatrix()
    glPushMatrix()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatex(0,0,-100<<16)
    glRotatex(F<<16,2<<16,0,0)
    glRotatex(-F<<16,0,2<<16,0)
    glRotatex(-F<<16,0,0,2<<16)
    glScalef(15.0 , 15.0 ,15.0 )
    glDrawElementsub(GL_LINES,self.lines)
    glPopMatrix()
  def set_exit(self):
    global canvas
    self.canvas=None
    self.running=0
  def __init__(self):
    appuifw.app.exit_key_handler=self.set_exit
    appuifw.app.screen = 'full'
    self.canvas=glcanvas.GLCanvas(redraw_callback=self.redraw, event_callback=None, resize_callback=self.resize)
    appuifw.app.body=self.canvas
    self.initgl()
    while self.running:
      self.canvas.drawNow()
      e32.ao_sleep(0.0001)
gl=GL()