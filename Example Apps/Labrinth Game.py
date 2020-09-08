'''
Mazing Days - Simple maze

jouni dot miettunen at iki dot fi
http://jouni.miettunen.googlepages.com

1.00 2008-10-31 First public release, no changes
0.5  2008-09-08 Demo for Mobile Games Innovation Challenge
0.4  2008-07-13 Animation continues
0.3  2008-06-02 First try with continuous animation
0.2  2008-05-27 Animation at S60 Summit 2008 Barcelona
0.1  2008-05-20 Started at Budapest
'''

NAME = u"Mazing Days"
VERSION = u'1.0'

import os
import sys
import e32
import appuifw
import graphics
import key_codes
import random
import time

# SENSOR: if exception, it's not available in this device
SENSOR_ACC = False
sensor_acc = None
sensor_stab = 10
s_zero1 = 0
s_zero2 = 0
try:
    import sensor
    from sensor import orientation
    SENSOR = True                # Sensor interface available
except ImportError:
    SENSOR = False               # Sensor interface not available

# Global definitions
FLAG_OPEN_UP = 0x01
FLAG_OPEN_LEFT = 0x02
FLAG_OPEN_DOWN = 0x04
FLAG_OPEN_RIGHT = 0x08
FLAG_PATH = 0x10
FLAG_STEP = 0x20
FLAG_USER = 0x40      # Doesn't have to be flag
FLAG_GOAL = 0x80      # Doesn't have to be flag

LEVEL_EASY = 24
LEVEL_MEDI = 12
LEVEL_HARD = 6
TILE_SIZE = LEVEL_EASY

# Global definitions
MOVE_NONE = 0
MOVE_UP = FLAG_OPEN_UP
MOVE_DOWN = FLAG_OPEN_DOWN
MOVE_LEFT = FLAG_OPEN_LEFT
MOVE_RIGHT = FLAG_OPEN_RIGHT

RUN_EXIT = 0
RUN_PLAY = 1
RUN_SOLVED = 2

RGB_BLACK = (0, 0, 0)
RGB_BLUE = (0, 0, 255)
RGB_RED = (255, 0, 0)
RGB_WHITE = (255, 255, 255)

# Global variables
running = RUN_EXIT
board = None
canvas = None
img = None
im1 = None
pic = None
pic_orig = None
animation_timer = None

my_lock = False
my_timer = e32.Ao_timer()

# Manage screensaver on/off
screen_timer = e32.Ao_timer()
g_screensaver_on = True

def cb_handle_redraw(a_rect=(0, 0, 0, 0)):
    ''' Overwrite default screen redraw event handler '''
    if img:
        canvas.blit(img)

def cb_focus(fg):
    ''' System callback to tell when focus is lost/regained '''
    global g_screensaver_on
    if fg:
        # Got focus
        handle_screensaver()
        if SENSOR_ACC:
            sensor_acc.connect(m.handle_sensor_raw)
    else:
        # Lost focus
        g_screensaver_on = False
        screen_timer.cancel()
        if SENSOR_ACC:
            sensor_acc.disconnect()

def handle_screensaver():
    ''' Reset inactivity timer '''
    global g_screensaver_on
    e32.reset_inactivity()
    g_screensaver_on = True
    screen_timer.cancel()
    screen_timer.after(4, handle_screensaver)

