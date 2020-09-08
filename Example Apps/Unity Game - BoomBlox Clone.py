'''
Unity - ChainShot, SameGame, MaciGame, TileFall etc.

Unity was originally invented in Japan 1985 as "Chain Shot!"
by Kuniaki Moribe. After that it has spread all over the world
with names such as SameGame, TumeGame, KomeGame, MameGame,
DebaGame, TileFall, Cabeem, MaciGame, GD-BMD etc.

The idea is to clear the whole playing area by removing tiles
in groups. The more tiles you remove at the same time, the more
points you get: (n_tiles - 2) ** 2

http://jouni.miettunen.googlepages.com
jouni dot miettunen at iki dot fi

Defects:
- Works only with portrait screens, not E61i landscape screen
- Verify that undo works correctly
- SIS must be installed on same disk drive as python

2.20 2008-10-31 Disable screensaver when at foreground
                Disable sensor when at background
                Startup board size Small (5x6)
                Cursor stays at selected non-empty tile when rotating
                Simple end detection (1 tile remaining)
                3 - Jump level, for testing purposes
                Fix: all top10 scores numbered 1-10
2.10 2008-10-20 New keyboard shortcuts:
                5 - New game
                * - Small board (star)
                0 - Normal board (zero)
                # - Large board (hash)
                7 - Take screenshot (was previously star)
                Settings: cursor wrap ON/OFF
                Cursor wraps around board edges
                Accelerator sensor support (Sensor API)
                Keyboard support to emulate Sensor API:
                2 - Drop tiles upwards, shift columns right
                4 - Drop tiles leftwards, shift columns up
                6 - Drop tiles rightwards, shift columns down
                8 - Drop tiles downwards, shift columns left
                Settings: down arrow ON/OFF
                Tested on: N77 (no sensors), N82 (sensors)
1.10 2008-10-15 Settings complete rewrite
                Settings: username
                Some code clean-up and speed-up
1.00 2008-10-05 Dedicated to croozeus.com (featured app #7)
                Settings: fade-out ON/OFF
                Separate Top-10 for each game size
0.60 2008-09-30 Top-10 code rewritten
                Removed cursor wrap
                Easy normal and hard, with shared score table
0.5  2008-09-28 Compare only points, no levels
                Tiles visually connected
                Top-10 high score table
                Cursor wraps around screen edges
                Fadeout selected tiles before removal
                Fix: undo one move
0.3  2008-09-18 Save screenshot with star (C:\Data\Images)
                Undo one move (with clear key)
                Fix: score counting (n_tiles - 2) ** 2
                Full screen board (10x10 -> 10x12)
                Simple high score recording
0.2  2008-09-02 Fix: point and level calculations
0.1  2008-09-01 First release
'''

VERSION = u'2.20'

import os
import sys
import e32
import appuifw
import graphics
import key_codes
import random

# Create own files in current installation directory
try:
    raise Exception
except Exception:
    fr = sys.exc_info()[2].tb_frame
    fpath = fr.f_code.co_filename

# Setup highscore
fdir, fname = os.path.split(fpath)
(a, b) = fname.split('.')
FILE_TOP = os.path.join(fdir, a + ".top")
FILE_SET = os.path.join(fdir, a + ".set")
TOP_ITEMS = 10
TOP_NAME = "Unity"

GAME_SMALL = 0
GAME_NORMAL = 1
GAME_LARGE = 2

# Global definitions
MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3

RUN_EXIT = 0
RUN_PLAY = 1
RUN_SOLVED = 2

RGB_BLACK = (0, 0, 0)
RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)
RGB_YELLOW = (255, 255, 0)
RGB_ORANGE = (255, 127, 0)
RGB_VIOLET = (153, 0, 153)
RGB_WHITE = (255, 255, 255)
my_colors = [RGB_BLACK, RGB_RED, RGB_GREEN, RGB_BLUE, RGB_ORANGE, RGB_VIOLET, RGB_YELLOW, RGB_WHITE]
g_colors = len(my_colors) - 1

# Global variables
running = RUN_EXIT
board = None
canvas = None
img = None
user_set = None

my_timer = e32.Ao_timer()
g_screensaver_off = False
timer_screen = e32.Ao_timer()

# SENSOR: if exception, it's not available in this device
SENSOR_ACC = False
try:
    import sensor
    from sensor import orientation
    SENSOR = True                # Sensor interface available
except ImportError:
    SENSOR = False               # Sensor interface not available

def handle_orientation(a_data):
    ''' My own handler for accelerator events '''
    if SENSOR_ACC == False:
        return
    # Handle OrientationEventFilter events
    if a_data == orientation.TOP:
        board.rotate(MOVE_DOWN)
    elif a_data == orientation.BOTTOM:
        board.rotate(MOVE_UP)
    elif a_data == orientation.LEFT:
        board.rotate(MOVE_RIGHT)
    elif a_data == orientation.RIGHT:
        board.rotate(MOVE_LEFT)

