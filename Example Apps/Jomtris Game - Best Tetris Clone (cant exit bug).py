VERSION = u'1.60'
import os
import sys
import e32
import appuifw
import graphics
import random
import time
import key_codes
AABG = 'jomtris_160.jpg'
AAME = 'jomtris'
if e32.in_emulator():
    try:
        raise Exception
    except Exception:
        fr = sys.exc_info()[2].tb_frame
        fpath = fr.f_code.co_filename
    (fdir, fname,) = os.path.split(fpath)
    (a, b,) = fname.split('.')
    AAPATH = fdir
else:
    AAPATH = os.getcwd()
try:
    s = os.path.join(AAPATH, AABG)
    pic = graphics.Image.open(s)
except:
    pic = None
AATOP = os.path.join(AAPATH, (AAME + '.top'))
AASET = os.path.join(AAPATH, (AAME + '.set'))
AITEMS = 10
ANAME = 'Jomtris'
AAABLACK = (0,
 0,
 0)
AAAYELLOW = (255,
 255,
 0)
AAAGREEN = (0,
 255,
 0)
AAAORANGE = (240,
 160,
 0)
AAAWHITE = (255,
 255,
 255)
AAABG = (0,
 0,
 85)
AIMARA = 0
AISPRI = 1
AICHAL = 2
AIlEXIT = 0
AIlIDLE = 1
AIlPLAY = 2
AIlHARD = 4
AIlWAIT = 8
AIlPAUS = 16
AIlDONE = 32
oo0000 = AIlIDLE
fc_run = AIlEXIT
w_run = []
_oO00 = None
nm = None
mn = None
user_set = None
mnm = e32.Ao_timer()
nmn = e32.Ao_timer()
g_ignore = False
g_oo0000 = 0
T_LEFT = 1
T_RIGHT = 2
T_TOP = 1

def ooo():
    if (oo0000 != AIlPLAY):
        return 
    e32.reset_inactivity()
    nmn.after(4, ooo)



def o0o(a_wait):
    global oo0000
    if a_wait:
        mnm.cancel()
        nmn.cancel()
        w_run.append(oo0000)
        oo0000 = AIlWAIT
    else:
        nmn.cancel()
        ooo()
        oo0000 = w_run.pop()
        if (oo0000 == AIlPLAY):
            mnm.cancel()
            mnm.after(_oO00._oO00oo, lambda :_oO00.o0o0o(0, 1)
)



def o0O(fg):
    global oo0000
    global fc_run
    if fg:
        nmn.cancel()
        ooo()
        oo0000 = fc_run
        fc_run = AIlEXIT
        if (oo0000 == AIlPLAY):
            mnm.cancel()
            mnm.after(_oO00._oO00oo, lambda :_oO00.o0o0o(0, 1)
)
    else:
        mnm.cancel()
        nmn.cancel()
        fc_run = oo0000
        oo0000 = AIlWAIT



def o0Oo(dummy = (0,
 0,
 0,
 0)):
    if mn:
        nm.blit(mn)



def o0oo(dummy = (0,
 0,
 0,
 0)):
    global pic
    global mn
    global g_oo0000
    if g_ignore:
        return 
    if (not nm):
        return 
    if (not _oO00):
        return 
    a = nm.size[0]
    if (g_oo0000 == a):
        return 
    else:
        g_oo0000 = a
    o0o(True)
    _oO00.g_oo000(nm.size[0], nm.size[1])
    _oO00.g_oo00()
    mn = graphics.Image.resize(mn, nm.size)
    pic = graphics.Image.resize(pic, mn.size)
    _oO00.g_oo0()
    o0Oo()
    o0o(False)


class CMS(object):
    __module__ = __name__

    def __init__(self, a_file):
        self.reset()
        f = None
        try:
            f = open(a_file, 'r')
            s = f.readline()
            if s:
                self._o = s.strip('\n')
            else:
                raise Exception
            s = f.readline()
            if s:
                (a, b,) = s.split('\t')
                self._oo0 = int(a)
                self._oo = int(b)
            else:
                raise Exception
        except:
            self.reset()
        if f:
            f.close()



    def reset(self):
        self._o = ANAME
        self._oo0 = -1
        self._oo = 1



    def name(self, _o0 = None):
        if _o0:
            self._o = _o0
        return self._o



    def rotate(self, _o0 = 0):
        if _o0:
            self._oo0 = _o0
        return self._oo0



    def level(self, _o0 = 0):
        if _o0:
            self._oo = _o0
        return self._oo



    def save(self, a_file):
        f = open(a_file, 'w')
        s = str(('%s\n%d\t%d' % (self._o,
         self._oo0,
         self._oo)))
        f.write(s)
        f.close()