#############################################################
class Board(object):
    ''' Game play related operations '''
    def __init__(self, a_size):
        self.x = self.y = 0
        self.board_x = 2
        self.board_y = 2
        self.tile_width = self.tile_height = a_size
        self.next = None
        # Change level means change tile size
        global im1
        del im1
        im1 = None

    def initialize(self):
        ''' Setup new maze '''
        global running, my_lock
        running = RUN_PLAY
        my_lock = True
        my_timer.cancel()

        x,y = canvas.size
        self.board_x = x / self.tile_width
        self.board_y = y / self.tile_height
        self.board = [[0] * self.board_y for i in range(self.board_x)]
        self.x = self.y = 0
        self.make_maze(0, 0)
        self.x = self.y = 0
        self.board[self.x][self.y] |= FLAG_USER
        self.board[self.board_x-1][self.board_y-1] |= FLAG_GOAL

        my_lock = False

    def count_openings(self, x, y):
        ''' How many cell walls are open '''
        if x<0 or x>=self.board_x or y<0 or y>=self.board_y:
            return 5
        else:
            return self.board[x][y]

    def can_walk(self, x, y):
        ''' Which direction can I go from given cell '''
        # Can go to Right
        if self.count_openings(x+1, y) == 0:
            return True
        # Can go to Up
        elif self.count_openings(x, y-1) == 0:
            return True
        # Can go to Left
        elif self.count_openings(x-1, y) == 0:
            return True
        # Can go to Down
        elif self.count_openings(x, y+1) == 0:
            return True
        # Cannot go any direction
        else:
            return False

    def get_new_location(self, x, y):
        ''' Get a random usable location in maze '''
        i = random.choice(range(self.board_x))
        j = random.choice(range(self.board_y))
        while i<self.board_x:
            while j<self.board_y:
                if self.board[i][j] and self.can_walk(i, j):
                    self.x = i
                    self.y = j
                    return True
                j += 1
            j = 0
            i += 1

        i = 0
        j = 0
        while i<self.board_x:
            while j<self.board_y:
                if self.board[i][j] and self.can_walk(i, j):
                    self.x = i
                    self.y = j
                    return True
                j += 1
            j = 0
            i += 1

        return False

    def make_maze(self, x, y):
        ''' Make a new maze '''
        counter = self.board_x * self.board_y - 1

        GO_UP = 0
        GO_DOWN = 1
        GO_LEFT = 2
        GO_RIGHT = 3

        while counter >= 0:
            # Can we continue
            if not self.can_walk(self.x, self.y):
                # Get new starting location
                if not self.get_new_location(self.x, self.y):
                    return

            # Get random direction
            if self.x == 0:
                i = GO_RIGHT
            elif self.y == 0:
                i = GO_DOWN
            elif self.x == self.board_x-1:
                i = GO_LEFT
            elif self.y == self.board_y-1:
                i = GO_UP
            else:
                i = random.choice([GO_UP, GO_DOWN, GO_LEFT, GO_RIGHT])

            # Try to go that direction, else find next best
            # Left
            if i == GO_LEFT:
                xx = -1
                yy = 0
                if self.count_openings(self.x+xx, self.y+yy):
                    i = GO_RIGHT
            # Right
            if i == GO_RIGHT:
                xx = 1
                yy = 0
                if self.count_openings(self.x+xx, self.y+yy):
                    i = GO_UP
            # Up
            if i == GO_UP:
                xx = 0
                yy = -1
                if self.count_openings(self.x+xx, self.y+yy):
                    i = GO_DOWN
            # Down
            if i == GO_DOWN:
                xx = 0
                yy = 1
                if self.count_openings(self.x+xx, self.y+yy):
                    i = GO_LEFT
            # Left again
            if i == GO_LEFT:
                xx = -1
                yy = 0
                if self.count_openings(self.x+xx, self.y+yy):
                    i = GO_RIGHT
            # Right again
            if i == GO_RIGHT:
                xx = 1
                yy = 0
                if self.count_openings(self.x+xx, self.y+yy):
                    i = GO_UP
            # Up again
            if i == GO_UP:
                xx = 0
                yy = -1

            # Go random distance, prefer horizontal zigzag
            dist = [1, 2, 3]
            if i == GO_LEFT or i == GO_RIGHT:
                dist.append(4)
            j = random.choice(dist)

            # Walk chosen distance into chosen direction
            while 1:
                 counter = counter - 1
                 if i == GO_LEFT:
                     self.board[self.x][self.y] |= FLAG_OPEN_LEFT
                 elif i == GO_RIGHT:
                     self.board[self.x][self.y] |= FLAG_OPEN_RIGHT
                 elif i == GO_UP:
                     self.board[self.x][self.y] |= FLAG_OPEN_UP
                 elif i == GO_DOWN:
                     self.board[self.x][self.y] |= FLAG_OPEN_DOWN

                 self.x += xx
                 self.y += yy

                 if i == GO_LEFT:
                     self.board[self.x][self.y] |= FLAG_OPEN_RIGHT
                 elif i == GO_RIGHT:
                     self.board[self.x][self.y] |= FLAG_OPEN_LEFT
                 elif i == GO_UP:
                     self.board[self.x][self.y] |= FLAG_OPEN_DOWN
                 elif i == GO_DOWN:
                     self.board[self.x][self.y] |= FLAG_OPEN_UP

                 j = j - 1
                 if j <= 0 or self.count_openings(self.x+xx, self.y+yy) != 0:
                     break

    def draw_board(self):
        ''' Redraw and show the whole game board '''
        self.draw_alltiles()
        cb_handle_redraw(())

    def solved(self):
        ''' Is game finished or not '''
        # Last cell is the goal
        if self.x == self.board_x-1 and self.y == self.board_y-1:
            return True
        else:
            return False

