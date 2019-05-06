import appuifw
import e32

def hsv_to_rgb(h, s, v):
    if s == 0.0: return v, v, v
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    if i%6 == 0: return v, t, p
    if i == 1: return q, v, p
    if i == 2: return p, v, t
    if i == 3: return p, q, v
    if i == 4: return t, p, v
    if i == 5: return v, p, q
    # Cannot get here

class Mandelbrot:

    def __init__(self):
        self.canvas=appuifw.Canvas()
        self.old_body=appuifw.app.body
        self.old_screen=appuifw.app.screen
        appuifw.app.body=self.canvas
        appuifw.app.screen='full'
        self.max = 32
        self.w, self.h = self.canvas.size
        self.palette()
        self.lock = e32.Ao_lock()            
        appuifw.app.exit_key_handler = self.quit

    def quit(self):
        appuifw.app.exit_key_handler = None 
        self.lock.signal()                       

    def cleanup(self):
        self.lock.wait()
        appuifw.app.body=self.old_body
        appuifw.app.screen=self.old_screen

    def iterate(self, x, y):
        c = complex(x, y)
        z = 0
        n = 0
        while n < self.max and abs(z) < 2.0:
            z = z*z + c
            n = n + 1
        return n

    def palette(self):
        self.p = []
        for n in range(self.max):
            h = n * 1.0 / self.max
            r, g, b = hsv_to_rgb(h, 0.5, 1.0)
            c = (int(r*255), int(g*255), int(b*255))
            self.p.append(c)
        self.p.append((0,0,0))

    def redraw(self):
        for v in range(self.h):
            x = -2.25 + v * 3.25 / self.h
            for u in range(self.w):
                y = -1.375 + u * 2.75 / self.w
                n = self.iterate(x, y)
                self.canvas.point((u,v), self.p[n])
            e32.ao_sleep(0.01)

m = Mandelbrot()
m.redraw()
m.cleanup()