class CHS(object):
    __module__ = __name__

    def __init__(self, a_file, a_items, a_games):
        self.items = a_items
        self.games = a_games
        self.reset()
        try:
            f = open(a_file, 'r')
            for i in range((a_games * self.items)):
                s = f.readline()
                if s:
                    (name, points, level,) = s.split('\t')
                    self.hof[i] = [name,
                     int(points),
                     int(level)]
                else:
                    raise Exception

            f.close()
        except:
            self.reset()



    def top(self, i, a_game):
        i = (((a_game * self.items) + i) - 1)
        return (self.hof[i][0],
         self.hof[i][1],
         self.hof[i][2])



    def check_score(self, a_points, a_oo, a_game):
        global oo0000
        if (oo0000 != AIlDONE):
            return 
        oo0000 = AIlIDLE
        a = (a_game * self.items)
        b = (a + self.items)
        for i in range(a, b):
            if (a_points >= self.hof[i][1]):
                s = ('Congratulations Top-%d! You got %d (%d) points. What is your name:' % (((i - a) + 1),
                 a_points,
                 a_oo))
                name = user_set.name()
                s = appuifw.query(unicode(s), 'text', unicode(name))
                if s:
                    user_set.name(s)
                break

        if ((i - a) < (self.items - 1)):
            for j in range((b - 1), i, -1):
                self.hof[j] = self.hof[(j - 1)][:]

            self.hof[i] = [user_set.name(),
             a_points,
             a_oo]



    def reset(self):
        self.hof = [ [ANAME,
         1,
         1] for i in range((self.items * self.games)) ]



    def save_score(self, a_file):
        f = open(a_file, 'w')
        for i in range((self.games * self.items)):
            s = str(('%s\t%d\t%d\n' % (self.hof[i][0],
             self.hof[i][1],
             self.hof[i][2])))
            f.write(s)

        f.close()



class oo00(object):
    __module__ = __name__

    def __init__(self, squares, color):
        self._o0o = squares
        self._o0O = color
        self._o00 = 0



    def fix(self, x, y, _oO00):
        for s in self._o0o[self._o00]:
            _oO00.board[(x + s[0])][(y + s[1])] = self._o0O




    def test(self, x, y, _oO00):
        for s in self._o0o[self._o00]:
            a = (x + s[0])
            b = (y + s[1])
            if ((b >= _oO00._oO00oOO) or ((a < 0) or ((a >= _oO00._oO00oO0) or _oO00.board[a][b]))):
                return False

        return True



    def draw(self, x, y, _oO00, a = -1):
        if (a == -1):
            a = self._o00
        _oO00._oO00o(x, y, self._o0o[a], self._o0O)



    def clear(self, x, y, _oO00):
        _oO00._oO00o(x, y, self._o0o[self._o00], 0)



    def move(self, x1, y1, x2, y2, _oO00):
        atile = {}
        for s in self._o0o[self._o00]:
            atile[s] = 0

        for s in self._o0o[self._o00]:
            x = (x2 + s[0])
            y = (y2 + s[1])
            if atile.has_key((x,
             y)):
                del atile[(x,
                 y)]
            else:
                atile[(x,
                 y)] = self._o0O

        alist = []
        for (x, y,) in atile.iteritems():
            alist.append((x,
             y))

        _oO00._oO00o2(x1, y1, alist)



    def rotate(self, x, y, a, _oO00):
        result = False
        old = self._o00
        self._o00 = ((self._o00 + a) % 4)
        if self.test(x, y, _oO00):
            result = True
        self._o00 = old
        return result



    def tilt(self, a):
        self._o00 = ((self._o00 + a) % 4)



