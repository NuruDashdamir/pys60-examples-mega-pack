# Copyright (c) 2008 Nokia Corporation
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

import e32
import appuifw
import camera
import key_codes

def viewfinder_cb(img):
    appuifw.app.body.blit(img)

def capture_cb():
    global photo
    photo=camera.take_photo()
    camera.stop_finder()
    lock.signal()

old_body=appuifw.app.body
appuifw.app.body=appuifw.Canvas()
lock=e32.Ao_lock()
photo=None
camera.start_finder(viewfinder_cb)
appuifw.app.body.bind(key_codes.EKeySelect, capture_cb)
lock.wait()
appuifw.app.body=old_body

filename=u'c:\\photo.jpg'
photo.save(filename)
print "Photo taken and saved at:",filename