def handle_screensaver():
    ''' Reset inactivity timer '''
    global g_screensaver_off
    g_screensaver_off = True
    e32.reset_inactivity()
    timer_screen.after(4, handle_screensaver)

def cb_focus(fg):
    ''' System callback to tell when focus is lost/regained '''
    global g_screensaver_off
    if fg:
        # Got focus
        g_screensaver_off = True
        timer_screen.after(4, handle_screensaver)
        if SENSOR_ACC:
            sensor_acc.connect(handle_sensor_raw)
    else:
        # Lost focus
        g_screensaver_off = False
        timer_screen.cancel()
        if SENSOR_ACC:
            sensor_acc.disconnect()

def cb_handle_redraw(a_rect=(0, 0, 0, 0)):
    ''' Overwrite default screen redraw event handler '''
    if not img:
        return
    canvas.blit(img)

#############################################################
class MySettings(object):
    def __init__(self, a_file):
        ''' Init by reading data '''
        self.reset()
        f = None
        try:
            f = open(a_file, "r")
            s = f.readline()
            if s:
                self._name = s.strip('\n')
            else:
                raise Exception
            s = f.readline()
            if s:
                a, b, c = s.split('\t')
                self._fadeout = int(a)
                self._down = int(b)
                self._wrap = int(c)
            else:
                raise Exception
        except:
            self.reset()
        if f:
            f.close()

    def reset(self):
        ''' Set default data '''
        self._name = TOP_NAME
        self._fadeout = 1
        self._down = 1
        self._wrap = 1

    def name(self, a_value = None):
        ''' Handle name setting '''
        if a_value:
            self._name = a_value
        return self._name

    def fadeout(self, a_value = -1):
        ''' Handle fadeout setting '''
        if a_value != -1:
            self._fadeout = a_value
        return self._fadeout

    def down(self, a_value = -1):
        ''' Handle Show Down setting '''
        if a_value != -1:
            self._down = a_value
        return self._down

    def wrap(self, a_value = -1):
        ''' Handle cursor wrap setting '''
        if a_value != -1:
            self._wrap = a_value
        return self._wrap

    def save(self, a_file):
        ''' Save current data into file '''
        f = open(a_file, "w")
        s = str("%s\n%d\t%d\t%d" % (self._name, self._fadeout, self._down, self._wrap))
        f.write(s)
        f.close()

#############################################################
class HighScore(object):
    def __init__(self, a_file, a_items, a_games):
        ''' Init by reading old high scores '''
        self.items = a_items
        self.games = a_games
        self.reset()
        try:
            f = open(a_file, "r")
            for i in range(a_games * self.items):
                s = f.readline()
                if s:
                    name, points, level = s.split('\t')
                    self.hof[i] = [name, int(points), int(level)]
                else:
                    raise Exception
            f.close()
        except:
            self.reset()

    def top(self, i, a_game):
        ''' Return top-x item name, points, level '''
        i = a_game * self.items + i - 1
        return (self.hof[i][0], self.hof[i][1], self.hof[i][2])

    def check_score(self, a_points, a_level, a_game):
        ''' Check if user got on top-10 '''
        a = a_game * self.items
        b = a + self.items
        for i in range(a, b):
            if a_points >= self.hof[i][1]:
                s = 'Congratulations Top-%d! You got %d (%d) points. What is your name:' %\
                    (i-a+1, a_points, a_level)
                name = user_set.name()
                s = appuifw.query(unicode(s), "text", unicode(name))
                if s:
                    user_set.name(s)
                break

        if i-a < self.items-1:
            for j in range(b-1, i, -1):
                self.hof[j] = self.hof[j-1][:]
            self.hof[i] = [user_set.name(), a_points, a_level]

    def reset(self):
        ''' Remove old hiscore '''
        self.hof = [[TOP_NAME, 1, 1] for i in range(self.items * self.games)]

    def save_score(self, a_file):
        ''' Save current high score into file '''
        f = open(a_file, "w")
        for i in range(self.games * self.items):
            s = str("%s\t%d\t%d\n" % (self.hof[i][0], self.hof[i][1], self.hof[i][2]))
            f.write(s)
        f.close()