# TODO not a move but movement direction until something
# - New movement direction
# - Cannot move any more == stop movement don't keep hitting wall !!!

    def handle_movement(self, a_dir):
        ''' Take all movement first here '''
        if my_lock:
            self.next = a_dir
        else:
            self.do_movement(a_dir)

    def next_movement(self):
        ''' Is there next movement waiting '''
        if self.next:
            my_timer.cancel()
            a = self.next
            self.next = None
            my_timer.after(0.01, lambda:self.do_movement(a))
        else:
            global my_lock
            my_lock = False

    def do_movement(self, a_dir):
        ''' Make one move on board '''
        global my_lock
        my_lock = True

        # Test whether requested direction is allowed
        if not (self.board[self.x][self.y] & a_dir):
            self.next_movement()
            return

        if a_dir == MOVE_LEFT:
            dx = -1
            dy = 0
        elif a_dir == MOVE_RIGHT:
            dx = 1
            dy = 0
        elif a_dir == MOVE_UP:
            dx = 0
            dy = -1
        elif a_dir == MOVE_DOWN:
            dx = 0
            dy = 1
        else:
            self.next_movement()
            return

        old_x = self.x
        old_y = self.y
        new_x = self.x + dx
        new_y = self.y + dy

        old_trail = self.board[new_x][new_y] & FLAG_PATH
        self.draw_animate(old_x, old_y, dx, dy, old_trail, self.tile_width/2)

        # Create or clear a trail of small dots
        if old_trail:
            # Moving backwards into old visited tile
            self.board[old_x][old_y] &= ~FLAG_PATH
            self.board[new_x][new_y] &= ~FLAG_PATH
            self.board[old_x][old_y] |= FLAG_STEP
        else:
            # Moving forwards into new unvisited tile
            self.board[old_x][old_y] |= FLAG_PATH

        self.board[old_x][old_y] &= ~FLAG_USER
        self.board[new_x][new_y] |= FLAG_USER
        self.draw_onetile(old_x, old_y)
        self.draw_onetile(new_x, new_y)
        self.x = new_x
        self.y = new_y
        cb_handle_redraw()

        if self.solved():
            running = RUN_SOLVED
            appuifw.note(u'Aferin leyn! Kerata!')
        else:
            self.next_movement()

    def draw_alltiles(self):
        ''' Create complete game board on off-screen '''
        img.clear(RGB_WHITE)
        for y in range(self.board_y):
            for x in range(self.board_x):
                self.draw_onetile(x, y)

    def draw_onetile(self, x, y):
        ''' Draw one tile on off-screen table '''
        top_x, top_y = self.screen_coord(x, y)
        bot_x = top_x + self.tile_width
        bot_y = top_y + self.tile_height
        value = self.board[x][y]

        # Clear previous image
        img.rectangle((top_x, top_y, bot_x, bot_y), \
            outline=RGB_WHITE, fill=RGB_WHITE)

        global im1
        if not im1:
            x = self.tile_width - 1
            y = self.tile_height - 1
            im1 = graphics.Image.new((x, y))
            im1.clear((220,255,0))
            im1.ellipse((0,0,x,y), outline=RGB_BLUE, fill=RGB_BLUE)

        # Special tiles
        if value & FLAG_USER:
            img.blit(im1, target=(top_x+1, top_y+1))
        elif value & FLAG_PATH:
            #img.point((top_x+self.tile_width/2, top_y+self.tile_height/2), width=3, outline=RGB_BLUE)
            img.rectangle((top_x, top_y, bot_x, bot_y), \
                outline=(220,255,0), fill=(220,255,0))
        elif value & FLAG_STEP:
            img.point((top_x+self.tile_width/2, top_y+self.tile_height/2), width=3, outline=(173,216,230))
        if value & FLAG_GOAL:
            img.ellipse((top_x,top_y,bot_x,bot_y), width=2, outline=RGB_RED)

        # Draw walls
        if not (value & FLAG_OPEN_UP):
            img.line ((top_x, top_y, bot_x, top_y), outline=RGB_BLACK, fill=RGB_BLACK)
        if not (value & FLAG_OPEN_LEFT):
            img.line ((top_x, top_y, top_x, bot_y), outline=RGB_BLACK, fill=RGB_BLACK)
        if not (value & FLAG_OPEN_DOWN):
            img.line ((top_x, bot_y, bot_x, bot_y), outline=RGB_BLACK, fill=RGB_BLACK)
        if not (value & FLAG_OPEN_RIGHT):
            img.line ((bot_x, top_y, bot_x, bot_y), outline=RGB_BLACK, fill=RGB_BLACK)

    def draw_animate(self, x, y, dx, dy, a_value, a_step):
        ''' Animate user movement '''
        top_x, top_y = self.screen_coord(x, y)
        bot_x = top_x + self.tile_width
        bot_y = top_y + self.tile_height

        off_x = off_y = 0
        if dx:
            off_x = dx * (self.tile_width / a_step)
        if dy:
            off_y = dy * (self.tile_height / a_step)

        if a_value:
            color = RGB_WHITE
        else:
            color = (220,255,0)

        animation_timer.cancel()
        while a_step>0:
            img.rectangle((top_x+1, top_y+1, bot_x, bot_y), \
                outline=color, fill=color)
            top_x += off_x
            top_y += off_y
            bot_x += off_x
            bot_y += off_y
            img.blit(im1, target=(top_x+1, top_y+1))
            cb_handle_redraw()
            a_step -= 1
            animation_timer.after(0.01)

        top_x, top_y = self.screen_coord(x+dx, y+dy)
        bot_x = top_x + self.tile_width
        bot_y = top_y + self.tile_height
        img.rectangle((top_x+1, top_y+1, bot_x, bot_y), \
            outline=color, fill=color)
        img.blit(im1, target=(top_x+1, top_y+1))
        cb_handle_redraw()

    def screen_coord(self, x, y):
        ''' Get screen coordinates from table coordinates '''
        return x*self.tile_width, y*self.tile_height

