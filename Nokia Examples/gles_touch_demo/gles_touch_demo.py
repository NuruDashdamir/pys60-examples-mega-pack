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
from gles import *
from glcanvas import *
import graphics


class GlesBall:

    vertices = array(GL_FLOAT, 3, (
        [-1.0, 1.0, -0.0],
        [1.0, 1.0, -0.0],
        [-1.0, -1.0, -0.0],
        [1.0, -1.0, -0.0]))

    normals = array(GL_FLOAT, 3, (
        [0.0, 0.0, 1.0],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, 1.0]))

    tex_coords = array(GL_FLOAT, 3, (
        [0.0, 1.0],
        [1.0, 1.0],
        [0.0, 0.0],
        [1.0, 0.0]))

    def __init__(self):
        self.exitflag = False
        self.old_body = appuifw.app.body
        appuifw.app.screen = 'large'
        self.canvas = None
        self.texhandle = 0
        appuifw.app.directional_pad = False
        self.x_coord = 0
        self.y_coord = 0
        self.gl_initialized = False
        self.canvas = GLCanvas(redraw_callback=self.redraw,
                               event_callback=self.event,
                               resize_callback=self.resize)
        appuifw.app.body = self.canvas
        self.x_max = self.canvas.size[0]
        self.y_max = self.canvas.size[1]
        # Factor used in the calculation of relative mapping of the pixels to
        # gles units
        self.x_factor = 30
        self.y_factor = 30
        self.init_gl()

    def event(self, event_dict):
        if 'pos' in event_dict:
            self.x, self.y = event_dict['pos']
            diff = self.x - (self.x_max / 2.0)
            self.x_coord = diff / self.x_factor
            diff = (self.y_max / 2.0) - self.y
            self.y_coord = diff / self.y_factor

    def init_view(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = float(self.canvas.size[1]) / float(self.canvas.size[0])
        glFrustumf(-1.0, 1.0, -1.0*aspect, 1.0*aspect, 3, 1000.0)
        glViewport(0, 0, self.canvas.size[0], self.canvas.size[1])
        glMatrixMode(GL_MODELVIEW)

    def init_gl(self):
        glEnable(GL_DEPTH_TEST)

        self.init_view()
        self.gl_initialized = True

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light0_ambient = array(GL_FLOAT, 3, ([0.1, 0.1, 0.1, 1.0]))
        glLightfv(GL_LIGHT0, GL_AMBIENT, light0_ambient)
        light0_diffuse = array(GL_FLOAT, 3, ([0.7, 0.7, 0.7, 1.0]))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_diffuse)
        light0_specular = array(GL_FLOAT, 3, ([0.7, 0.7, 0.7, 1.0]))
        glLightfv(GL_LIGHT0, GL_SPECULAR, light0_specular)

        light0_position = array(GL_FLOAT, 3, ([0.0, 10.0, 10.0, 0.0]))
        glLightfv(GL_LIGHT0, GL_POSITION, light0_position)
        light0_direction = array(GL_FLOAT, 3, ([0.0, 0.0, -1.0]))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light0_direction)

        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 45.0)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_SRC_COLOR)
        self.img = graphics.Image.open(os.getcwd()[0] +
                                       ":\\data\\python\\ball.png")
        self.texhandle = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texhandle)

        # Disable mip mapping
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_FASTEST)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.img.size[0],
                     self.img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, self.img)

    def redraw(self, rect):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor4f(1.0, 1.0, 1.0, 1.0)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glLoadIdentity()
        glTranslatef(self.x_coord, self.y_coord, self.z_coord)

        glBindTexture(GL_TEXTURE_2D, self.texhandle)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glNormalPointer(GL_FLOAT, 0, self.normals)
        glTexCoordPointer(2, GL_FLOAT, 0, self.tex_coords)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    def resize(self):
        if self.canvas:
            if self.canvas.size[0] < self.canvas.size[1]:
                self.z_coord = -18.0
            else:
                self.z_coord = -26.0
            self.x_max = self.canvas.size[0]
            self.y_max = self.canvas.size[1]
            if self.gl_initialized:
                self.init_view()

    def set_exit(self):
        self.exitflag = True

    def cleanup(self):
        appuifw.app.body = self.old_body
        self.canvas = None
        appuifw.app.exit_key_handler = None

    def run(self):
        appuifw.app.exit_key_handler = self.set_exit
        while not self.exitflag:
            self.canvas.drawNow()
            e32.ao_sleep(0.0001)
        self.cleanup()


if __name__ == '__main__':
    if not appuifw.touch_enabled():
        appuifw.note(u"This only works on touch devices")
    else:
        gl_ball = GlesBall()
        gl_ball.run()
