import random
import appuifw, e32
from key_codes import *

# constants

# row evaluation constants depending on neighbours colors

# XO 4   0
# X. 1   3
# .. 0  10
# O. 3  30
# XX 2 100
# OO 6 300

rates = (10, 3, 100, 30, 0, 0, 300)

# neighbours squares for each position on the grid

neighbours = [
    [('23','59','47'),('13','58'),('12','57','69')],
    [('17','56'),('19','28','37','46'),('45','39')],
    [('14','53','89'),('79','52'),('78','51','36')]
]

# variables

grid = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
]
player = ['X', 'O'] # X = human, O = computer
input = -1
cx = cy = 0
aborted = ''

# subroutines

def setup(): 
    """ Symbian Series 60 UI setup """
    global canvas, old_body, old_screen
    old_body = appuifw.app.body
    old_screen = appuifw.app.screen
    appuifw.app.screen = 'full'
    canvas = appuifw.Canvas()
    appuifw.app.body = canvas
    appuifw.app.exit_key_handler = quit
    canvas.draw = display
    canvas.bind(EKeyRightArrow, lambda: cursor(1,0))
    canvas.bind(EKeyUpArrow,    lambda: cursor(0,-1))
    canvas.bind(EKeyLeftArrow,  lambda: cursor(-1,0))
    canvas.bind(EKeyDownArrow,  lambda: cursor(0,1))
    canvas.bind(EKeySelect,  enter)

def cleanup():
    """ restore saved objects """
    appuifw.app.body = old_body
    appuifw.app.screen = old_screen

def quit():
    """ abort game loop """
    global aborted
    aborted = '*'

def enter():
    """ select square under cursor """
    global input
    input = cx+cy*3+1

def cursor(dx, dy):
    """ cursor movement """
    global cx, cy
    cx += dx
    cy += dy
    if cx < 0:
        cx = 0
    elif cx > 2:
        cx = 2
    if cy < 0:
        cy = 0
    elif cy > 2:
        cy = 2

def display():
    """ game board display """
    canvas.line((12,77,162,77), 0x000000, width=4)
    canvas.line((12,127,162,127), 0x000000, width=4)
    canvas.line((62,27,62,177), 0x000000, width=4)
    canvas.line((112,27,112,177), 0x000000, width=4)
    for line in range(3):
        for column in range(3):
            x1 = column * 50 + 18
            y1 = line * 50 + 33
            x2 = x1 + 40
            y2 = y1 + 40
            canvas.rectangle((x1,y1,x2,y2), fill=0xffffff)
            piece = grid[line][column]
            if piece == 'X':
                canvas.line((x1,y1,x2,y2), 0x00ff00, width=4)
                canvas.line((x2,y1,x1,y2), 0x00ff00, width=4)
            elif piece == 'O':
                canvas.ellipse((x1,y1,x2,y2), 0xff0000, width=4)
            if cx == column and cy == line:
                canvas.rectangle((x1,y1,x2,y2), 0x0000ff)

def best(possible):
    """ use a static evaluation function to choose a move (not perfect) """
    bestrate = 0
    bestmove = 0
    for move in possible:
        line, column = divmod(move-1, 3)
        rate = 0
        for row in neighbours[line][column]:
            total = 0
            for square in row:
                line, column = divmod(int(square)-1, 3)
                color = grid[line][column]
                if color == 'X':
                    total += 1
                elif color == 'O':
                    total += 3
            rate += rates[total]
        if rate > bestrate:
            bestmove = move
            bestrate = rate
    return bestmove

def play():
    """ choose and play one move """
    global input
    move = 0
    if player[0] == 'X': # human
        if input:
            move = input
            input = 0
    else:       # computer
        possible = []   # list all possible moves
        for move in range(1, 10):
            line, column = divmod(move-1, 3)
            if grid[line][column] not in player:
                possible.append(move)
        if not possible: # grid is full
            quit()
            return
        else:
            #move = random.choice(possible) # random play
            move = best(possible) # choose the best move
    if 1 <= move <= 9:
        line, column = divmod(move-1, 3)
        if grid[line][column] in player: # square already occupied?
            appuifw.note(u"Invalid move!'", 'info')
        else:
            grid[line][column] = player[0]
            player[0], player[1] = player[1], player[0] # swap players

def finished():
    """ check for game end """
    if grid[0][0] == grid[0][1] == grid[0][2]:
        return grid[0][0]
    if grid[1][0] == grid[1][1] == grid[1][2]:
        return grid[1][0]
    if grid[2][0] == grid[2][1] == grid[2][2]:
        return grid[2][0]
    if grid[0][0] == grid[1][0] == grid[2][0]:
        return grid[0][0]
    if grid[0][1] == grid[1][1] == grid[2][1]:
        return grid[0][1]
    if grid[0][2] == grid[1][2] == grid[2][2]:
        return grid[0][2]
    if grid[0][0] == grid[1][1] == grid[2][2]:
        return grid[0][0]
    if grid[2][0] == grid[1][1] == grid[0][2]:
        return grid[2][0]
    return aborted

def game():
    """ game """
    for square in range(1, 10):
        row, col = divmod(square-1, 3)
        grid[row][col] = str(square)
    while not finished():
        display()
        play()
        e32.ao_sleep(0.08)
    display()
    winner = finished()
    if winner == '*':
        appuifw.note(u"Draw!", 'info')
    else:
        appuifw.note(u"%s wins!'" % winner, 'info')

# main program
setup()
playing = 1
while playing:
    game()
    playing = appuifw.query(u'Play again?','query')
cleanup()
