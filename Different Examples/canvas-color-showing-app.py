#
# Watch Me - Light Now
# Email jouni dot miettunen at gmail dot com
#
# Copyright (c) 2007 - 2008 Jouni Miettunen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
'''
1.2  2008-07-05
     Keep screensaver off with focus callback
     Non-editable About dialog thanx to keycapturer
     RGB value setting with Listbox
1.1  2008-05-30 RGB visualization at Brussels airport
1.0  2008-03-26 Released
'''

VERSION = '1.2'

import sys
import e32
import appuifw
import graphics
import key_codes
import random

# For HELP menu item
import keycapture

# Use current installation directory, c: or e:
FILE_PICKER_NAME = 'WatchMeLightNow.jpg'
FILE_LOG_NAME = 'WatchMeLightNow.txt'

try:
    raise Exception
except Exception:
    filepath = sys.exc_info()[2].tb_frame.f_code.co_filename

import os
filedir, filename = os.path.split(filepath)
FILE_LOG = os.path.join(filedir, FILE_LOG_NAME)
FILE_PICKER = os.path.join(filedir, FILE_PICKER_NAME)
FILE_PNG = os.path.join(filedir, filename + ".png")
del os

STATE_COLOR = 10
STATE_ROTATE = 11
STATE_PICK = 12
g_state = STATE_COLOR

MOVE_UP = 1
MOVE_RIGHT = 2
MOVE_DOWN = 3
MOVE_LEFT = 4

RGB_MIN = 0
RGB_MAX = 255
RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)
RGB_WHITE = (255, 255, 255)
RGB_GRAY = (120, 120, 120)
RGB_BLACK = (0, 0, 0)
(rgb_red, rgb_green, rgb_blue) = RGB_BLUE
dir_red = dir_green = dir_blue = -1

canvas = img = img_pick = None
g_maxx = g_maxy = g_pickx = g_picky = 0
g_rotate_time = 0.01
g_screen_size = "full"
g_show_rgb = True
g_step = 5
lb = None

# Manage screensaver on/off
my_timer = e32.Ao_timer()
rot_timer = e32.Ao_timer()
g_screensaver_on = True

# Help menu item control
capturer = None

def key_checkstate(aState):
    global g_state
    if g_state == aState:
       return True
    else:
       return False

def show_rgb():
    ''' Toggle showing RGB numbers on/off '''
    global g_show_rgb
    if g_show_rgb:
        g_show_rgb = False
    else:
        g_show_rgb = True
    cb_handle_redraw()

def change_screensize():
    ''' Toggle screen between full and normal '''
    global g_screen_size
    if g_screen_size == "full":
        g_screen_size = "normal"
    else:
        g_screen_size = "full"
    appuifw.app.screen = g_screen_size
    cb_handle_resize()

def key_arrow(a_dir):
    ''' Different arrow key handling based on application state '''
    global g_pickx, g_picky, g_step
    if key_checkstate(STATE_PICK):
        if a_dir == MOVE_UP:
            g_picky = max(g_picky-g_step, 0)
        elif a_dir == MOVE_RIGHT:
            g_pickx = min(g_pickx+g_step, g_maxx)
        elif a_dir == MOVE_DOWN:
            g_picky = min(g_picky+g_step,g_maxy)
        elif a_dir == MOVE_LEFT:
            g_pickx = max(g_pickx-g_step, 0)
    else:
        if a_dir == MOVE_UP or a_dir == MOVE_LEFT:
            g_step -= 1
        elif a_dir == MOVE_DOWN or a_dir == MOVE_RIGHT:
            g_step += 1
        if g_step < 1:
            g_step = 1
        elif g_step > 10:
            g_step = 10
    cb_handle_redraw()

def key_selectcolor():
    ''' Different Select key handling based on application state '''
    if key_checkstate(STATE_PICK):
        # Back to single color display
        global g_state, rgb_red, rgb_green, rgb_blue
        g_state = STATE_COLOR
        (rgb_red, rgb_green, rgb_blue) = img.getpixel((g_pickx, g_picky))[0]
        cb_handle_redraw()
    else:
        tmp = graphics.screenshot()
        tmp.save(FILE_PNG)

