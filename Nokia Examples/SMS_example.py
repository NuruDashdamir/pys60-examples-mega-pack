# SMS sending example application

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


import appuifw
import e32
# import messaging 

old_title = appuifw.app.title
appuifw.app.title = u"SMS sending"


class NumbersView:
    def __init__(self, SMS_multiviewApp):
        self.SMS_multiviewApp = SMS_multiviewApp
        self.dict = [(u"Jim", "55512345"), (u"Jane", "55567890")]
        self.names = [item[0] for item in self.dict]
        self.numbers = [item[1] for item in self.dict]

        self.numbers_list = appuifw.Listbox(self.names, self.handle_select)
        self.index = None
        appuifw.app.body = self.numbers_list

    def activate(self):
        appuifw.app.body = self.numbers_list
        appuifw.app.menu = [(u"Select", self.handle_select)]
        
    def handle_select(self):
        n = self.get_name()
        appuifw.note(u"Selected: "+ n, 'info')

    def get_current(self):
        return self.numbers_list.current()

    def get_name(self):
        i = self.get_current()
        return self.names[i]

    def get_number(self):
        i = self.get_current()
        return self.numbers[i]


class ChoiceView:
    def __init__(self, SMS_multiviewApp):
        self.SMS_multiviewApp = SMS_multiviewApp
        self.texts = [u"I am late",
                      u"What is for dinner?",
                      u"Do you need anything from the supermarket?", 
                      u"How about a round of golf after work?"]
        self.listbox = appuifw.Listbox(self.texts, self.handle_select)

    def activate(self):
        appuifw.app.body = self.listbox
        appuifw.app.menu = [(u"Select", self.handle_select),
                            (u"Send", self.handle_send)]
        
    def handle_select(self):
        i = self.listbox.current()
        appuifw.note(u"Selected: " + self.get_text(),'info')

    def handle_send(self):
        appuifw.app.activate_tab(3)
        self.SMS_multiviewApp.handle_tab(3)

    def get_text(self):
        return self.texts[self.listbox.current()]


class TextView:
    def __init__(self, SMS_multiviewApp):
        self.SMS_multiviewApp = SMS_multiviewApp
        self.view_text = appuifw.Text()

    def activate(self):
        t = self.SMS_multiviewApp.get_text()
        self.view_text.set(t)
        appuifw.app.body = self.view_text
        appuifw.app.menu = [(u"Send", self.handle_send)]
        self.view_text.focus = True

    def handle_send(self):
        appuifw.app.activate_tab(3)
        self.SMS_multiviewApp.handle_tab(3)


class SendView:
    def __init__(self, SMS_multiviewApp):
        self.SMS_multiviewApp = SMS_multiviewApp
        self.log_text = appuifw.Text()
        self.log_contents = u""
        
    def activate(self):
        self.log_text.set(self.log_contents)
        appuifw.app.body = self.log_text
        appuifw.app.menu = []
        nbr = self.SMS_multiviewApp.get_number()
        txt = self.SMS_multiviewApp.get_text()
        nam = self.SMS_multiviewApp.get_name()
        if appuifw.query(u"Send message to " + nam + "?", 'query'):
            t = u"Sent " + txt + " to " + nbr + " (" + nam + ")\n"
            self.log_contents += t
            self.log_text.add(t)
            # messaging.sms_send(nbr, txt)
    

class SMS_multiviewApp:
    def __init__(self):
        self.lock = e32.Ao_lock()
        appuifw.app.exit_key_handler = self.exit_key_handler
        
        self.n_view = NumbersView(self)
        self.c_view = ChoiceView(self)
        self.t_view = TextView(self)
        self.s_view = SendView(self)
        self.views = [self.n_view, self.c_view, self.t_view, self.s_view]
        appuifw.app.set_tabs([u"Numbers", u"Choice", u"Text", u"Send"],
                             self.handle_tab)
        
    def run(self):
        self.handle_tab(0)
        self.lock.wait()
        self.close()

    def get_name(self):
        return self.n_view.get_name()

    def get_number(self):
        return self.n_view.get_number()

    def get_text(self):
        return self.c_view.get_text()

    def handle_tab(self, index):
        self.views[index].activate()

    def exit_key_handler(self):
        self.lock.signal()

    def close(self):
        appuifw.app.exit_key_handler = None
        appuifw.app.set_tabs([u"Back to normal"], lambda x: None)
        del self.t_view
        del self.s_view

myApp = SMS_multiviewApp()
myApp.run()

appuifw.app.title = old_title
appuifw.menu = None
