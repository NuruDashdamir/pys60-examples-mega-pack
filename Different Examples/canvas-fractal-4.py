#  "Mandelbrot Set Fractal Generator"
#  (c) Copyright 2008 Brian Fattorini under terms of GPL
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the 
#  GNU General Public License as published by the Free Software Foundation, either version 3 of the 
#  License, or (at your option) any later version. This program is distributed in the hope that it 
#  will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
#  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  <http://www.gnu.org/licenses/>.
#
#  Note: You need to have Python for S60 version installed on your phone for this to work.
#  Tested on Nokia e90 (s60 3rd edition - front screen only).
#
#  Future functionality to include ability to zoom into a particular area..
#  Bugs: It won't exit gracefully until finished plotting.
#        Causes mayhem when jumping between front screen & large screen on e90.
#
#  Inspired by the superb open source software Fractint.

__author__  = "Brian Fattorini"
__email__   = "brian (at) aeolian (dot) co (dot) uk"
__version__ = "0.1"
__date__    = "$Date: 2008/05/03 12:00:00 $"[7:-2]

import appuifw, e32, key_codes, graphics

def draw_point(column, row, colour):
    img.point((column, row), outline = colour, width = 1)
    #canvas.blit(img)  # Print to screen on a per pixel basis (slow).

def handle_redraw(rect):
    if img:
        canvas.blit(img)  # Print to screen on a per line basis.

def handle_event(event):
    # Maybe handle key code events in some future release..
    #ev = event["keycode"]
    #if ev == key_codes.EKeyUpArrow:
    #    wibble = None
    handle_redraw(None)

def quit():
    appuifw.app.set_exit()

def mandelbrot():
    xIncrement = (xMax - xMin)/maxColumn
    yIncrement = (yMax - yMin)/maxRow
    for row in range(maxRow):
        cIp = yMin + (row * yIncrement)
        canvas.blit(img)
        for column in range(maxColumn):
            cRp = xMin + (column * xIncrement)
            zIp = cIp
            zRp = cRp
            iteration = 0
            test = 0
            while ((test < bailout) and (iteration < maxIteration)):
                zRpSquared = zRp * zRp
                zIpSquared = zIp * zIp
                zTemp = zRp * zIp
                zIp = cIp + zTemp + zTemp
                zRp = cRp + zRpSquared - zIpSquared
                test = zRpSquared + zIpSquared
                iteration += 1
                if test < 4:
                    if iteration == maxIteration:
                        draw_point(column, row, red)
                    if iteration == (maxIteration - 82):
                        draw_point(column, row, green)
                    if iteration == (maxIteration - 93):
                        draw_point(column, row, purple)
    handle_redraw(None)


if __name__ == '__main__':
     
    # Define constants.
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    red = (177, 0, 0)
    green = (0, 244, 0)
    purple = (84, 14, 155)
    maxIteration = 100  # Lowering this number will speed up the processing but lower the fractal quality.
    bailout = 4
    xMin = -2.25
    xMax = 0.75
    yMin = -1.5
    yMax = 1.5

    img = None
    canvas = appuifw.Canvas(redraw_callback = handle_redraw, event_callback = handle_event)
    appuifw.app.body = canvas
    appuifw.app.screen = "normal"  # options are 'normal', 'large' and 'full'.
    appuifw.app.exit_key_handler = quit
    appuifw.app.title = u"Mandelbrot Set Fractal Generator"
    maxColumn, maxRow = canvas.size
    img = graphics.Image.new((maxColumn, maxRow))
    img.clear(black)
    
    mandelbrot()
    
    # Uncomment the following two lines to enable screen capture grab at the end of drawing.
    #screenCap = graphics.screenshot()
    #screenCap.save(u"e:\\Images\screenshot.png")
    
    app_lock = e32.Ao_lock()
    app_lock.wait()