pieces = (oo00({0: ((1,
       0),
      (0,
       1),
      (1,
       1),
      (2,
       1)),
  1: ((1,
       0),
      (1,
       1),
      (2,
       1),
      (1,
       2)),
  2: ((0,
       1),
      (1,
       1),
      (2,
       1),
      (1,
       2)),
  3: ((1,
       0),
      (0,
       1),
      (1,
       1),
      (1,
       2))}, 1),
 oo00({0: ((0,
       1),
      (1,
       1),
      (2,
       1),
      (3,
       1)),
  1: ((1,
       0),
      (1,
       1),
      (1,
       2),
      (1,
       3)),
  2: ((0,
       1),
      (1,
       1),
      (2,
       1),
      (3,
       1)),
  3: ((1,
       0),
      (1,
       1),
      (1,
       2),
      (1,
       3))}, 2),
 oo00({0: ((1,
       0),
      (2,
       0),
      (1,
       1),
      (2,
       1)),
  1: ((1,
       0),
      (2,
       0),
      (1,
       1),
      (2,
       1)),
  2: ((1,
       0),
      (2,
       0),
      (1,
       1),
      (2,
       1)),
  3: ((1,
       0),
      (2,
       0),
      (1,
       1),
      (2,
       1))}, 3),
 oo00({0: ((0,
       0),
      (1,
       0),
      (1,
       1),
      (2,
       1)),
  1: ((2,
       0),
      (1,
       1),
      (2,
       1),
      (1,
       2)),
  2: ((0,
       0),
      (1,
       0),
      (1,
       1),
      (2,
       1)),
  3: ((2,
       0),
      (1,
       1),
      (2,
       1),
      (1,
       2))}, 4),
 oo00({0: ((1,
       0),
      (2,
       0),
      (0,
       1),
      (1,
       1)),
  1: ((0,
       0),
      (0,
       1),
      (1,
       1),
      (1,
       2)),
  2: ((1,
       0),
      (2,
       0),
      (0,
       1),
      (1,
       1)),
  3: ((0,
       0),
      (0,
       1),
      (1,
       1),
      (1,
       2))}, 5),
 oo00({0: ((2,
       0),
      (0,
       1),
      (1,
       1),
      (2,
       1)),
  1: ((1,
       0),
      (1,
       1),
      (1,
       2),
      (2,
       2)),
  2: ((1,
       0),
      (2,
       0),
      (3,
       0),
      (1,
       1)),
  3: ((1,
       0),
      (2,
       0),
      (2,
       1),
      (2,
       2))}, 6),
 oo00({0: ((1,
       0),
      (1,
       1),
      (2,
       1),
      (3,
       1)),
  1: ((1,
       0),
      (2,
       0),
      (1,
       1),
      (1,
       2)),
  2: ((0,
       0),
      (1,
       0),
      (2,
       0),
      (2,
       1)),
  3: ((2,
       0),
      (2,
       1),
      (2,
       2),
      (1,
       2))}, 7))