#############################################################
class Main(object):
    ''' Application related things '''

    def __init__(self):
        self.screen_size = 'full'
        self.orientation = 'portrait'
        appuifw.app.screen = self.screen_size
        appuifw.app.title = NAME
        appuifw.app.exit_key_handler = self.cb_quit
        appuifw.app.focus = cb_focus
        self.init_menu()

        global canvas
        canvas = appuifw.Canvas(
             redraw_callback = cb_handle_redraw)

        # Calls automatically resize_callback and redraw_callback
        appuifw.app.body = canvas

        global img
        if not img:
            img = graphics.Image.new(canvas.size)

        e32.ao_yield()
        global board
        board = Board(TILE_SIZE)
        board.initialize()
        handle_screensaver()
        board.draw_board()

        # Define keyboard shortcuts
        canvas.bind(key_codes.EKeyLeftArrow, lambda: board.handle_movement(MOVE_LEFT))
        canvas.bind(key_codes.EKeyRightArrow, lambda: board.handle_movement(MOVE_RIGHT))
        canvas.bind(key_codes.EKeyUpArrow, lambda: board.handle_movement(MOVE_UP))
        canvas.bind(key_codes.EKeyDownArrow, lambda: board.handle_movement(MOVE_DOWN))
        canvas.bind(key_codes.EKeyEnter, lambda: self.query_newgame())
        canvas.bind(key_codes.EKeySelect, lambda: self.query_newgame())

        #############################################################
        # SENSOR init after everything else
        if SENSOR:
            # returns the dictionary of available sensors
            sensors = sensor.sensors()

            # "Support is device dependent, e.g. Nokia 5500 supports
            # OrientationEventFilter and Nokia N95 supports RotEventFilter"
            # Hox: Also N95 seems to support OrientationEventFilter

            # Does this device have Accelerator Sensor
            if sensors.has_key('AccSensor'):
                global SENSOR_ACC
                global sensor_acc
                SENSOR_ACC = True
                sensor_data = sensors['AccSensor']
                sensor_acc = \
                    sensor.Sensor(sensor_data['id'], sensor_data['category'])
                # Orientation filter: up, down, left, right, front, back
                #self.sensor_acc.set_event_filter(sensor.OrientationEventFilter())
                # My callback handler, only for Orientation events
                #sensor_acc.connect(self.handle_sensor_raw)
                sensor_acc.connect(self.sensor_stabilizer)

    def sensor_stabilizer(self, a_data):
        ''' Find new zero level '''
        global sensor_stab, s_zero1, s_zero2

        if sensor_stab:
            sensor_stab -= 1
            if a_data.has_key('data_1'):
                s_zero1 = s_zero1 + a_data['data_1'] - a_data['data_3']
                s_zero2 += a_data['data_2']
        else:
            s_zero1 = s_zero1 / 10
            s_zero2 = s_zero2 / 10
            sensor_acc.connect(self.handle_sensor_raw)
        # BUG: change of focus can reset stabilizer prematurately
        # As result zero levels can be way off scale

    def handle_sensor_raw(self, a_data):
        ''' My own handler for raw sensor events '''

        # Avoid unnecassary processing
        if not running == RUN_PLAY:
            return

        if my_lock == True:
            return

        # TODO: Too fast, how to slow down
        # TODO: Too slippery, user needs reaction time

        #handle_orientation:  {'a_data':
        # {'data_3': -287, 'data_2': -10, 'data_1': -31,
        # 'sensor_id': 271003684}}
        # Was called about 30-40 times a second in N82 debug test
        if a_data.has_key('data_1'):
            d1 = a_data['data_1']
            d2 = a_data['data_2']
            d3 = a_data['data_3']

            # data_1 is y-axel
            data_1 = (d1 - d3) - s_zero1
            # data_2 is x-axel
            data_2 = d2 - s_zero2

        # TODO: Create own event filter
        LIMIT = 50
        if abs(data_1) > abs(data_2):
            if data_1 < -LIMIT:
                board.handle_movement(MOVE_DOWN)
            elif data_1 > LIMIT:
                board.handle_movement(MOVE_UP)
            else:
                board.handle_movement(MOVE_NONE)
        else:
            if data_2 < -LIMIT:
                board.handle_movement(MOVE_RIGHT)
            elif data_2 > LIMIT:
                board.handle_movement(MOVE_LEFT)
            else:
                board.handle_movement(MOVE_NONE)

    def init_menu(self):
        ''' Defining S60 style Options menu '''
        appuifw.app.menu = [
            (u"New Maze", self.menu_start),
            (u"Level",
                ((u"Easy", lambda:self.menu_level(2)),
                (u"Medium", lambda:self.menu_level(1)),
                (u"Hard", lambda:self.menu_level(0)))),
            (u"Reset Sensor", self.menu_reset_sensor),
           (u"About", self.menu_about),
           (u"Exit", self.cb_quit)]

    def menu_start(self):
        ''' Callback for menu item NewGame '''
        board.initialize()
        board.draw_board()
        self.menu_reset_sensor()

    def menu_level(self, a_level):
        ''' Set difficulty level '''
        global TILE_SIZE
        if a_level == 0:
            TILE_SIZE = LEVEL_HARD
        elif a_level == 1:
            TILE_SIZE = LEVEL_MEDI
        else:
            TILE_SIZE = LEVEL_EASY
        board.__init__(TILE_SIZE)
        self.menu_start()

    def menu_reset_sensor(self):
        ''' Start sensor zero level reset '''
        global running, sensor_stab, s_zero1, s_zero2

        if not SENSOR_ACC:
            return
        old_run = running
        running = ~RUN_PLAY
        sensor_stab = 10
        s_zero1 = s_zero2 = 0
        sensor_acc.connect(self.sensor_stabilizer)
        running = old_run
        i = appuifw.InfoPopup()
        i.show(u"Ready")
        e32.ao_yield()

    def query_newgame(self):
        ''' Callback for dialog asking about a new game '''
        if appuifw.query(u'New maze?', 'query'):
            self.menu_start()

    def cb_quit(self):
        ''' Generic callback for exit, first do clean-up '''
        global running
        running = RUN_EXIT
        animation_timer.cancel()
        my_timer.cancel()
        screen_timer.cancel()

        # Free just in case, due previous mysterious crash
        canvas.bind(key_codes.EKeyLeftArrow, None)
        canvas.bind(key_codes.EKeyRightArrow, None)
        canvas.bind(key_codes.EKeyUpArrow, None)
        canvas.bind(key_codes.EKeyDownArrow, None)
        canvas.bind(key_codes.EKeyEnter, None)
        canvas.bind(key_codes.EKeySelect, None)

        # SENSOR cleanup
        if SENSOR_ACC:
            sensor_acc.disconnect()

        # Ready to exit
        app_lock.signal()

    def menu_about(self):
        ''' Callback for menu item About '''
        appuifw.note(NAME+u' v'+VERSION+'\n'+\
            'jouni.miettunen.googlepages.com\n(c) 2008 Jouni Miettunen')

#global timers
animation_timer = e32.Ao_timer()

m = Main()
app_lock = e32.Ao_lock()
app_lock.wait()