def key_lesscolor(a_color, a_value):
    if key_checkstate(STATE_COLOR):
        global rgb_red, rgb_green, rgb_blue
        a_value = max(a_value, RGB_MIN)
        if a_color == "red":
            rgb_red = a_value
        elif a_color == "green":
            rgb_green = a_value
        elif a_color == "blue":
            rgb_blue = a_value
        cb_handle_redraw()

def key_morecolor(a_color, a_value):
    if key_checkstate(STATE_COLOR):
        global rgb_red, rgb_green, rgb_blue
        a_value = min(a_value, RGB_MAX)
        if a_color == "red":
            rgb_red = a_value
        elif a_color == "green":
            rgb_green = a_value
        elif a_color == "blue":
            rgb_blue = a_value
        cb_handle_redraw()

def set_fullcolor(a_color):
    if key_checkstate(STATE_COLOR):
        global rgb_red, rgb_green, rgb_blue
        (rgb_red, rgb_green, rgb_blue) = a_color
        cb_handle_redraw()

def validate_rgb(a_value):
    ''' Fit given value inside RGB limits '''
    if a_value < RGB_MIN:
        a_value = RGB_MIN
    elif a_value > RGB_MAX:
        a_value = RGB_MAX
    return a_value

def validate_color(r, g, b):
    r = validate_rgb(r)
    g = validate_rgb(g)
    b = validate_rgb(b)
    return (r, g, b)

def rgb_rotate():
    ''' Color rotation on-screen '''
    rot_timer.cancel()
    global rgb_red, rgb_green, rgb_blue
    global dir_red, dir_green, dir_blue

    # Red
    value = random.choice([0, 1])
    if dir_red < 0:
        value = -value
    rgb_red = validate_rgb(rgb_red + value)
    if rgb_red <= RGB_MIN or rgb_red >= RGB_MAX:
        dir_red = -dir_red
    # Green
    value = random.choice([0, 1, 2])
    if dir_green < 0:
        value = -value
    rgb_green = validate_rgb(rgb_green + value)
    if rgb_green <= RGB_MIN or rgb_green >= RGB_MAX:
        dir_green = -dir_green
    # Blue
    value = random.choice([0, 1, 2, 3])
    if dir_blue < 0:
        value = -value
    rgb_blue = validate_rgb(rgb_blue + value)
    if rgb_blue <= RGB_MIN or rgb_blue >= RGB_MAX:
        dir_blue = -dir_blue
    # Update screen, make it visible
    draw_screen()
    rot_timer.after(g_rotate_time, rgb_rotate)

def cb_listbox():
    ''' RGB query listbox '''
    global lb
    global rgb_red, rgb_green, rgb_blue
    i = lb.current()
    if i == 0:
        a = appuifw.query(u"New \'Red\' value (0-255):", "number", int(rgb_red))
        rgb_red = validate_rgb(a)
    elif i == 1:
        a = appuifw.query(u"New \'Green\' value (0-255):", "number", int(rgb_green))
        rgb_green = validate_rgb(a)
    elif i == 2:
        a = appuifw.query(u"New \'Blue\' value (0-255):", "number", int(rgb_blue))
        rgb_blue = validate_rgb(a)
    entries = [
        (u"Red", unicode(int(rgb_red))),
        (u"Green", unicode(int(rgb_green))),
        (u"Blue", unicode(int(rgb_blue))),
        ]
    lb = appuifw.Listbox(entries, cb_listbox)
    appuifw.app.body = lb

def menu_rgb_query():
    ''' Define listbox for RGB query '''
    global g_state
    g_state = STATE_COLOR

    # Force screen size 'normal', otherwise looks weird
    appuifw.app.screen = "normal"
    entries = [
        (u"Red", unicode(int(rgb_red))),
        (u"Green", unicode(int(rgb_green))),
        (u"Blue", unicode(int(rgb_blue))),
        ]
    global lb
    lb = appuifw.Listbox(entries, cb_listbox)
    appuifw.app.body = lb

    appuifw.app.exit_key_handler = cb_rgb_close
    appuifw.app.menu = [
        (u"Select", cb_listbox),
        (u"Close", cb_rgb_close)]

def cb_rgb_close():
    ''' Close RGB query listbox '''
    appuifw.app.screen = g_screen_size
    appuifw.app.body = canvas
    appuifw.app.exit_key_handler = cb_quit
    appuifw.app.menu = [
        (u"Rotate RGB", menu_rgb_rotate),
        (u"Color Picker", menu_color_picker),
        (u"Set RGB Color", menu_rgb_query),
        (u"About", menu_about),
        (u"Exit", cb_quit)]
    draw_screen()