#############################################################
class Board(object):
    ''' Game play related operations '''
    def __init__(self):
        self.board = []
        self.cursor_y = self.cursor_x = 0
        self.width, self.height = canvas.size
        self.tile_width = self.tile_height = 1
        self.level = 0
        self.points = -1
        self.game = GAME_NORMAL
        self.down = MOVE_DOWN
        self.left = (self.down + 1) % 4
        self.undo_board = []
        self.undo_points = 0
        self.init_arrow(self.down)

    def initialize(self, a_game=-1):
        ''' Setup new game '''
        top10.check_score(self.points, self.level, self.game)

        if a_game == GAME_SMALL:
            self.game = a_game
            self.dim_x = 5
            self.dim_y = 5 + 1
        elif a_game == GAME_NORMAL:
            self.game = a_game
            self.dim_x = 10
            self.dim_y = 10 + 2
        elif a_game == GAME_LARGE:
            self.game = a_game
            self.dim_x = 20
            self.dim_y = 20 + 4

        a = self.width / self.dim_x
        b = self.height / self.dim_y
        self.tile_width = self.tile_height = min(a, b)

        self.tile_total = self.dim_x * self.dim_y
        self.board = []
        self.board = range(0, self.tile_total)
        self.level = 1
        self.points = 0
        self.undo_board = []
        self.undo_points = 0
        self.undo_count = 0
        self.new_level(self.level)

        global running
        running = RUN_PLAY

    def new_level(self, a_level):
        ''' Initialize next game level '''
        self.cursor_y = self.cursor_x = 0

        # Slow down difficulty progress: do each count about 4 times
        a_list = range(1, min(int(2 + ((a_level-1) / 4)), len(my_colors))+1)
        self.tile_count = 0
        for i in range(self.tile_total):
            self.board[i] = random.choice(a_list)
        self.undo_board = self.board[:]
        self.undo_count = 0
        self.undo_points = self.points

    def jump_level(self, a_count):
        ''' For testing purposes, jump level '''
        if self.level == 1:
            self.level += 1
        self.level += a_count
        self.new_level(self.level)
        self.draw_board()

    def undo(self):
        ''' One level undo '''
        self.board = self.undo_board[:]
        self.points = self.undo_points
        self.tile_count = self.undo_count
        self.rotate(self.down)

    def draw_board(self):
        ''' Redraw and show the whole game board '''
        self.draw_alltiles()
        self.draw_score()
        cb_handle_redraw()

    def draw_alltiles(self):
        ''' Create complete game board on off-screen '''
        img.clear(RGB_BLACK)
        i = 0
        for y in range(self.dim_y):
            for x in range(self.dim_x):
                self.draw_onetile(x, y, self.board[i])
                i += 1
        self.draw_cursor(self.cursor_x, self.cursor_y, self.board[self.cursor_x + self.cursor_y * self.dim_x])

    def draw_onetile(self, x, y, a_value, a_color=(-1,-1,-1)):
        ''' Draw one tile on off-screen image '''
        top_x, top_y = self.screen_coord(x, y)
        bot_x = top_x + self.tile_width
        bot_y = top_y + self.tile_height

        # TODO: make more colors
        a_value = min(a_value, g_colors)

        if a_color == (-1,-1,-1):
            c = my_colors[a_value]
        else:
            c = a_color
        (r, g, b) = c
        #c2 = (r/2, g/2, b/2)
        c2 = (3*r/4, 3*g/4, 3*b/4)

        if self.check_tile(x, y-1) == a_value:
            top_y -= 1
        if self.check_tile(x, y+1) == a_value:
            bot_y += 1
        if self.check_tile(x-1, y) == a_value:
             top_x -= 1
        if self.check_tile(x+1, y) == a_value:
             bot_x += 1

        img.rectangle((top_x+1, top_y+1, bot_x-2, bot_y-2), \
            width=2, outline=c, fill=c2)

    def init_arrow(self, a_dir):
        ''' Initialize down arrow '''
        mm = 30
        aa = 10
        bb = 35 # magic 240x320, calc relative to last tile
        if a_dir == MOVE_DOWN:
            xx = self.width - mm - aa
            yy = aa
        elif a_dir == MOVE_LEFT:
            xx = self.width - mm - aa
            yy = self.height - bb - mm - aa
        elif a_dir == MOVE_UP:
            xx = aa
            yy = self.height - bb - mm - aa
        else: #default to if a_dir == MOVE_RIGHT:
            xx = aa
            yy = aa

        a1 = (xx, yy)
        b1 = (xx, yy+mm/2)
        c1 = (xx, yy+mm)
        a2 = (xx+mm/2, yy)
        b2 = (xx+mm/2, yy+mm/2)
        c2 = (xx+mm/2, yy+mm)
        a3 = (xx+mm, yy)
        b3 = (xx+mm, yy+mm/2)
        c3 = (xx+mm, yy+mm)

        self.poly = []
        self.poly = [[(0,0)] for i in range(4)]
        poly = []
        poly += c1 + b2 + c3 + a2 + c1
        self.poly[MOVE_UP] = poly[:]
        poly = []
        poly += a1 + b3 + c1 + b2 + a1
        self.poly[MOVE_RIGHT] = poly[:]
        poly = []
        poly += a1 + b2 + a3 + c2 + a1
        self.poly[MOVE_DOWN] = poly[:]
        poly = []
        poly += b1 + a3 + b2 + c3 + b1
        self.poly[MOVE_LEFT] = poly[:]

    def draw_cursor(self, x, y, a_value):
        ''' Draw cursor on off-screen image '''
        top_x, top_y = self.screen_coord(x, y)
        bot_x = top_x + self.tile_width
        bot_y = top_y + self.tile_height

        a_value = min(a_value, g_colors)
        if self.check_tile(x, y-1) == a_value:
            top_y -= 1
        if self.check_tile(x, y+1) == a_value:
            bot_y += 1
        if self.check_tile(x-1, y) == a_value:
             top_x -= 1
        if self.check_tile(x+1, y) == a_value:
             bot_x += 1

        img.rectangle((top_x+2, top_y+2, bot_x-2, bot_y-2), \
            width=3, outline=RGB_WHITE)

        if user_set.down():
            # Show "down" direction in "top right" corner
            # This is good place, draw over cursor
            img.line(self.poly[self.down], width=3, outline=RGB_WHITE)
            img.line(self.poly[self.down], width=1, outline=RGB_BLACK)

    def check_tile(self, x, y):
        ''' Check location in matrix '''
        if x<0 or y<0 or (x>self.dim_x-1) or (y>self.dim_y-1):
            return -1
        else:
            return self.board[x+y*self.dim_x]

    def move_cursor(self, a_dir):
        ''' make move in matrix, not on-screen '''
        result = False
        if user_set.wrap():
            result = True
            if a_dir == MOVE_UP:
                # Cursor goes up
                self.cursor_y = (self.cursor_y - 1) % self.dim_y
            elif a_dir == MOVE_DOWN:
                # Cursor goes down
                self.cursor_y = (self.cursor_y + 1) % self.dim_y
            elif a_dir == MOVE_LEFT:
                # Cursor goes left
                self.cursor_x = (self.cursor_x - 1) % self.dim_x
            elif a_dir == MOVE_RIGHT:
                # Cursor goes right
                self.cursor_x = (self.cursor_x + 1) % self.dim_x
        else:
            if a_dir == MOVE_UP:
                # Cursor goes up
                if self.cursor_y > 0:
                    self.cursor_y -= 1
                    result = True
            elif a_dir == MOVE_DOWN:
                # Cursor goes down
                if self.cursor_y < self.dim_y-1:
                    self.cursor_y += 1
                    result = True
            elif a_dir == MOVE_LEFT:
                # Cursor goes left
                if self.cursor_x > 0:
                    self.cursor_x -= 1
                    result = True
            elif a_dir == MOVE_RIGHT:
                # Cursor goes right
                if self.cursor_x < self.dim_x-1:
                    self.cursor_x += 1
                    result = True
        return result

    def make_move(self, a_dir):
        ''' Handle possible next move '''
        if running == RUN_SOLVED or running == RUN_EXIT:
            return

        old_x = self.cursor_x
        old_y = self.cursor_y

        if self.move_cursor(a_dir):
            # Update new, clean old
            old_i = old_x + old_y * self.dim_x
            self.draw_onetile(old_x, old_y, self.board[old_i])
            self.draw_cursor(self.cursor_x, self.cursor_y, self.board[self.cursor_x + self.cursor_y * self.dim_x])
            cb_handle_redraw()

    def check_click(self):
        ''' User made a selection '''
        x = self.cursor_x
        y = self.cursor_y
        i = x + y * self.dim_x
        # zero means empty, non-zero means something
        if self.board[i]:
            my_list = []
            my_list.append(i)
            color = self.board[i]
            self.temp_board = self.board[:]
            self.board[i] = 0
            count = 1 + self.count_group(x, y, color, my_list)
            if count > 1:
                self.undo_board = self.temp_board[:]
                if user_set.fadeout():
                    self.fade_tiles(my_list, color)
                self.remove_tiles(my_list)
                self.update_score((count-2)*(count-2))
                #TODO: optimize to draw only changed columns/rows + neighbours
                self.draw_board()
