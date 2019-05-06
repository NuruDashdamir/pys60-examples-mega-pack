# created by Ash_Rockit #

import appuifw
import e32
from key_codes import *

##### SETTING #####
appuifw.app.screen = 'normal'

title_x1 = 4
title_y1 = 4
title_x2 = title_x1 + 168
title_y2 = title_y1 + 15

menu_x1 = title_x1
menu_y1 = title_y2 + 2
menu_x2 = menu_x1 + 60
menu_y2 = menu_y1 + (15*8)

cursor_x1 = menu_x1
cursor_y1 = menu_y1
cursor_x2 = menu_x2
cursor_y2 = menu_y1 + 15

color_x1 = menu_x2 + 2
color_y1 = menu_y1
color_x2 = title_x2
color_y2 = menu_y2

color = ('Pink',
 'Red',
 'Green',
 'Blue',
 'Black',
 'Yellow',
 'White',
 'Do you really wanna exit?')

set_color0 = (255,153,204)
set_color1 = (255,0,0)
set_color2 = (0,255,0)
set_color3 = (0,0,255)
set_color4 = (0,0,0)
set_color5 = (255,255,00)
set_color6 = (255,255,255)

title_color = 0xffffff
col_color = set_color0
cursor_color = 0x99cc99
menu_color = 0xccff99
text_color = 0x000000

color_text = color[0]

pos = 0
tm_pos = (10,25,40,55,70,85,100)

##### BEGIN #####
def MENU():
  can.clear()
  can.rectangle((title_x1, title_y1, title_x2, title_y2), 0x000000, fill = (title_color))
  can.rectangle((menu_x1, menu_y1, menu_x2, menu_y2), (menu_color), fill = (menu_color))
  can.rectangle((menu_x1, menu_y1+105, menu_x2, menu_y1+120), 0x99ccff, fill = 0x99ccff)
  can.rectangle((color_x1, color_y1, color_x2, color_y2), (col_color), fill = (col_color))

  can.text((title_x1+10,title_y1+10), unicode(color_text), (text_color))

  can.rectangle((cursor_x1, cursor_y1, cursor_x2, cursor_y2), (cursor_color), fill = (cursor_color))
  can.text((cursor_x1+52, cursor_y1+10), u'>', (text_color))

  for num in range(0,7):
    can.text((menu_x1+8, menu_y1+tm_pos[num]), unicode(color[num]), (text_color))
  can.text((menu_x1+8, menu_y1+115), u'Exit', 0xffffff)

  for pos in range(3):
     can.text((color_x1+3+pos, color_y1+12+pos), u'created by Ash Rockit', 0x000000)
  can.text((color_x1+6, color_y1+15), u'created by Ash Rockit', 0xffffff)
  can.text((color_x1+6, color_y1+30), u'icq: 448060955', 0xffffff)
  can.text((color_x1+6, color_y1+31), u'icq: 448060955', 0x000000)
##########
def UP():
  global cursor_y1, cursor_y2, pos
  if (cursor_y1 - 15) >= menu_y1:
      cursor_y1 -= 15
      cursor_y2 -= 15
      pos -= 1
  else:
      cursor_y1 = menu_y2 - 15
      cursor_y2 = menu_y2
      pos = 7
  COLOR()
  MENU()
##########
def DOWN():
  global cursor_y1, cursor_y2, pos
  if (cursor_y2 + 15) <= menu_y2:
      cursor_y1 += 15
      cursor_y2 += 15
      pos += 1
  else:
      cursor_y1 = menu_y1
      cursor_y2 = menu_y1 + 15
      pos = 0
  COLOR()
  MENU()
##########
def ENTER():
  if pos == 7:
     appuifw.note(u'Bye Bye!', 'info')
     appuifw.app.set_exit()

##########
def COLOR():
  global color_text, col_color
  for num in range(0,8):
    if num == pos:
      color_text = color[num]
  if pos == 0:
    col_color = set_color0
  if pos == 1:
    col_color = set_color1
  if pos == 2:
    col_color = set_color2
  if pos == 3:
    col_color = set_color3
  if pos == 4:
    col_color = set_color4
  if pos == 5:
    col_color = set_color5
  if pos == 6:
    col_color = set_color6
  if pos == 7:
    col_color = set_color4

##########
lock = e32.Ao_lock()
appuifw.app.exit_key_handler = lock.signal
appuifw.app.body = can = appuifw.Canvas()
appuifw.app.title = u"graphic_menu"
##########
can.bind(EKeyUpArrow,lambda:UP())
can.bind(EKeyDownArrow,lambda:DOWN())
can.bind(EKeySelect,lambda:ENTER())
##########
MENU()
lock.wait()

##### END #####