def menu_rgb_rotate():
    ''' Initialize on-screen color rotation '''
    global g_state
    g_state = STATE_ROTATE
    cb_handle_redraw()
    capturer.start()
    rgb_rotate()

def menu_color_picker():
    ''' Start Color Picker view '''
    global g_state
    g_state = STATE_PICK

def menu_about():
    ''' Create and display About view '''
    t = appuifw.Text()
    t.clear()
    t.color = RGB_BLACK
    t.font = u"title"
    t.style = (appuifw.STYLE_BOLD | appuifw.STYLE_UNDERLINE)
    t.add(u' Watch Me - Light Now \n')
    t.font = u"annotation"
    t.style = 0
    t.color = RGB_RED
    t.add(u' 1 - less  2 - RED    3 - more\n')
    t.color = RGB_GREEN
    t.add(u' 4 - less  5 - GREEN  6 - more\n')
    t.color = RGB_BLUE
    t.add(u' 7 - less  8 - BLUE   9 - more\n')
    t.color = RGB_BLACK
    t.add(u'                0 - Rotate\n')
    t.add(u' Clear key - WHITE\n')
    t.add(u' * - Change screen size\n')
    t.add(u' # - Show / hide RGB values\n')
    t.add(u' Arrow up/down: color step -/+ 1\n')
    t.add(u'\n')
    t.style = appuifw.STYLE_ITALIC
    t.add(u'http://jouni.miettunen.googlepages.com\n')
    t.style = 0
    t.add(u' Version: %s. Jouni Miettunen, 2008\n' % (VERSION))

    appuifw.app.screen = "large"
    appuifw.app.body = t

    # Wait for any key
    capturer.start()

def keycapturer_stop(dummy):
    ''' Special op done, return to normal '''
    capturer.stop()

    global g_state
    g_state = STATE_COLOR

    rot_timer.cancel()
    appuifw.app.screen = g_screen_size
    appuifw.app.body = canvas

def cb_handle_resize(a_size=(0, 0, 0, 0)):
    global canvas
    # Called before log file open !!!
    if canvas != None:
       global g_maxx, g_maxy, img, img_pick, g_pickx, g_picky
       (g_maxx,g_maxy) = canvas.size
       g_maxx -= 1
       g_maxy -= 1
       if g_pickx > g_maxx:
           g_pickx = g_maxx
       if g_picky > g_maxy:
           g_picky = g_maxy
       del img
       img = None
       del img_pick
       img_pick = None
       cb_handle_redraw(a_size)

def cb_handle_redraw(dummy=(0, 0, 0, 0)):
    global canvas, img, img_pick, g_pickx, g_picky
    if img == None:
        img = graphics.Image.new(canvas.size)
    if g_state == STATE_PICK:
        if img_pick == None:
           tmp = graphics.Image.open(FILE_PICKER)
           img_pick = graphics.Image.resize(tmp,canvas.size)
        img.blit(img_pick)
    draw_screen()

def print_value(a_index, a_value, a_color):
    ''' Print selected RGB value on-screen '''
    if img == None:
        return
    str_value = unicode(str(a_value))
    ((top_x, top_y, bot_x, bot_y), dummy, dummy) = \
        img.measure_text(str_value, font="normal")
    x, y = img.size
    mid_x = (x/2) - 1
    if a_index:
        top_x += mid_x - (abs(top_x-bot_x)/2)
        sec_y = y/3
        mid_y = ((a_index-1) * sec_y) + (sec_y/2) - 1
        top_y = mid_y + abs(top_y-bot_y)/2
    else:
        top_y = 30
        top_x = x - 40
    img.text((top_x-1, top_y-1), str_value, RGB_WHITE, 'normal')
    img.text((top_x+1, top_y+1), str_value, RGB_BLACK, 'normal')
    img.text((top_x, top_y), str_value, a_color, 'normal')