#             elif self.tile_count == self.tile_total-1:
#                 s = appuifw.query(u"Do You want to remove last tile (costs -1000 points)", "query")
#                 if s:
#                     self.update_score(-1000)
#                     self.remove_tiles(my_list)
#                 else:
#                     self.board[i] = color
            else:
                self.board[i] = color

            # Game finished, show it somehow
            result = self.level_solved()
            if result == 1:
                self.level += 1
                self.update_score(1000)
                self.new_level(self.level)
                self.draw_board()
            elif result == -1:
                m.menu_start()

    def update_score(self, a_points):
        ''' Calculate new points '''
        self.points += a_points

    def reset_score(self):
        ''' Remove old hiscore '''
        top10.reset()
        self.draw_board()

    def draw_score(self):
        ''' Show score on-screen '''
        if not img:
            return

        x, y = self.screen_coord(0, self.dim_y)
        y += 18
        s = unicode(str("Score: %d(%d)" % (self.points, self.level)))
        img.text((x+1, y+1), s, RGB_RED, 'dense')
        img.text((x-1, y-1), s, RGB_ORANGE, 'dense')
        img.text((x, y), s, RGB_WHITE, 'dense')
        x = self.width/2
        name, best_points, best_level = top10.top(1, self.game)
        s = unicode(str("Best: %d(%d)" % (best_points, best_level)))
        img.text((x+1, y+1), s, RGB_BLUE, 'dense')
        img.text((x-1, y-1), s, RGB_GREEN, 'dense')
        img.text((x, y), s, RGB_WHITE, 'dense')

    def count_group(self, x, y, a_color, a_list):
        ''' How many connected tiles '''
        count = 0
        # Can you go up
        if y and self.board[x+(y-1)*self.dim_x] == a_color:
            count += 1
            a_list.append(x+(y-1)*self.dim_x)
            self.board[x+(y-1)*self.dim_x] = 0
            count += self.count_group(x, y-1, a_color, a_list)
        # Can you go left
        if x and self.board[(x-1)+y*self.dim_x] == a_color:
            count += 1
            a_list.append((x-1)+y*self.dim_x)
            self.board[(x-1)+y*self.dim_x] = 0
            count += self.count_group(x-1, y, a_color, a_list)
        # Can you go down
        if y<self.dim_y-1 and self.board[x+(y+1)*self.dim_x] == a_color:
            count += 1
            a_list.append(x+(y+1)*self.dim_x)
            self.board[x+(y+1)*self.dim_x] = 0
            count += self.count_group(x, y+1, a_color, a_list)
        # Can you go right
        if x<self.dim_x-1 and self.board[(x+1)+y*self.dim_x] == a_color:
            count += 1
            a_list.append((x+1)+y*self.dim_x)
            self.board[(x+1)+y*self.dim_x] = 0
            count += self.count_group(x+1, y, a_color, a_list)
        return count

    def fade_tiles(self, a_list, a_color):
        ''' Fade selected tiles to black '''
        r, g, b = my_colors[a_color]
        step = 2
        dr = r/step
        dg = g/step
        db = b/step
        len_list = len(a_list)
        my_timer.cancel()
        for count in range(step):
            r = r-dr
            g = g-dg
            b = b-db
            for i in range(len_list):
                #Reverse of i = x + y * self.dim_x
                y = a_list[i] / self.dim_x
                x = a_list[i] % self.dim_x
                self.draw_onetile(x, y, 0, (r, g, b))
            self.draw_cursor(self.cursor_x, self.cursor_y, self.board[self.cursor_x + self.cursor_y * self.dim_x])
            cb_handle_redraw()
            my_timer.after(0.05)

    def rotate(self, a_new):
        ''' Manual screen rotation '''
        self.down = a_new
        self.left = (a_new + 1) % 4
        i = self.cursor_x + self.cursor_y * self.dim_x
        value = self.board[i]
        # BUG: cursor on empty doesn't drop/shift
        # FIX: temporarily only follow selected tile :(
        if value:
            self.board[i] = value + 0xf0
        self.drop_tiles(self.down)
        self.shift_tiles(self.left)
        if value:
            i = self.board.index(value + 0xf0)
            self.cursor_y = i / self.dim_x
            self.cursor_x = i % self.dim_x
            self.board[i] = value
        self.init_arrow(self.down)
        self.draw_board()

    def remove_tiles(self, a_list):
        ''' Remove selected tiles '''
        self.undo_points = self.points
        self.undo_count = self.tile_count
        for i in a_list:
            self.board[i] = 0
        self.tile_count += len(a_list)
        self.drop_tiles(self.down)
        self.shift_tiles(self.left)

    def drop_tiles(self, a_dir):
        ''' Collapse tiles together '''
        if a_dir == MOVE_DOWN:
            for x in range(self.dim_x):
                i = i_zero = x + (self.dim_y-1) * self.dim_x
                limit = x-1
                while i > limit:
                    if self.board[i]:
                        if i != i_zero:
                            self.board[i_zero] = self.board[i]
                        i_zero -= self.dim_x
                        i -= self.dim_x
                    else:
                        i -= self.dim_x
                while i_zero > limit:
                    self.board[i_zero] = 0
                    i_zero -= self.dim_x

        elif a_dir == MOVE_UP:
            for x in range(self.dim_x):
                i = i_zero = x
                limit = x + self.dim_y * self.dim_x
                while i < limit:
                    if self.board[i]:
                        if i != i_zero:
                            self.board[i_zero] = self.board[i]
                        i += self.dim_x
                        i_zero += self.dim_x
                    else:
                        i += self.dim_x
                while i_zero < limit:
                    self.board[i_zero] = 0
                    i_zero += self.dim_x

        elif a_dir == MOVE_LEFT:
            for y in range(self.dim_y):
                i = i_zero = y * self.dim_x
                limit = i + self.dim_x
                while i < limit:
                    if self.board[i]:
                        if i != i_zero:
                            self.board[i_zero] = self.board[i]
                        i_zero += 1
                        i += 1
                    else:
                        i += 1
                while i_zero < limit:
                    self.board[i_zero] = 0
                    i_zero += 1

        elif a_dir == MOVE_RIGHT:
            for y in range(self.dim_y):
                i = i_zero = (y+1) * self.dim_x - 1
                limit = i - self.dim_x
                while i > limit:
                    if self.board[i]:
                        if i != i_zero:
                            self.board[i_zero] = self.board[i]
                        i_zero -= 1
                        i -= 1
                    else:
                        i -= 1
                while i_zero > limit:
                    self.board[i_zero] = 0
                    i_zero -= 1

    def shift_tiles(self, a_dir):
        ''' Shift columns together '''
        if a_dir == MOVE_LEFT:
            i = i_zero = (self.dim_y-1) * self.dim_x
            limit = self.dim_y * self.dim_x - 1
            while i <= limit:
                if self.board[i]:
                    if i != i_zero:
                        a = i_zero
                        b = i
                        for j in range(self.dim_y):
                            self.board[a] = self.board[b]
                            a -= self.dim_x
                            b -= self.dim_x
                    i += 1
                    i_zero += 1
                else:
                    i += 1
            while i_zero <= limit:
                a = i_zero
                for j in range(self.dim_y):
                    self.board[a] = 0
                    a -= self.dim_x
                i_zero += 1

        if a_dir == MOVE_UP:
            i = i_zero = 0
            limit = (self.dim_y-1) * self.dim_x
            while i <= limit:
                if self.board[i]:
                    if i != i_zero:
                        a = i_zero
                        b = i
                        for j in range(self.dim_x):
                            self.board[a] = self.board[b]
                            a += 1
                            b += 1
                    i += self.dim_x
                    i_zero += self.dim_x
                else:
                    i += self.dim_x
            while i_zero <= limit:
                a = i_zero
                for j in range(self.dim_x):
                    self.board[a] = 0
                    a += 1
                i_zero += self.dim_x

        if a_dir == MOVE_DOWN:
            i = i_zero = self.dim_y * self.dim_x - 1
            limit = self.dim_x-1
            while i >= limit:
                if self.board[i]:
                    if i != i_zero:
                        a = i_zero
                        b = i
                        for j in range(self.dim_x):
                            self.board[a] = self.board[b]
                            a -= 1
                            b -= 1
                    i -= self.dim_x
                    i_zero -= self.dim_x
                else:
                    i -= self.dim_x
            while i_zero >= limit:
                a = i_zero
                for j in range(self.dim_x):
                    self.board[a] = 0
                    a -= 1
                i_zero -= self.dim_x

        elif a_dir == MOVE_RIGHT:
            i = i_zero = self.dim_x-1
            limit = 0
            while i >= limit:
                if self.board[i]:
                    if i != i_zero:
                        a = i_zero
                        b = i
                        for j in range(self.dim_y):
                            self.board[a] = self.board[b]
                            a += self.dim_x
                            b += self.dim_x
                    i -= 1
                    i_zero -= 1
                else:
                    i -= 1
            while i_zero >= limit:
                a = i_zero
                for j in range(self.dim_y):
                    self.board[a] = 0
                    a += self.dim_x
                i_zero -= 1

    def screen_coord(self, x, y):
        ''' Get screen coordinates from table coordinates '''
        return x*self.tile_width, y*self.tile_height

    def level_solved(self):
        ''' Is game finished or not '''
        if self.tile_count == self.tile_total:
            return 1
        elif self.tile_count == self.tile_total - 1:
            return -1
        else:
            return 0

