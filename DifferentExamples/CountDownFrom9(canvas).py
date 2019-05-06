#
# Count Down
#
# Copyright (c) 2008 Jouni Miettunen
# http://jouni.miettunen.googlepages.com/
#
import e32
import appuifw
import graphics
import key_codes

VERSION = 1.1

# Color definitions
RGB_BLACK = (0,0,0)
RGB_YELLOW = (255,255,0)

# Global variables with safe default values
canvas = None
img = None
gCount = 9
gColor = RGB_YELLOW

# Create timer
gTimer = e32.Ao_timer()

# Speed up drawing by calculating points beforehands
#   a1   a2
#   b1   b2
#   c1   c2
gPointA1 = (0,0)
gPointA2 = (0,0)
gPointB1 = (0,0)
gPointB2 = (0,0)
gPointC1 = (0,0)
gPointC2 = (0,0)

def draw_count(aValue):
   # Draw a number, stop at negative values
   if aValue < 0: return
   global gCount
   gCount = aValue

   # Set coordinates for drawing new number
   points = []
   if gCount == 0:
      points += gPointA1 + gPointA2 + gPointB2 + gPointC2 + gPointC1 + gPointB1 + gPointA1
   elif gCount == 1:
      points += gPointA2 + gPointB2 + gPointC2
   elif gCount == 2:
      points += gPointA1 + gPointA2 + gPointB2 + gPointB1 + gPointC1 + gPointC2
   elif gCount == 3:
      points += gPointA1 + gPointA2 + gPointB2 + gPointB1 + gPointB2 + gPointC2 + gPointC1
   elif gCount == 4:
      points += gPointA1 + gPointB1 + gPointB2 + gPointA2 + gPointC2
   elif gCount == 5:
      points += gPointA2 + gPointA1 + gPointB1 + gPointB2 + gPointC2 + gPointC1
   elif gCount == 6:
      points += gPointA2 + gPointA1 + gPointC1 + gPointC2 + gPointB2 + gPointB1
   elif gCount == 7:
      points += gPointA1 + gPointA2 + gPointC2
   elif gCount == 8:
      points += gPointB1 + gPointA1 + gPointA2 + gPointC2 + gPointC1 + gPointB1 + gPointB2
   elif gCount == 9:
      points += gPointB2 + gPointB1 + gPointA1 + gPointA2 + gPointC2 + gPointC1
   else:
      # Should never get here, but avoid problems anyway
      gCount = 0
      points = gPointA1

   # Color depends on number, just for fun
   color = gCount*25
   gColor = (255, color, 0)

   # Remove old and draw new number
   # Version 1.0 colors
   # img.clear(RGB_BLACK)
   # img.line(points, width=40, outline=gColor)
   # Version 1.1 colors
   img.clear(gColor)
   img.line(points, width=40, outline=RGB_BLACK)
   canvas.blit(img)

   # Must reset timer, user can restart at any time
   gTimer.cancel()
   # Next number in one second
   gTimer.after(1,lambda:draw_count(gCount-1))

def cb_handle_redraw(aRect=(0,0,0,0)):
   if not canvas: return
   if img: canvas.blit(img)

def cb_handle_resize(aSize=(0,0,0,0)):
   global canvas, img
   if not canvas: return

   # Initialize drawing coordinate
   if img: del img
   img = graphics.Image.new(canvas.size)
   x,y = canvas.size
   x1 = 40       # my draw limit at left column
   x2 = x - 40   # my draw limit at right column
   x5 = x/2      # my draw limit at middle column
   y1 = 40       # my draw limit at top row
   y2 = y - 40   # my draw limit at bottom row
   y5 = y/2      # my draw limit at middle row

   # Define new drawing coordinates in advance
   global gPointA1, gPointA2, gPointB1, gPointB2, gPointC1, gPointC2
   gPointA1 = (x1, y1)
   gPointA2 = (x2, y1)
   gPointB1 = (x1, y5)
   gPointB2 = (x2, y5)
   gPointC1 = (x1, y2)
   gPointC2 = (x2, y2)

   # Draw last number again due screen resize request
   draw_count(gCount)
   cb_handle_redraw()

def menu_start():
  draw_count(9)

def cb_quit():
  gTimer.cancel()
  app_lock.signal()

#############################################################
appuifw.app.screen = 'full'
appuifw.app.title = u'Count Down'
appuifw.app.exit_key_handler = cb_quit
appuifw.app.menu = [
    (u"Start", menu_start),
    (u"Exit", cb_quit)
    ]

canvas = appuifw.Canvas(
       resize_callback = cb_handle_resize,
       redraw_callback = cb_handle_redraw)
img = graphics.Image.new(canvas.size)

# Calls automatically resize_callback and redraw_callback
appuifw.app.body = canvas

# Key handling
canvas.bind(key_codes.EKeyEnter, menu_start)
canvas.bind(key_codes.EKeySelect, menu_start)
canvas.bind(key_codes.EKey0, lambda: draw_count(0))
canvas.bind(key_codes.EKey1, lambda: draw_count(1))
canvas.bind(key_codes.EKey2, lambda: draw_count(2))
canvas.bind(key_codes.EKey3, lambda: draw_count(3))
canvas.bind(key_codes.EKey4, lambda: draw_count(4))
canvas.bind(key_codes.EKey5, lambda: draw_count(5))
canvas.bind(key_codes.EKey6, lambda: draw_count(6))
canvas.bind(key_codes.EKey7, lambda: draw_count(7))
canvas.bind(key_codes.EKey8, lambda: draw_count(8))
canvas.bind(key_codes.EKey9, lambda: draw_count(9))

#############################################################
app_lock = e32.Ao_lock()
app_lock.wait()
