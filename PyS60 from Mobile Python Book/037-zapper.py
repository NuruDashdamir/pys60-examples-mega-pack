
import key_codes, appuifw, e32, graphics, random

MAX_UFO_SIZE = 50
MAX_UFOS = 7
UFO_TIME = 100.0

PAD_W = 40
PAD_H = 15
PAD_COLOR = (12, 116, 204)
PAD_SPEED = 7
LASER_COLOR = (255, 0, 204)
TIME = 1000

def handle_redraw(rect):
        global shoot, sleep, ufos, timer
        buf.clear((0, 0, 0))
        buf.rectangle((pad_x, H - PAD_H, pad_x + PAD_W, H),\
                fill = PAD_COLOR)

        if shoot:
                x = pad_x + PAD_W / 2
                buf.line((x, H - PAD_H, x, 0),\
                        width = 2, outline = LASER_COLOR)
                shoot = False
                sleep = 0.1
                check_hits(x)
        else:
                sleep = 0.01
        
        for x, y, s, t, hit in ufos:
                f = 1.0 - (timer - t) / UFO_TIME
                if hit:
                        c = (255, 0, 0)
                else:
                        c = (0, f * 255, 0)
                buf.ellipse((x, y, x + s, y + s), fill = c)

        buf.text((10, 40), u"%d" % score,
                fill = LASER_COLOR, font = "title")
        
        buf.text((W - 70, 40), u"%d" % (TIME - timer),
                fill = LASER_COLOR, font = "title")
        
        canvas.blit(buf)


def check_hits(laser_x):
        global ufos, score
        i = 0
        ok_ufos = []
        for x, y, s, t, hit in ufos:
                if laser_x > x and laser_x < x + s:
                        ok_ufos.append((x, y, s, t, True))
                        score += MAX_UFO_SIZE - (s - 1)
                else:
                        ok_ufos.append((x, y, s, t, False))
        ufos = ok_ufos

def update_ufos():
        global ufos, timer
        ok_ufos = []
        for x, y, s, t, hit in ufos:
                if not hit and timer < t + UFO_TIME:
                        ok_ufos.append((x, y, s, t, False))
        ufos = ok_ufos
        
        if len(ufos) < MAX_UFOS:
                s = random.randint(10, MAX_UFO_SIZE)
                x = random.randint(0, W - s)
                y = random.randint(0, H - PAD_H * 3)
                t = random.randint(0, UFO_TIME)
                ufos.append((x, y, s, timer + t, False))


def handle_event(event):
        global direction, shoot
        if event['keycode'] == key_codes.EKeyLeftArrow:
                direction = -PAD_SPEED
        elif event['keycode'] == key_codes.EKeyRightArrow:
                direction = PAD_SPEED
        elif event['keycode'] == key_codes.EKeySelect:
                shoot = True

def quit():
        global timer
        timer = TIME

ufos = []
shoot = False
direction = pad_x = score = timer = 0
appuifw.app.exit_key_handler = quit
appuifw.app.screen = 'large'
canvas = appuifw.Canvas(event_callback = handle_event,\
                        redraw_callback = handle_redraw)
W, H = canvas.size
buf = graphics.Image.new((W, H))
appuifw.app.body = canvas 

while timer < TIME:
        pad_x += direction
        pad_x = min(pad_x, W - PAD_W)
        pad_x = max(pad_x, 0)

        update_ufos()
        handle_redraw((W, H))
        e32.ao_sleep(sleep)
        timer += 1

print "Your final score was %d!" % score
