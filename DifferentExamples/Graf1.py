import e32
import appuifw

def dragon(level, turn):
    global x, y, dx, dy, p
    if level == 0:
        canvas.line((x,y,x+dx,y+dy), 0x0000ff)
        x += dx
        y += dy
        p += 1
        if p % 20 == 0:
            e32.ao_sleep(0.01)
    else:
        dragon(level-1, 0)
        if turn:
            dx, dy = dy, -dx
        else:
            dx, dy = -dy, dx
        dragon(level-1, 1)

def quit():
    appuifw.app.exit_key_handler = None
    lock.signal()

lock = e32.Ao_lock()
old_screen=appuifw.app.screen
old_body=appuifw.app.body
appuifw.app.exit_key_handler = quit
appuifw.app.screen='full'
canvas=appuifw.Canvas()
appuifw.app.body=canvas
x, y = 110, 160
dx, dy = 1, 0
p = 0
dragon(14, 0)
lock.wait()
canvas=None
appuifw.app.body=old_body
appuifw.app.screen=old_screen
