'''
Multi-Selection List Test

Copyright (c) 2009 Jouni Miettunen
http://jouni.miettunen.googlepages.com/

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

1.10 2009-04-15 Simpler code to update custom listbox selection
1.00 2009-03-31 First release
'''

VERSION = u'1.10'

import e32
import appuifw
import key_codes

### keypress handler trick
import time
g_time = 0
my_timer = e32.Ao_timer()

# Application main body, appuifw.Text()
g_t = None

# List items for all listboxes
my_list = [u"One", u"Two", u"Three", u"Four", u"Five", u"Six"]

# Custom listbox related items, global or within class
lb3 = None       # Listbox
e3 = []          # Entries: list items with icons
my_items = ()    # Save selections for next time
icon_on = None   # Icon for selected checkbox
icon_off = None  # Icon for non-selected checkbox

# Listbox icons, use built-in graphics
# See inside C:\Symbian\9.2\S60_3rd_FP1\Epoc32\include\avkonicons.hrh
# AVKON_ICON_FILE = u"z:\\resource\\apps\\avkon2.mbm"

# Listbox 1
# - Perfect, except cannot initialize selections
# - Search field works great

def menu_list1():
    ''' Built-in multi-selection listbox '''
    items = appuifw.multi_selection_list(my_list, style='checkbox', search_field=1)
    # Show what happened
    appuifw.note(u"Selected: %s" % unicode(str(items)))

# Listbox 2
# - Nice, use shift + scrolling to select several items

def menu_list2():
    ''' Built-in multi-selection listbox '''
    items = appuifw.multi_selection_list(my_list, style='checkmark')
    # Show what happened
    appuifw.note(u"Selected: %s" % unicode(str(items)))

# Listbox custom, lots of work
# - Checkbox icon for listbox (get_checkbox)
# - Handle selection on listbox (cb_select)
# - Handle closing listbox (cb_return)
# - Initialize and draw listbox (menu_list3)
# - Missing search field

def get_checkbox(a_value):
    ''' Checkbox icon: selected or not '''
    global icon_on, icon_off
    # Create only once, reuse after that
    if not icon_on:
        # See avkon2.mbm content (old version)
        # http://alindh.iki.fi/symbian/avkon2.mbm/

        try:
            # webkit checkbox looks better, but might not exist
            icon_off = appuifw.Icon(u"z:\\resource\\apps\\webkit.mbm", 12, 31)
            icon_on = appuifw.Icon(u"z:\\resource\\apps\\webkit.mbm", 13, 32)
        except:
            # Counting on avkon2 to be there, hopefully with checkbox
            icon_off = appuifw.Icon(u"z:\\resource\\apps\\avkon2.mbm", 103, 104)
            icon_on = appuifw.Icon(u"z:\\resource\\apps\\avkon2.mbm", 109, 110)

    if a_value:
        return icon_on
    else:
        return icon_off

def cb_select():
    ''' Callback for listbox item selection event '''

    ### keypress handler trick, to allow Enter/Select work
    global g_time
    my_timer.cancel()
    # Ignore first and non-timer trickered events
    if (not g_time) or (time.clock() - g_time < 0.1):
        g_time = time.clock()
        # Should be more than start keyrepeat rate
        my_timer.after(0.15, cb_select)
        return
    g_time = 0
    ### keypress handler trick, done

    # Current listbox selection
    index = lb3.current()

    # Change selected item icon: on <-> off
    if e3[index][1] == icon_on:
        new_icon = icon_off
    else:
        new_icon = icon_on

    e3[index] = (e3[index][0], new_icon)

    # Show new list, same item selected
    lb3.set_list(e3, index)
    appuifw.app.body = lb3

    # Make it visible
    e32.ao_yield()

def cb_return():
    ''' Closing listbox, clean up and bring back main view '''
    # Restore Main view
    global appuifw
    appuifw.app.body = g_t
    appuifw.app.menu = self_options[0]
    appuifw.app.exit_key_handler = cb_quit

    # Save selections from listbox
    global my_items
    my_items = ()
    for index in range(len(e3)):
        if e3[index][1] == icon_on:
            my_items += (index, )

    # Show what happened
    appuifw.note(u"Selected: %s" % unicode(str(my_items)))

def menu_list3():
    ''' Custom multi-selection listbox '''
    global e3, lb3
    e3 = []

    # Mark initial selections
    for item in range(len(my_list)):
        if item in my_items:
            icon = get_checkbox(True)
        else:
            icon = get_checkbox(False)
        e3.append((my_list[item], icon))

    global appuifw
    lb3 = appuifw.Listbox(e3, cb_select)
    appuifw.app.body = lb3
    appuifw.app.menu = self_options[1]
    appuifw.app.exit_key_handler = cb_return

    # Several ways to select item
    # BUG: One press of Enter/Select gives two events: KeyDown and KeyUp
    # BUG: ...or even 3+ with key repeat
    # Fix: write own key handler, react only on KeyUp event
    # Fix: use timer to separate "one" key press
    lb3.bind(key_codes.EKeyRightArrow, cb_select)
    lb3.bind(key_codes.EKeyEnter, cb_select)
    lb3.bind(key_codes.EKeySelect, cb_select)

def menu_about():
    ''' Callback for menu item About '''
    appuifw.note(u'Multi-selection List Test v' + VERSION + u'\n' +\
        u'jouni.miettunen.googlepages.com\n\u00a92009 Jouni Miettunen')

def cb_quit():
    ''' Cleanup before exit '''
    # ALWAYS cancel your timers before exit.
    my_timer.cancel()

    # User might NOT have initialized lb3 in custom listbox
    # Crash when unbinding non-binded keys
    global e3, lb3, icon_on, icon_off
    try:
        lb3.bind(key_codes.EKeyRightArrow, None)
        lb3.bind(key_codes.EKeyEnter, None)
        lb3.bind(key_codes.EKeySelect, None)
    except:
        pass

    # Help system clean-up, delete stuff by yourself
    e3 = []
    del lb3
    del icon_on
    del icon_off

    # Done, continue exit
    app_lock.signal()

# Initialize application UI
self_options = [
    [
        (u"Checkbox", menu_list1),
        (u"Checkmark", menu_list2),
        (u"Custom", menu_list3),
        (u"About", menu_about),
        (u"Exit", cb_quit)
    ],
    [
        (u"Change", cb_select),
        (u"Back", cb_return)
    ]
    ]

# Hox: no need to fix as portrait screen
# Supports automatic screen rotation as-is (N82)
appuifw.app.title = u'Multi-selection List Test'
appuifw.app.exit_key_handler = cb_quit
appuifw.app.menu = self_options[0]

# Create UI control and initilize instructions
g_t = appuifw.Text()
g_t.style = appuifw.STYLE_BOLD
g_t.add(u"Select listbox from Options menu:\n\n")
g_t.add(u"Checkbox: ")
g_t.style = 0
g_t.add(u"built-in listbox, looks nice, cannot initialize selections\n")
g_t.style = appuifw.STYLE_BOLD
g_t.add(u"Checkmark:")
g_t.style = 0
g_t.add(u"built-in listbox, cannot initialize selections\n")
g_t.style = appuifw.STYLE_BOLD
g_t.add(u"Custom: ")
g_t.style = 0
g_t.add(u"Looks plain, can initialize selections!\n")

# Show to user
appuifw.app.body = g_t

# Wait for user to do anything
app_lock = e32.Ao_lock()
app_lock.wait()