class oo000(object):
    __module__ = __name__

    def __init__(self, x, y):
        self.color = [(0,
          0,
          0),
         (160,
          0,
          240),
         (0,
          240,
          240),
         (240,
          240,
          0),
         (240,
          0,
          0),
         (0,
          240,
          0),
         (240,
          160,
          0),
         (0,
          0,
          240)]
        self.name = 'Jomtris'
        self._oO00oo = 0.5
        self.game = 0
        self._oO00oO = False
        self._oO00oO0 = x
        self._oO00oOO = y
        self.clear()
        self.mask = None
        self.tile = []
        self.g_oo000(nm.size[0], nm.size[1])
        self._0O0OooO(True)
        self.g_oo00()



    def g_oo00(self):
        global T_LEFT
        global T_RIGHT
        global T_TOP
        (x, y,) = nm.size
        if (x > y):
            (a1, b1,) = self._0O0Ooo0(16, 9)
        else:
            (a1, b1,) = self._0O0Ooo0(10, 13)
        T_LEFT = (a1 + (self.wide / 2))
        T_RIGHT = (nm.size[0] - 10)
        T_TOP = (b1 + (self.wide / 2))



    def g_oo000(self, sx, sy):
        x = self._oO00oO0
        y = self._oO00oOO
        w = self.wide = min(((sx - 4) / x), ((sy - 4) / (y - 2)))
        if self.mask:
            del self.mask
        self.mask = graphics.Image.new((w,
         w), mode='L')
        self.mask.clear((200,
         200,
         200))
        if self.tile:
            del self.tile
            self.tile = []
        self.tile = [ graphics.Image.new((w,
         w)) for i in range(8) ]
        self.tile[0].clear(AAABLACK)
        for i in range(0, w, 2):
            self.tile[0].point(((w - 1),
             i), outline=AAAYELLOW)
            self.tile[0].point((i,
             (w - 1)), outline=AAAYELLOW)

        for i in range(1, 8):
            (r, g, b,) = self.color[i]
            c = (r,
             g,
             b)
            c2 = (((3 * r) / 4),
             ((3 * g) / 4),
             ((3 * b) / 4))
            self.tile[i].ellipse((-2,
             -2,
             (w + 2),
             (w + 2)), width=5, outline=c, fill=c2)
            self.tile[i].point(((w / 3),
             (w / 3)), width=3, outline=AAAYELLOW)




    def _0O0Oo0o(self):
        global oo0000
        oo0000 = AIlPLAY
        self.clear()
        self._0O0OooO(True)
        _oO00.do__oO00oO(False)



    def clear(self):
        self.board = [ [ 0 for j in range(self._oO00oOO) ] for i in range(self._oO00oO0) ]
        self.level_0 = user_set.level()
        self.level = user_set.level()
        self.lines = 0
        self.score = 0
        self.o0O0o0o = None
        self.o0O0o0o2 = None
        self.pindex = []
        self._oO00oo = 0.5



    def _0O0Oooo(self):
        if (self.pindex == []):
            self.pindex = range(7)
            random.shuffle(self.pindex)
        piece = pieces[self.pindex[0]]
        del self.pindex[0]
        return piece



    def _0O0OooO(self, init = False):
        if init:
            self.o0O0o0o2 = self._0O0Oooo()
            self.o0O0o0o3 = self._0O0Oooo()
            self.o0O0o0o4 = self._0O0Oooo()
        self.o0O0o0o = self.o0O0o0o2
        self.o0O0o0o2 = self.o0O0o0o3
        self.o0O0o0o3 = self.o0O0o0o4
        self.o0O0o0o4 = self._0O0Oooo()
        self.o0O0o0o._o00 = 0
        self.o0O0o0o_x = 3
        self.o0O0o0o_y = 0



    def _0o0Oo0o(self):
        (a, b,) = self._0O0Ooo0(self._oO00oO0, self._oO00oOO)
        s = u'Jomtris:'
        ((x1, y1, x2, y2,), dummy, dummy,) = mn.measure_text(s, font='title')
        x = ((a / 2) - (x2 / 2))
        y = (b / 3)
        mn.text(((x - 1),
         (y - 1)), s, fill=AAAWHITE, font='title')
        mn.text(((x + 1),
         (y + 1)), s, fill=AAABLACK, font='title')
        mn.text((x,
         y), s, fill=AAAYELLOW, font='title')
        s = u'* Winter 2009 *'
        ((x1, y1, x2, y2,), dummy, dummy,) = mn.measure_text(s, font='annotation')
        x = ((a / 2) - (x2 / 2))
        y += 25
        mn.text(((x - 1),
         (y - 1)), s, fill=AAAWHITE, font='annotation')
        mn.text(((x + 1),
         (y + 1)), s, fill=AAABLACK, font='annotation')
        mn.text((x,
         y), s, fill=AAAYELLOW, font='annotation')
        y += 10
        s = u'Press any key'
        ((x1, y1, x2, y2,), dummy, dummy,) = mn.measure_text(s)
        x = ((a / 2) - (x2 / 2))
        y += 25
        mn.text(((x - 1),
         (y - 1)), s, fill=AAABLACK)
        mn.text(((x + 1),
         (y + 1)), s, fill=AAABLACK)
        mn.text((x,
         y), s, fill=AAAYELLOW)
        s = u'to play!'
        ((x1, y1, x2, y2,), dummy, dummy,) = mn.measure_text(s)
        x = ((a / 2) - (x2 / 2))
        y += 25
        mn.text(((x - 1),
         (y - 1)), s, fill=AAABLACK)
        mn.text(((x + 1),
         (y + 1)), s, fill=AAABLACK)
        mn.text((x,
         y), s, fill=AAAYELLOW)
        o0Oo()



    def oOoOo(self):
        global oo0000
        if (oo0000 == AIlIDLE):
            self._0O0Oo0o()
            return 
        elif (oo0000 == AIlPAUS):
            self.do__oO00oO(False)
            return 
        elif (oo0000 != AIlPLAY):
            return 
        oo0000 = AIlHARD
        mnm.cancel()
        y = self.o0O0o0o_y
        c = 0
        while self.o0O0o0o.test(self.o0O0o0o_x, (y + 1), self):
            self.o0O0o0o.move(self.o0O0o0o_x, y, 0, 1, self)
            o0Oo()
            y += 1
            c += 5

        if (self.o0O0o0o_y != y):
            self.o0O0o0o.fix(self.o0O0o0o_x, y, self)
            o0Oo()
            self.o0O0o0o_y = y
            self.score += (c * self.level)
        oo0000 = AIlPLAY
        mnm.after(self._oO00oo, lambda :self.o0o0o(0, 1)
)



    def o0o0o(self, x, y):
        if (oo0000 == AIlIDLE):
            self._0O0Oo0o()
            return 
        elif (oo0000 == AIlPAUS):
            self.do__oO00oO(False)
            return 
        elif (oo0000 != AIlPLAY):
            return 
        if (x == 0):
            mnm.cancel()
        if y:
            b = 1
        else:
            b = 0
        if (not self.o0oOo(x, b)):
            mnm.cancel()
            x = 0
            self.o0O0o0o.fix(self.o0O0o0o_x, self.o0O0o0o_y, self)
            self.score += self.level
            self.o0O0o0o = None
            removed = self._oOo0o()
            if removed:
                self.lines += removed
                n = [100,
                 300,
                 600,
                 1200]
                self.score += (n[(removed - 1)] * self.level)
                self.level = ((self.level_0 + (self.lines / 10)) + 1)
                self._oO00oo = (0.5 * (0.85 ** (self.level - 1)))
            self._oOo0o_0()
            if (self.o0O0o0o_y < 2):
                self.oOo0o()
            else:
                self._0O0OooO()
                self._oOo0o_O()
                if self.o0O0o0o.test(self.o0O0o0o_x, self.o0O0o0o_y, self):
                    self.o0O0o0o.draw(self.o0O0o0o_x, self.o0O0o0o_y, self)
                else:
                    self.oOo0o()
        elif (y == 2):
            self.score += self.level
            self._oOo0o_0()
        o0Oo()
        if ((oo0000 == AIlPLAY) and (x == 0)):
            mnm.after(self._oO00oo, lambda :self.o0o0o(0, 1)
)



    def oOo0o(self):
        global oo0000
        oo0000 = AIlDONE
        top10.check_score(self.score, self.level, self.game)
        self._0o0Oo0o()



    def o0oOo(self, x, y):
        result = False
        if self.o0O0o0o.test((self.o0O0o0o_x + x), (self.o0O0o0o_y + y), self):
            self.o0O0o0o.move(self.o0O0o0o_x, self.o0O0o0o_y, x, y, self)
            self.o0O0o0o_x += x
            self.o0O0o0o_y += y
            result = True
        elif (y == 0):
            result = True
        return result



    def _oOo0o(self):
        removed = 0
        o0Oo()
        for i in range(self._oO00oOO):
            if self._oOo0o_(i):
                self.remove_one_row(i)
                self._oOo0o_o()
                o0Oo()
                removed += 1

        return removed



    def _oOo0o_(self, row):
        for x in range(self._oO00oO0):
            if (not self.board[x][row]):
                return False

        return True



    def remove_one_row(self, row):
        for y in range(row, 0, -1):
            for x in range(self._oO00oO0):
                self.board[x][y] = self.board[x][(y - 1)]


        for x in range(self._oO00oO0):
            self.board[x][0] = 0




    def change_o00(self, a):
        if (oo0000 == AIlIDLE):
            self._0O0Oo0o()
            return 
        elif (oo0000 != AIlPLAY):
            return 
        result = self.o0O0o0o.rotate(self.o0O0o0o_x, self.o0O0o0o_y, a, self)
        if result:
            self.o0O0o0o.clear(self.o0O0o0o_x, self.o0O0o0o_y, self)
            self.o0O0o0o.tilt(a)
            self.o0O0o0o.draw(self.o0O0o0o_x, self.o0O0o0o_y, self)
            o0Oo()



    def _oO00o(self, a, b, a_piece, a_o0O):
        w = self.wide
        (x, y,) = self._0O0Ooo0(a, b)
        for s in a_piece:
            x1 = (x + (s[0] * w))
            y1 = (y + (s[1] * w))
            mn.blit(self.tile[a_o0O], target=(x1,
             y1))
            if (not a_o0O):
                mn.blit(pic, source=(x1,
                 y1,
                 (x1 + w),
                 (y1 + w)), target=(x1,
                 y1), mask=self.mask)




    def _oO00o2(self, a, b, tiles):
        w = self.wide
        (x, y,) = self._0O0Ooo0(a, b)
        for s in tiles:
            x1 = (x + (s[0][0] * w))
            y1 = (y + (s[0][1] * w))
            c = s[1]
            mn.blit(self.tile[c], target=(x1,
             y1))
            if (not c):
                mn.blit(pic, source=(x1,
                 y1,
                 (x1 + w),
                 (y1 + w)), target=(x1,
                 y1), mask=self.mask)




    def _oOo0o_o(self):
        w = self.wide
        YY = 1
        (x1, y1,) = self._0O0Ooo0(0, YY)
        (x2, y2,) = self._0O0Ooo0(self._oO00oO0, self._oO00oOO)
        a1 = (x1 - 2)
        a2 = ((y1 + w) - 2)
        x2 = x2
        y2 = y2
        for y in range(YY, self._oO00oOO):
            a1 = x1
            for x in range(self._oO00oO0):
                mn.blit(self.tile[self.board[x][y]], target=(a1,
                 y1))
                if (not self.board[x][y]):
                    mn.blit(pic, source=(a1,
                     y1,
                     (a1 + w),
                     (y1 + w)), target=(a1,
                     y1), mask=self.mask)
                a1 += w

            y1 += w




    def g_oo0(self):
        mn.blit(pic)
        w = self.wide
        YY = 1
        (x1, y1,) = self._0O0Ooo0(0, YY)
        (x2, y2,) = self._0O0Ooo0(self._oO00oO0, self._oO00oOO)
        a1 = (x1 - 2)
        a2 = ((y1 + w) - 2)
        x2 = x2
        y2 = y2
        points = [(a1,
          a2),
         (a1,
          y2),
         (x2,
          y2),
         (x2,
          a2)]
        mn.line(points, width=2, outline=AAAYELLOW)
        self._oOo0o_o()
        if self.o0O0o0o:
            self.o0O0o0o.draw(self.o0O0o0o_x, self.o0O0o0o_y, self)
        (a1, b1,) = self._0O0Ooo0(11, 3)
        a2 = (a1 + (4 * w))
        s = u'Jomtris'
        ((x1, y1, x2, y2,), dummy, dummy,) = mn.measure_text(s, font='annotation')
        x = ((a1 + ((a2 - a1) / 2)) - ((x2 - x1) / 2))
        y = (b1 + (2.8 * w))
        mn.text(((x - 1),
         (y - 1)), s, fill=AAABLACK, font=('annotation',
         None,
         graphics.FONT_BOLD))
        mn.text(((x + 1),
         (y + 1)), s, fill=AAABLACK, font=('annotation',
         None,
         graphics.FONT_BOLD))
        mn.text((x,
         y), s, fill=AAAYELLOW, font='annotation')
        t_top = T_TOP
        mn.text(((T_LEFT + 1),
         (t_top + 1)), u'Level:', font='title', fill=AAABLACK)
        mn.text((T_LEFT,
         t_top), u'Level:', font='title', fill=AAAYELLOW)
        t_top += 50
        mn.text(((T_LEFT + 1),
         (t_top + 1)), u'Lines:', font='title', fill=AAABLACK)
        mn.text((T_LEFT,
         t_top), u'Lines:', font='title', fill=AAAYELLOW)
        t_top += 50
        mn.text(((T_LEFT + 1),
         (t_top + 1)), u'Score:', font='title', fill=AAABLACK)
        mn.text((T_LEFT,
         t_top), u'Score:', font='title', fill=AAAYELLOW)
        self._oOo0o_0()
        self._oOo0o_O()
        if ((oo0000 & (AIlIDLE | AIlPAUS)) or ((fc_run & (AIlIDLE | AIlPAUS)) or ((len(w_run) > 0) and (w_run[0] & (AIlIDLE | AIlPAUS))))):
            self._0o0Oo0o()



    def _oOo0o_0(self):
        t_top = T_TOP
        self._oOo0o_02(t_top, (u'%d' % self.level))
        t_top += 50
        s = (u'%d' % self.lines)
        self._oOo0o_02(t_top, s)
        t_top += 50
        s = (u'%d' % self.score)
        self._oOo0o_02(t_top, s)



    def _oOo0o_02(self, t_top, s):
        mn.rectangle(((T_LEFT + 5),
         (t_top + 5),
         T_RIGHT,
         (t_top + 25)), None, AAABG)
        ((x1, y1, x2, y2,), dummy, dummy,) = mn.measure_text(s)
        mn.text((((T_RIGHT - 5) - x2),
         (t_top + 20)), s, fill=AAAWHITE)



    def _oOo0o_O(self):
        if self.o0O0o0o2:
            a = [(0,
              0),
             (1,
              0),
             (2,
              0),
             (3,
              0),
             (0,
              1),
             (1,
              1),
             (2,
              1),
             (3,
              1)]
            _oO00._oO00o(11, 2.5, a, 0)
            self.o0O0o0o2.draw(11, 2.5, self, 0)
            (a1, b1,) = self._0O0Ooo0(11, 6.5)
            a2 = (a1 + (4 * self.wide))
            b2 = (b1 + (4.5 * self.wide))
            mn.blit(pic, source=(a1,
             b1,
             a2,
             b2), target=(a1,
             b1,
             a2,
             b2))
            self.o0O0o0o3.draw(11, 6.5, self, 0)
            self.o0O0o0o4.draw(11, 9, self, 0)



    def do__oO00oO(self, _o0 = 999, a_visible = True):
        global oo0000
        if ((oo0000 != AIlPLAY) and (oo0000 != AIlPAUS)):
            return 
        if (_o0 == 999):
            if self._oO00oO:
                self._oO00oO = False
            else:
                self._oO00oO = True
        else:
            self._oO00oO = _o0
        mnm.cancel()
        nmn.cancel()
        if self._oO00oO:
            oo0000 = AIlPAUS
            if a_visible:
                self._0o0Oo0o()
        else:
            ooo()
            oo0000 = AIlPLAY
            if a_visible:
                self.g_oo0()
                o0Oo()
            mnm.after(_oO00._oO00oo, lambda :_oO00.o0o0o(0, 1)
)



    def _0O0Ooo0(self, x, y):
        off_x = 8
        off_y = 5
        return (((x * self.wide) + off_x),
         (((y - 2) * self.wide) + off_y))



