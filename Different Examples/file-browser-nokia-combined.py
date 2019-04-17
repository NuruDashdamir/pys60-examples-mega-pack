#
# filebrowser.py
#
# A very simple file browser script to demonstrate the power of Python
# on Series 60.
#      
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
#   

import os
import appuifw
import e32
import sys
import time

# utility module for filebrowser.
class Directory_iter:
    def __init__(self, drive_list):
        self.drives = [((i, u"Drive")) for i in drive_list]
        self.at_root = 1
        self.path = '\\'

    def pop(self):
        if os.path.splitdrive(self.path)[1] == '\\':
            self.path = '\\'
            self.at_root = 1
        else:
            self.path = os.path.split(self.path)[0]

    def add(self, i):
        if self.at_root:
            self.path = str(self.drives[i][0] + u'\\')
            self.at_root = 0
        else:
            self.path = os.path.join(self.path, os.listdir(self.name())[i])

    def name(self):
        return self.path

    def list_repr(self):
        if self.at_root:
            return self.drives
        else:

            def item_format(i):
                full_name = os.path.join(str(self.name()), i)
                try:
                    time_field = time.strftime("%d.%m.%Y %H:%M",\
                                 time.localtime(os.stat(full_name).st_mtime))
                    info_field = time_field + "  " + \
                                 str(os.stat(full_name).st_size) + "b"
                    if os.path.isdir(full_name):
                        name_field = "["+i+"]"
                    else:
                        name_field = i
                except:
                    info_field = "[inaccessible]"
                    name_field = "["+i+"]"
                return (unicode(name_field), unicode(info_field))
            try:
                l = map(item_format, os.listdir(self.name()))
            except:
                l = []
            return l

    def entry(self, i):
        return os.path.join(self.name(), os.listdir(self.name())[i])


# main class
class Filebrowser:
    def __init__(self):
        self.script_lock = e32.Ao_lock()
        self.dir_stack = []
        self.current_dir = Directory_iter(e32.drive_list())

    def run(self):
        from key_codes import EKeyLeftArrow
        entries = self.current_dir.list_repr()
        if not self.current_dir.at_root:
            entries.insert(0, (u"..", u""))
        self.lb = appuifw.Listbox(entries, self.lbox_observe)
        self.lb.bind(EKeyLeftArrow, lambda: self.lbox_observe(0))
        old_title = appuifw.app.title
        self.refresh()
        self.script_lock.wait()
        appuifw.app.title = old_title
        appuifw.app.body = None
        self.lb = None

    def refresh(self):
        appuifw.app.title = u"File browser"
        appuifw.app.menu = []
        appuifw.app.exit_key_handler = self.exit_key_handler
        appuifw.app.body = self.lb

    def do_exit(self):
        self.exit_key_handler()

    def exit_key_handler(self):
        appuifw.app.exit_key_handler = None
        self.script_lock.signal()

    def lbox_observe(self, ind = None):
        if not ind == None:
            index = ind
        else:
            index = self.lb.current()
        focused_item = 0

        if self.current_dir.at_root:
            self.dir_stack.append(index)
            self.current_dir.add(index)
        elif index == 0:                              # ".." selected
            focused_item = self.dir_stack.pop()
            self.current_dir.pop()
        elif os.path.isdir(self.current_dir.entry(index-1)):
            self.dir_stack.append(index)
            self.current_dir.add(index-1)
        else:
            item = self.current_dir.entry(index-1)
            if os.path.splitext(item)[1] == '.py':
                i = appuifw.popup_menu([u"execfile()", u"Delete"])
            else:
                i = appuifw.popup_menu([u"Open", u"Delete"])
            if i == 0:
                if os.path.splitext(item)[1].lower() == u'.py':
                    execfile(item, globals())
                    self.refresh()
                    #appuifw.Content_handler().open_standalone(item)
                else:
                    try:
                        appuifw.Content_handler().open(item)
                    except:
                        import sys
                        type, value = sys.exc_info() [:2]
                        appuifw.note(unicode(str(type)+'\n'+str(value)), "info")
                return
            elif i == 1:
                os.remove(item)
                focused_item = index - 1

        entries = self.current_dir.list_repr()
        if not self.current_dir.at_root:
            entries.insert(0, (u"..", u""))
        self.lb.set_list(entries, focused_item)

if __name__ == '__main__':
    Filebrowser().run()
