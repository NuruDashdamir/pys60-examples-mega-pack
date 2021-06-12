# Simple GUI example
# Copyright (c) 2005 Nokia Corporation
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


import socket
import urllib

import e32
import appuifw

# List of triplets "Name", "URL", "extension"
choices=[(u"US Graphical Forecast", "http://weather.gov/forecasts/graphical/images/thumbnail/Thumbnail_Wx4_conus.png", "png"),
         (u"US Radar Image", "http://weather.gov/mdl/radar/rcm1pix_b.gif", "gif"),
         (u"US Satellite Image", "http://weather.gov/satellite_images/national.jpg", "jpg") ]
tempfile_without_extension = "c:\\weather"

old_title = appuifw.app.title
appuifw.app.title = u"Weather forecast"

L = [ x[0] for x in choices ]
index = appuifw.popup_menu(L, u"Select picture")

if index is not None:
    url = choices[index][1]
    ext = choices[index][2]
    tempfile = tempfile_without_extension + "." + ext

    try:
        print "Retrieving information..."
        urllib.urlretrieve(url, tempfile)
        lock=e32.Ao_lock()
        content_handler = appuifw.Content_handler(lock.signal)
        content_handler.open(tempfile)
        # Wait for the user to exit the image viewer.
        lock.wait()
        print "Image viewer finished."
    except IOError:
        print "Could not fetch the image."
    except:
        print "Could not open data received."
        
appuifw.app.title = old_title
