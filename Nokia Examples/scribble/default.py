# Copyright (c) 2009 Nokia Corporation
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

import appuifw
import e32
import os
import time
import operator
from graphics import *
from key_codes import *


class PaintApp():
    BG_COLOR = 0xffffff # white
    BORDER_COLOR = 0x000000 # black
    BRUSH_COLOR = 0x000000 # black
    ERASER_ACTIVE = 0xFF0000 # Red

    def __init__(self):
        appuifw.app.exit_key_handler = self.quit
        self.running = True
        appuifw.app.directional_pad = False
        self.erase_mode = False
        self.saving_file = False
        self.orientation_changed = False
        self.bind_palette = True
        self.about_active = False
        self.is_about_active = False
        self.about_timer = None
        self.pen_width = 4
        self.x_max = 0
        self.y_max = 0
        self.canvas = appuifw.Canvas(event_callback=self.event_callback,
                                     redraw_callback=self.redraw_callback)
        if self.canvas.size[0] > self.canvas.size[1]:
            self.orientation = 'landscape'
        else:
            self.orientation = 'portrait'
        self.drive = unicode(os.getcwd()[0])
        self.old_body = appuifw.app.body
        appuifw.app.body = self.canvas
        appuifw.app.screen = 'full'
        appuifw.app.focus = self.focus_monitor
        self.canvas.clear()
        self.draw = self.canvas
        self.draw_img = Image.new((self.canvas.size[0], self.canvas.size[1]))
        self.draw_buttons()
        self.bind_buttons()

    def draw_buttons(self):
        self.x_max = self.canvas.size[0]
        self.y_max = self.canvas.size[1]
        self.pointer_advance = min(self.x_max, self.y_max) / 4
        self.toolbar_size = max(self.x_max, self.y_max) / 4
        if self.orientation == 'landscape':
            box_width = self.pointer_advance - 10
            self.menu_bar_size = self.toolbar_size / 2
            self.color_palette = self.toolbar_size - self.menu_bar_size
            draw_position = self.x_max - self.menu_bar_size
            y_displacement = (self.menu_bar_size / 2) + 10
            self.options_button = ((draw_position, 0),
                                   (self.x_max, self.pointer_advance))
            self.clear_button = ((draw_position, self.pointer_advance),
                                 (self.x_max, 2 * self.pointer_advance))
            self.eraser = ((draw_position, 2 * self.pointer_advance),
                           (self.x_max, 3 * self.pointer_advance))
            self.quit_button = ((draw_position, 3 * self.pointer_advance),
                                (self.x_max, 4 * self.pointer_advance))
            self.draw.rectangle((draw_position, 0, self.x_max, self.y_max),
                                fill=self.BG_COLOR)
            self.draw.rectangle((self.x_max - self.toolbar_size, 0,
                                 self.x_max - self.menu_bar_size, self.y_max),
                                outline=self.BORDER_COLOR, width=5)
        else:
            box_width = self.pointer_advance
            self.menu_bar_size = self.toolbar_size / 4
            self.color_palette = self.toolbar_size - self.menu_bar_size
            draw_position = self.y_max - self.menu_bar_size
            y_displacement = (self.menu_bar_size / 2) + 5
            self.options_button = ((0, draw_position),
                                   (self.pointer_advance, self.y_max))
            self.clear_button = ((self.pointer_advance, draw_position),
                                 (2 * self.pointer_advance, self.y_max))
            self.eraser = ((self.pointer_advance * 2, draw_position),
                           (self.pointer_advance * 3, self.y_max))
            self.quit_button = ((self.pointer_advance * 3, draw_position),
                                (self.pointer_advance * 4, self.y_max))
            self.draw.rectangle((0, draw_position, self.x_max, self.y_max),
                                fill=self.BG_COLOR)
            self.draw.rectangle((0, self.y_max - self.toolbar_size,
                                 self.x_max, self.y_max - self.menu_bar_size),
                                outline=self.BORDER_COLOR, width=5)
        # Draw the buttons at the bottom and the respective text at an offset
        # specified by x_displacement and y_displacement
        buttons = [self.options_button, self.clear_button, self.eraser,
                   self.quit_button]
        options = [u'Options', u'Clear', u'Erase', u'Quit']
        for button, text in zip(buttons, options):
            if self.erase_mode and text == u'Erase':
                self.draw.rectangle(self.eraser, fill=self.ERASER_ACTIVE,
                                outline=self.BORDER_COLOR, width=5)
            else:
                self.draw.rectangle(button, outline=self.BORDER_COLOR, width=5)
            text_dimensions = self.draw.measure_text(text)
            x_displacement = (box_width - text_dimensions[0][2]) / 2
            self.draw.text((button[0][0] + x_displacement,
                            button[0][1] + y_displacement), text,
                            font=u'Sans MT TC Big5HK_S60C',
                            fill=self.BORDER_COLOR)
        self.draw_palette()

    def bind_buttons(self):
        self.canvas.bind(EButton1Down, self.reset_canvas, self.clear_button)
        self.canvas.bind(EButton1Down, self.options_callback,
                         self.options_button)
        self.canvas.bind(EButton1Down, self.set_exit, self.quit_button)
        self.canvas.bind(EButton1Down, self.eraser_callback, self.eraser)

    def clear_button_bindings(self):
        self.canvas.bind(EButton1Down, None, self.clear_button)
        self.canvas.bind(EButton1Down, None, self.options_button)
        self.canvas.bind(EButton1Down, None, self.quit_button)
        self.canvas.bind(EButton1Down, None, self.eraser)
        self.canvas.bind(EButton1Down, None)

    def focus_monitor(self, value):
        if value:
            self.canvas.blit(self.draw_img)
            self.draw_buttons()

    def set_exit(self, pos):
        appuifw.app.body = self.old_body
        self.canvas.bind(EButton1Down, None)
        self.canvas = None
        self.draw_img = None
        appuifw.app.focus = None
        self.running = False

    def options_callback(self, pos):
        option = appuifw.popup_menu([u'Save', u'Point/Line Width', u'About'],
                                    u'Options')
        pen_width_options = [u'1', u'2', u'3', u'4', u'5', u'6']
        if option == 0:
            self.save_callback()
        elif option == 1:
            pen_width_choice = appuifw.popup_menu(pen_width_options)
            if pen_width_choice is not None:
                self.pen_width = int(pen_width_options[pen_width_choice])
        elif option == 2:
            self.is_about_active = True
            self.show_about()
            return
        self.canvas.blit(self.draw_img)
        self.draw_buttons()

    def show_about(self):
        img_path = self.drive + u':\\data\\python\\about.png'
        if self.orientation == 'landscape' or not os.path.exists(img_path):
            appuifw.note(u"Scribble is Copyright (c) 2009 Nokia Corporation")
            self.canvas.blit(self.draw_img)
            self.draw_buttons()
        else:
            self.about_window = Image.open(img_path)
            self.about_active = True
            self.clear_button_bindings()
            self.canvas.blit(self.about_window)
            self.canvas.bind(EButton1Up, self.clear_about_screen, ((0, 0),
                             (self.x_max, self.y_max)))
            self.about_timer = e32.Ao_timer()
            self.about_timer.after(5, self.clear_about_screen)

    def clear_about_screen(self, pos=(0, 0)):
        if self.about_timer is not None:
            self.about_timer.cancel()
            self.about_timer = None
        self.canvas.bind(EButton1Up, None, ((0, 0), (self.x_max, self.y_max)))
        self.canvas.blit(self.draw_img)
        self.bind_palette = True
        self.draw_buttons()
        self.bind_buttons()
        self.about_active = False

    def eraser_callback(self, pos):
        # The pen_width and fill_color change in event_callback when erase_mode
        # changes
        self.erase_mode = not self.erase_mode
        self.draw_buttons()

    def save_callback(self):
        if not self.saving_file:
            self.saving_file = True
            save_dir = self.drive + u":\\data\\python\\"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            filename = save_dir + \
                   unicode(time.strftime("%d%m%Y%H%M%S", time.localtime())) + \
                   u".jpg"
            self.draw_img.save(filename, quality=100)
            appuifw.note(u"Saved :" + unicode(filename))
            self.canvas.blit(self.draw_img)
            self.saving_file = False
            self.draw_buttons()

    def set_brush_color(self, pos, color):
        self.BRUSH_COLOR = color

    def draw_and_bind_color(self, color):
        if self.orientation == 'portrait':
            self.top_left_x = (self.no_of_colors % (len(self.colors) / 2)) * \
                               self.color_box_width
            self.bottom_right_x = self.top_left_x + self.color_box_width
            self.top_left_y = self.y_max - self.toolbar_size
            self.bottom_right_y = self.y_max - self.menu_bar_size - \
                                  self.color_palette / 2
            if self.no_of_colors >= (len(self.colors) / 2):
                self.top_left_y = self.bottom_right_y
                self.bottom_right_y = self.y_max - self.menu_bar_size
        else:
            self.top_left_x = self.x_max - self.toolbar_size
            self.bottom_right_x = self.x_max - self.menu_bar_size - \
                                  self.color_palette / 2
            if self.no_of_colors >= (len(self.colors) / 2):
                self.top_left_x = self.bottom_right_x
                self.bottom_right_x = self.x_max - self.menu_bar_size
            self.top_left_y = (self.no_of_colors % (len(self.colors) / 2)) * \
                               self.color_box_width
            self.bottom_right_y = self.top_left_y + self.color_box_width

        self.top_left = (self.top_left_x, self.top_left_y)
        self.bottom_right = (self.bottom_right_x, self.bottom_right_y)
        # Draw the color rectangle and bind a function which sets the brush
        # color
        self.draw.rectangle((self.top_left, self.bottom_right),
                            fill=self.colors[color])
        if self.bind_palette:
            self.canvas.bind(EButton1Down,
                lambda pos: self.set_brush_color(pos, self.colors[color]),
                (self.top_left, self.bottom_right))
        self.no_of_colors += 1

    def draw_palette(self):
        self.colors = {'Black': 0x000000, 'Blue': 0x0000FF, 'Brown': 0xA52A2A,
                  'Gray': 0x808080, 'Green': 0x008000, 'Maroon': 0x800000,
                  'Orange': 0xFFA500, 'Pink': 0xFFC0CB, 'Purple': 0x800080,
                  'Silver': 0xC0C0C0, 'Violet': 0xEE82EE, 'Yellow': 0xFFFF00,
                  'Red': 0xFF0000, 'Lime': 0x00FF00}
        self.color_box_width = min(self.x_max, self.y_max) / (len(self.colors)
                                                               / 2)
        self.no_of_colors = 0
        map(self.draw_and_bind_color, sorted(self.colors))
        if self.bind_palette:
            self.bind_palette = False

    def reset_canvas(self, pos=(0, 0)):
        self.draw_img.clear(self.BG_COLOR)
        self.prev_x = 0
        self.prev_y = 0
        self.erase_mode = False
        self.canvas.clear(self.BG_COLOR)
        self.draw_buttons()

    def check_orientation(self):
        if not self.orientation_changed:
            self.orientation_changed = True
        else:
            self.orientation_changed = False
        self.x_max = self.canvas.size[0]
        self.y_max = self.canvas.size[1]

    def redraw_callback(self, rect):
        if self.about_active:
            self.canvas.blit(self.about_window)
        if rect == (0, 0, self.y_max, self.x_max) and \
                                                self.orientation == 'portrait':
            self.orientation = 'landscape'
            self.check_orientation()
        elif rect == (0, 0, self.y_max, self.x_max) and \
                                               self.orientation == 'landscape':
            self.orientation = 'portrait'
            self.check_orientation()

    def event_callback(self, event):
        if not event['type'] in [EButton1Up, EButton1Down, EDrag]:
            return

        if event['type'] == EButton1Up and self.is_about_active:
            # This check is for ignoring button up event generated when exiting
            # `About` menu option. The flag `is_about_active` is set when
            # `About` menu is active.
            self.is_about_active = False
            return

        if self.erase_mode:
            pen_size = self.pen_width * 2
            outline_color = self.BG_COLOR
            fill_color = self.BG_COLOR
        else:
            pen_size = self.pen_width
            outline_color = self.BRUSH_COLOR
            fill_color = self.BRUSH_COLOR

        # Ignore the touch events in the region where buttons are drawn or if
        # about screen is active
        if (self.orientation == 'portrait' and event['pos'][1] > \
           (self.y_max - self.toolbar_size - 3 - (pen_size/2))) or \
           self.about_active:
            self.prev_x = event['pos'][0]
            self.prev_y = self.y_max - self.toolbar_size - 3 - (pen_size / 2)
            return
        elif (self.orientation == 'landscape' and event['pos'][0] > \
             (self.x_max - self.toolbar_size - 3 - (pen_size/2))) or \
             self.about_active:
            self.prev_x = self.x_max - self.toolbar_size - 3 - (pen_size / 2)
            self.prev_y = event['pos'][1]
            return

        if event['type'] in [EButton1Down, EButton1Up]:
            self.draw.point((event['pos'][0], event['pos'][1]),
                    outline=outline_color, width=pen_size, fill=fill_color)
            self.draw_img.point((event['pos'][0], event['pos'][1]),
                    outline=outline_color, width=pen_size, fill=fill_color)
        elif event['type'] == EDrag:
            rect = (self.prev_x, self.prev_y, event['pos'][0], event['pos'][1])
            redraw_rect = list(rect)
            # Ensure that the prev_x and prev_y co-ordinates are above the
            # current co-ordinates. This way we can use prev_x and prev_y as
            # the top left corner and the current co-ordinates as the bottom
            # right corner of the rect to be passed to begin_redraw.
            if redraw_rect[0] > redraw_rect[2]:
                redraw_rect[0], redraw_rect[2] = redraw_rect[2], redraw_rect[0]
            if redraw_rect[1] > redraw_rect[3]:
                redraw_rect[1], redraw_rect[3] = redraw_rect[3], redraw_rect[1]
            self.canvas.begin_redraw((redraw_rect[0] - pen_size,
                                      redraw_rect[1] - pen_size,
                                      redraw_rect[2] + pen_size,
                                      redraw_rect[3] + pen_size))
            self.draw.line(rect, outline=outline_color, width=pen_size,
                           fill=fill_color)
            self.draw_img.line(rect, outline=outline_color, width=pen_size,
                           fill=fill_color)
            self.canvas.end_redraw()
        self.prev_x = event['pos'][0]
        self.prev_y = event['pos'][1]

    def run(self):
        while self.running:
            e32.ao_sleep(0.01)
            if self.orientation_changed:
                if self.orientation == 'landscape':
                    self.new_draw_img = self.draw_img.transpose(ROTATE_90)
                elif self.orientation == 'portrait':
                    self.new_draw_img = self.draw_img.transpose(ROTATE_270)
                self.draw_img = None
                self.draw_img = Image.new((self.canvas.size[0],
                                          self.canvas.size[1]))
                self.draw_img.blit(self.new_draw_img)
                self.new_draw_img = None
                self.canvas.blit(self.draw_img)
                self.clear_button_bindings()
                if self.about_active:
                    self.clear_about_screen()
                self.bind_palette = True
                self.draw_buttons()
                self.bind_buttons()
                self.orientation_changed = False

        self.quit()

    def quit(self):
        appuifw.app.exit_key_handler = None
        self.running = False


if __name__ == '__main__':
    if not appuifw.touch_enabled():
        appuifw.note(u"This application only works on devices that support " +
                     u"touch input")
    else:
        d = PaintApp()
        d.run()