def draw_screen():
    ''' Prepare off-screen and show it '''
    if img == None:
        return
    if g_state != STATE_PICK:
        img.clear((rgb_red,rgb_green,rgb_blue))
        if g_show_rgb:
            print_value(0, g_step, RGB_GRAY)
            print_value(1, rgb_red, RGB_RED)
            print_value(2, rgb_green, RGB_GREEN)
            print_value(3, rgb_blue, RGB_BLUE)
    canvas.blit(img)
    if g_state == STATE_PICK:
        c = img.getpixel((g_pickx,g_picky))[0]
        canvas.ellipse((g_pickx-15,g_picky-15,g_pickx+15,g_picky+15), outline=RGB_WHITE, width=2, fill=c)

def handle_screensaver():
    ''' Reset inactivity timer '''
    global g_screensaver_on
    if g_screensaver_on:
        e32.reset_inactivity()
        my_timer.cancel()
        # N82 Settings UI has minimum value 5 seconds
        # Set timeout as 4 seconds
        my_timer.after(4, handle_screensaver)
    else:
        my_timer.cancel()

def cb_focus(fg):
    ''' System callback to tell when focus is lost/regained '''
    global g_screensaver_on
    global g_state
    if fg:
        # Got focus
        g_screensaver_on = True
    else:
        # Lost focus
        g_screensaver_on = False
        g_state = STATE_COLOR
    handle_screensaver()

def cb_quit():
    ''' Prepare for application exit, do clean-up '''
    my_timer.cancel()
    rot_timer.cancel()
    capturer.stop()
    app_lock.signal()

###########################################################
appuifw.app.screen = g_screen_size
canvas = appuifw.Canvas(
    redraw_callback = cb_handle_redraw,
    resize_callback = cb_handle_resize)
appuifw.app.body = canvas
appuifw.app.exit_key_handler = cb_quit
appuifw.app.focus = cb_focus
appuifw.app.menu = [
    (u"Rotate RGB", menu_rgb_rotate),
    (u"Color Picker", menu_color_picker),
    (u"Set RGB Color", menu_rgb_query),
    (u"About", menu_about),
    (u"Exit", cb_quit)]
appuifw.app.title = u"WatchMe LightNow";

# Help menu item controller
capturer = keycapture.KeyCapturer(keycapturer_stop)
capturer.forwarding = 0
capturer.keys = keycapture.all_keys

canvas.bind(key_codes.EKeyHash, lambda: show_rgb())
canvas.bind(key_codes.EKeyStar, lambda: change_screensize())
canvas.bind(key_codes.EKeyLeftArrow, lambda: key_arrow(MOVE_LEFT))
canvas.bind(key_codes.EKeyRightArrow, lambda: key_arrow(MOVE_RIGHT))
canvas.bind(key_codes.EKeyUpArrow, lambda: key_arrow(MOVE_UP))
canvas.bind(key_codes.EKeyDownArrow, lambda: key_arrow(MOVE_DOWN))
canvas.bind(key_codes.EKeySelect, key_selectcolor)
canvas.bind(key_codes.EKeyEnter, key_selectcolor)
canvas.bind(key_codes.EKey0, menu_rgb_rotate)
canvas.bind(key_codes.EKey1, lambda: key_lesscolor("red", rgb_red-g_step))
canvas.bind(key_codes.EKey2, lambda: set_fullcolor(RGB_RED))
canvas.bind(key_codes.EKey3, lambda: key_morecolor("red", rgb_red+g_step))
canvas.bind(key_codes.EKey4, lambda: key_lesscolor("green", rgb_green-g_step))
canvas.bind(key_codes.EKey5, lambda: set_fullcolor(RGB_GREEN))
canvas.bind(key_codes.EKey6, lambda: key_morecolor("green", rgb_green+g_step))
canvas.bind(key_codes.EKey7, lambda: key_lesscolor("blue", rgb_blue-g_step))
canvas.bind(key_codes.EKey8, lambda: set_fullcolor(RGB_BLUE))
canvas.bind(key_codes.EKey9, lambda: key_morecolor("blue", rgb_blue+g_step))
canvas.bind(key_codes.EKeyBackspace, lambda: set_fullcolor(RGB_WHITE))

handle_screensaver()
app_lock = e32.Ao_lock()
app_lock.wait()

# HOX:
# e32.Ao_lock vs. e32.ao_sleep vs. e32.Ao_timer ???
#
# otsov
# (ps. the "e32.ao_sleep()" can be somewhat dangerous to use - the
# application will panic should the user exit during the sleep call,
# please see the API document for more information)