#############################################################
class Main(object):
    ''' Application related things '''

    def __init__(self):
        self.options = [
            [
                (u"New Game", self.menu_start),
                (u"Game size:",
                    ((u"Small (5x6)", lambda:self.menu_start(GAME_SMALL)),
                    (u"Normal (10x12)", lambda:self.menu_start(GAME_NORMAL)),
                    (u"Large (20x24)", lambda:self.menu_start(GAME_LARGE)))),
                (u"Top-10", self.show_top10),
                (u"Settings", self.show_settings),
                (u"About", self.menu_about),
                (u"Exit", self.cb_quit)
            ],
            [
                (u"Reset", self.top10_reset),
                (u"Back", self.cb_return_main)
            ],
            [
                (u"Change", self.handle_settings),
                (u"Reset", self.settings_reset),
                (u"Back", self.cb_return_main)
            ]
            ]

        self.lb = appuifw.Listbox([u""], lambda:None)

        appuifw.app.screen = 'full'
        appuifw.app.orientation = 'portrait'
        appuifw.app.title = u'Unity'
        appuifw.app.exit_key_handler = self.cb_quit
        appuifw.app.focus = cb_focus
        appuifw.app.menu = self.options[0]

        global canvas
        canvas = appuifw.Canvas(redraw_callback = cb_handle_redraw)
        appuifw.app.body = canvas

        # Board uses top10
        global top10
        top10 = HighScore(FILE_TOP, TOP_ITEMS, 3)

        # Board uses user_set.down
        global user_set
        user_set = MySettings(FILE_SET)

        global board
        board = Board()
        board.initialize(GAME_SMALL)

        global img
        img = graphics.Image.new(canvas.size)

        board.draw_board()

        # Define keyboard shortcuts
        canvas.bind(key_codes.EKeyLeftArrow, lambda: board.make_move(MOVE_LEFT))
        canvas.bind(key_codes.EKeyRightArrow, lambda: board.make_move(MOVE_RIGHT))
        canvas.bind(key_codes.EKeyUpArrow, lambda: board.make_move(MOVE_UP))
        canvas.bind(key_codes.EKeyDownArrow, lambda: board.make_move(MOVE_DOWN))
        canvas.bind(key_codes.EKeyEnter, board.check_click)
        canvas.bind(key_codes.EKeySelect, board.check_click)
        canvas.bind(key_codes.EKeyBackspace, board.undo)
        canvas.bind(key_codes.EKey5, self.menu_start)
        canvas.bind(key_codes.EKey2, lambda: board.rotate(MOVE_UP))
        canvas.bind(key_codes.EKey4, lambda: board.rotate(MOVE_LEFT))
        canvas.bind(key_codes.EKey6, lambda: board.rotate(MOVE_RIGHT))
        canvas.bind(key_codes.EKey8, lambda: board.rotate(MOVE_DOWN))
        canvas.bind(key_codes.EKey5, self.menu_start)
        canvas.bind(key_codes.EKeyStar, lambda:self.menu_start(GAME_SMALL))
        canvas.bind(key_codes.EKey0, lambda:self.menu_start(GAME_NORMAL))
        canvas.bind(key_codes.EKeyHash, lambda:self.menu_start(GAME_LARGE))
        canvas.bind(key_codes.EKey3, lambda:board.jump_level(3))

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
                SENSOR_ACC = True
                sensor_data = sensors['AccSensor']
                self.sensor_acc = sensor.Sensor(sensor_data['id'], sensor_data['category'])
                # Set default filter
                self.sensor_acc.set_event_filter(sensor.OrientationEventFilter())
                # Set my own event callback handler
                self.sensor_acc.connect(handle_orientation)

        # N82 Settings UI has minimum value 5 seconds
        # Set timeour in 4 seconds
        global g_screensaver_off
        g_screensaver_off = True
        timer_screen.after(4, handle_screensaver)

    def menu_start(self, a_game=-1):
        ''' Callback for menu item NewGame '''
        board.initialize(a_game)
        board.draw_board()

    def show_top10(self):
        ''' Change view '''
        appuifw.app.exit_key_handler = self.cb_return_main
        appuifw.app.menu = self.options[1]
        appuifw.app.screen = 'normal'
	appuifw.app.set_tabs([u"Small", u"Normal", u"Large"], self.handle_tabs)
        self.lb = appuifw.Listbox([u""], self.handle_tabs)
        appuifw.app.body = self.lb
        appuifw.app.activate_tab(board.game)
        self.handle_tabs(board.game)

    def handle_tabs(self, index):
        ''' Show high score '''
        a = index * top10.items + 1
        b = a + top10.items
        hof = []
        for i in range(a, b):
            name, points, level = top10.top(i-a+1, index)
            s = "%d: %5d(%d) %s" % (i-a+1, points, level, name)
            hof.append(unicode(s))
        self.lb.set_list(hof)

    def show_settings(self):
        ''' Show Settings view '''
        a = user_set.name()
        b = self.onoff(user_set.fadeout())
        c = self.onoff(user_set.down())
        d = self.onoff(user_set.wrap())
        lb_list = self.lb_settings(a, b, c, d)
        self.lb = appuifw.Listbox(lb_list, self.handle_settings)

        appuifw.app.exit_key_handler = self.cb_return_main
        appuifw.app.menu = self.options[2]
        appuifw.app.screen = 'normal'
        appuifw.app.body = self.lb

    def lb_settings(self, a, b, c, d):
        return [
            (u"TOP-10 Name", unicode(a)),
            (u"Animation", unicode(b)),
            (u"Down Arrow", unicode(c)),
            (u"Cursor Wrap", unicode(d))
          ]

    def onoff(self, a):
        ''' Number to text: 0 - Off, 1 - On '''
        if a:
            return "On"
        else:
            return "Off"

    def handle_settings(self):
        ''' Callback for Settings listbox '''
        b = user_set.fadeout()
        c = user_set.down()
        d = user_set.wrap()
        s1 = user_set.name()
        s2 = s3 = s4 = u""

        index = self.lb.current()
        if index == 0:
            t = "What is your name:"
            s1 = appuifw.query(unicode(t), "text", unicode(s1))
        if index == 1:
            b = (b + 1) % 2
            user_set.fadeout(b)
        elif index == 2:
            c = (c + 1) % 2
            user_set.down(c)
        elif index == 3:
            d = (d + 1) % 2
            user_set.wrap(d)

        if s1:
            user_set.name(s1)
        else:
            s1 = user_set.name()
        s2 = self.onoff(b)
        s3 = self.onoff(c)
        s4 = self.onoff(d)

        lb_list = self.lb_settings(s1, s2, s3, s4)
        self.lb.set_list(lb_list, index)
        appuifw.app.body = self.lb

    def settings_reset(self):
        ''' Reset settings '''
        user_set.reset()
        self.show_settings()

    def cb_return_main(self):
        ''' Return from Top-10 Listbox '''
        appuifw.app.exit_key_handler = self.cb_quit
        appuifw.app.screen = 'full'
        appuifw.app.body = canvas
        appuifw.app.menu = self.options[0]
	appuifw.app.set_tabs([], lambda:Null)
	# Full screen redraw because down arrow on/off
	board.draw_board()

    def top10_reset(self):
        ''' Reset high score '''
        top10.reset()
        self.show_top10()

    def menu_reset_score(self):
        ''' Reset high score '''
        board.reset_score()

    def query_newgame(self):
        ''' Callback for dialog asking top start a new game '''
        if appuifw.query(u'New game?', 'query'):
            board.initialize()
            board.draw_board()

    def cb_quit(self):
        ''' Generic callback for exit, first do clean-up '''
        global running
        running = RUN_EXIT
        my_timer.cancel()
        timer_screen.cancel()

        # SENSOR cleanup
        if SENSOR_ACC:
            self.sensor_acc.disconnect()

        global board
        global top10

        top10.check_score(board.points, board.level, board.game)
        top10.save_score(FILE_TOP)
        user_set.save(FILE_SET)

        # Help system with cleanup, to avoid CONE 8 crash:
        del board
        del top10
        self.lb = []

        # Free just in case, due previous mysterious crash
        canvas.bind(key_codes.EKeyLeftArrow, None)
        canvas.bind(key_codes.EKeyRightArrow, None)
        canvas.bind(key_codes.EKeyUpArrow, None)
        canvas.bind(key_codes.EKeyDownArrow, None)
        canvas.bind(key_codes.EKeyEnter, None)
        canvas.bind(key_codes.EKeySelect, None)
        canvas.bind(key_codes.EKeyStar, None)
        canvas.bind(key_codes.EKeyBackspace, None)
        canvas.bind(key_codes.EKey0, None)
        canvas.bind(key_codes.EKey1, None)
        canvas.bind(key_codes.EKey2, None)
        canvas.bind(key_codes.EKey3, None)
        canvas.bind(key_codes.EKey4, None)
        canvas.bind(key_codes.EKey5, None)
        canvas.bind(key_codes.EKey6, None)
        canvas.bind(key_codes.EKey7, None)
        canvas.bind(key_codes.EKey8, None)
        canvas.bind(key_codes.EKey9, None)

	appuifw.app.set_tabs([], lambda:Null)
        app_lock.signal()

    def menu_about(self):
        ''' Callback for menu item About '''
        appuifw.note(u'Unity v'+VERSION+'\n'+\
            'jouni.miettunen.googlepages.com\n(c) 2008 Jouni Miettunen')

#############################################################

m = Main()

##### SNAPSHOT SNAPSHOT SNAPSHOT SNAPSHOT SNAPSHOT SNAPSHOT
pic_index = 0
def take_snapshot():
    ''' Hardcoded screen snapshot '''
    global pic_index
    a = graphics.screenshot()
    filename = "c:\\Data\\Images\\unity%02d.png" % pic_index
    a.save(filename)
    pic_index = (pic_index + 1) % 100

canvas.bind(key_codes.EKey7, take_snapshot)
##### SNAPSHOT SNAPSHOT SNAPSHOT SNAPSHOT SNAPSHOT SNAPSHOT

app_lock = e32.Ao_lock()
app_lock.wait()