class JomtrisMain(object):
    __module__ = __name__

    def __init__(self):
        global mn
        global pic
        global nm
        global _oO00
        global top10
        global user_set
        self.options = [[(u'New game',
           self.menu_start),
          (u'Top-10',
           self.menu0o0o0),
          (u'Settings',
           self.show_settings),
          (u'About',
           self.menu_about),
          (u'Exit',
           self.cb_quit)],
         [(u'Reset',
           self.oO0ooo00),
          (u'Back',
           self.oO0ooo0)],
         [(u'Change',
           self.handle_settings),
          (u'Reset',
           self.oO0oO0oo),
          (u'Back',
           self.oO0ooo0)]]
        self.lb = appuifw.Listbox([u''], lambda :None
)
        appuifw.app.screen = 'full'
        appuifw.app.title = u'Jomtris'
        appuifw.app.exit_key_handler = self.cb_quit
        appuifw.app.focus = o0O
        appuifw.app.menu = self.options[0]
        nm = appuifw.Canvas(resize_callback=o0oo, redraw_callback=o0Oo)
        appuifw.app.body = nm
        mn = graphics.Image.new(nm.size)
        if pic:
            pic = graphics.Image.resize(pic, mn.size)
        else:
            pic = graphics.Image.new(nm.size)
            pic.clear(AAABG)
        self.game = 0
        top10 = CHS(AATOP, AITEMS, 3)
        user_set = CMS(AASET)
        _oO00 = oo000(10, 22)
        self.o0O0o0o = None
        _oO00.g_oo0()
        o0Oo()
        nm.bind(key_codes.EKeyLeftArrow, lambda :_oO00.o0o0o(-1, 0)
)
        nm.bind(key_codes.EKeyRightArrow, lambda :_oO00.o0o0o(1, 0)
)
        nm.bind(key_codes.EKeyUpArrow, lambda :_oO00.change_o00(1)
)
        nm.bind(key_codes.EKeyDownArrow, lambda :_oO00.o0o0o(0, 2)
)
        nm.bind(key_codes.EKeyEnter, _oO00.oOoOo)
        nm.bind(key_codes.EKeySelect, _oO00.oOoOo)
        nm.bind(key_codes.EKey1, lambda :_oO00.change_o00(-1)
)
        nm.bind(key_codes.EKey2, lambda :_oO00.change_o00(1)
)
        nm.bind(key_codes.EKey3, lambda :_oO00.change_o00(1)
)
        nm.bind(key_codes.EKey4, lambda :_oO00.o0o0o(-1, 0)
)
        nm.bind(key_codes.EKey5, _oO00.oOoOo)
        nm.bind(key_codes.EKey6, lambda :_oO00.o0o0o(1, 0)
)
        nm.bind(key_codes.EKey8, lambda :_oO00.o0o0o(0, 2)
)
        nm.bind(key_codes.EKey0, _oO00.do__oO00oO)



    def menu_start(self, a_game = -1):
        _oO00._0O0Oo0o()



    def menu0o0o0(self):
        global g_ignore
        o0o(True)
        appuifw.app.exit_key_handler = self.oO0ooo0
        appuifw.app.menu = self.options[1]
        appuifw.app.set_tabs([u'Enduro',
         u'Leveler',
         u'Speedy'], self.top10_draw)
        self.lb = appuifw.Listbox([u''], self.top10_draw)
        g_ignore = True
        appuifw.app.screen = 'normal'
        appuifw.app.body = self.lb
        g_ignore = False
        appuifw.app.activate_tab(_oO00.game)
        self.top10_draw(_oO00.game)



    def top10_draw(self, index = 0):
        a = ((index * top10.items) + 1)
        b = (a + top10.items)
        hof = []
        for i in range(a, b):
            (name, points, level,) = top10.top(((i - a) + 1), index)
            s = ('%d: %d(%d) %s' % (((i - a) + 1),
             points,
             level,
             name))
            hof.append(unicode(s))

        self.lb.set_list(hof)



    def oO0ooo00(self):
        top10.reset()
        self.top10_draw()



    def show_settings(self):
        global g_ignore
        o0o(True)
        a = user_set.name()
        b = self.leftright(user_set.rotate())
        c = user_set.level()
        lb_list = self.lb_settings(a, b, str(c))
        self.lb = appuifw.Listbox(lb_list, self.handle_settings)
        appuifw.app.exit_key_handler = self.oO0ooo0
        appuifw.app.menu = self.options[2]
        g_ignore = True
        appuifw.app.screen = 'normal'
        appuifw.app.body = self.lb
        g_ignore = False



    def lb_settings(self, a, b, c):
        return [(u"Player's Name:",
          unicode(a)),
         (u'Default Rotation:',
          unicode(b)),
         (u'Start Level:',
          unicode(c))]



    def leftright(self, a):
        if (a == 1):
            return 'Right'
        else:
            return 'Left'



    def handle_settings(self):
        index = self.lb.current()
        if (index == 0):
            t = u'What is your name:'
            s1 = user_set.name()
            s1 = appuifw.query(t, 'text', unicode(s1))
            if s1:
                user_set.name(s1)
        elif (index == 1):
            b = user_set.rotate()
            b = ((b + 1) % 2)
            user_set.rotate(b)
        elif (index == 2):
            t = u'Give Start Level (1-9):'
            c = user_set.level()
            c = appuifw.query(t, 'number', c)
            if (c != None):
                if (c < 1):
                    c = 1
                if (c > 9):
                    c = 9
                user_set.level(c)
        s1 = user_set.name()
        b = user_set.rotate()
        s2 = self.leftright(b)
        s3 = str(user_set.level())
        lb_list = self.lb_settings(s1, s2, s3)
        self.lb.set_list(lb_list, index)
        appuifw.app.body = self.lb



    def oO0oO0oo(self):
        user_set.reset()
        self.show_settings()



    def oO0ooo0(self):
        global g_ignore
        appuifw.app.exit_key_handler = self.cb_quit
        g_ignore = True
        appuifw.app.screen = 'full'
        appuifw.app.body = nm
        g_ignore = False
        appuifw.app.menu = self.options[0]
        appuifw.app.set_tabs([], lambda :Null
)
        o0o(False)
        if (g_oo0000 != nm.size[0]):
            o0oo()



    def oO0ooo00(self):
        top10.reset()
        self.menu0o0o0()



    def menu_reset_score(self):
        board.reset_score()



    def query_newgame(self):
        if appuifw.query(u'New game?', 'query'):
            board._0O0Oo0o()
            board.g_oo0()



    def cb_quit(self):
        global pic
        global _oO00
        global top10
        global oo0000
        oo0000 = AIlEXIT
        mnm.cancel()
        nmn.cancel()
        top10.check_score(_oO00.score, _oO00.level, self.game)
        top10.save_score(AATOP)
        user_set.save(AASET)
        _oO00.tile = []
        del _oO00.mask
        del _oO00
        del top10
        del pic
        self.lb = []
        nm.bind(key_codes.EKeyLeftArrow, None)
        nm.bind(key_codes.EKeyRightArrow, None)
        nm.bind(key_codes.EKeyUpArrow, None)
        nm.bind(key_codes.EKeyDownArrow, None)
        nm.bind(key_codes.EKeyEnter, None)
        nm.bind(key_codes.EKeySelect, None)
        nm.bind(key_codes.EKey1, None)
        nm.bind(key_codes.EKey2, None)
        nm.bind(key_codes.EKey3, None)
        nm.bind(key_codes.EKey4, None)
        nm.bind(key_codes.EKey5, None)
        nm.bind(key_codes.EKey6, None)
        nm.bind(key_codes.EKey8, None)
        appuifw.app.set_tabs([], lambda :Null)
        app_lock.signal()



    def menu_about(self):
        o0o(True)
        appuifw.note((((u'Jomtris v' + VERSION) + '\n') + u'jouni.miettunen.googlepages.com\n\xa9 2008-2009 Jouni Miettunen'))
        o0o(False)



m = JomtrisMain()
app_lock = e32.Ao_lock()
app_lock.wait()

