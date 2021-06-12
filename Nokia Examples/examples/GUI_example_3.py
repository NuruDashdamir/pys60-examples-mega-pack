# Advanced GUI example

# This nonfunctional sample code is based on a simple application for
# accessing a to-do list.  The details of that particular application
# have been edited out.
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


import e32
import appuifw

from MyDataAccess import MyDataAccess

e32.ao_yield()

def format(item):
    # Format the item as a short unicode string.
    return u""                          # omitted

class MyApp:
    def __init__(self):
        self.lock = e32.Ao_lock()

        self.old_title = appuifw.app.title
        appuifw.app.title = u"My Application"

        self.exit_flag = False
        appuifw.app.exit_key_handler = self.abort

        self.data = []
        appuifw.app.body = appuifw.Listbox([u"Loading..."], self.handle_modify)

        self.menu_add = (u"Add", self.handle_add)
        self.menu_del = (u"Delete", self.handle_delete)
        appuifw.app.menu = [] # First call to refresh() will fill in the menu.

    def connect(self, host):
        self.db = MyDataAccess(host)
        self.db.listen(self.notify) # Set up callback for change notifications.

    def loop(self):
        try:
            self.lock.wait()
            while not self.exit_flag:
                self.refresh()
                self.lock.wait()
        finally:
            self.db.close()

    def close(self):
        appuifw.app.menu = []
        appuifw.app.body = None
        appuifw.app.exit_key_handler = None
        appuifw.app.title = self.old_title

    def abort(self):
        # Exit-key handler.
        self.exit_flag = True
        self.lock.signal()

    def notify(self, in_sync):
        # Handler for database change notifications.
        if in_sync:
            self.lock.signal()

    def refresh(self):
        # Note selected item.
        current_item = self.get_current_item()

        # Get updated data.
        self.data = self.db.get_data()

        if not self.data:
            content = [u"(Empty)"]
        else:
            content = [format(item) for item in self.data]

        if current_item in self.data:
            # Update the displayed data, retaining the previous selection.
            index = self.data.index(current_item)
            appuifw.app.body.set_list(content, index)
        else:
            # Previously selected item is no longer present, so allow
            # the selection to be reset.
            appuifw.app.body.set_list(content)

        if not self.data:
            appuifw.app.menu = [self.menu_add]
        else:
            appuifw.app.menu = [self.menu_add, self.menu_del]

    def handle_modify(self):
        item = self.get_current_item()
        if item is not None:
            # Display data in Form for user to edit.
            # Save modified record in database.
            pass                        # omitted

    def handle_add(self):
        new_item = self.edit_item(ToDoItem())
        if new_item is not None:
            # User enters new data into Form.
            # Save new record in database.
            pass                        # omitted

    def handle_delete(self):
        item = self.get_current_item()
        if item is not None:
            # Remove record from database.
            pass                        # omitted

    def get_current_item(self):
        # Return currently selected item, or None if the list is empty.
        if not self.data:
            return None
        else:
            current = appuifw.app.body.current()
            return self.data[current]

def main():
    app = MyApp()
    try:
        hosts = [u"some.foo.com", u"other.foo.com"]
        i = appuifw.popup_menu(hosts, u"Select server:")
        if i is not None:
            app.connect(hosts[i])
            app.loop()
    finally:
        app.close()

if __name__ == "__main__":
    main()
