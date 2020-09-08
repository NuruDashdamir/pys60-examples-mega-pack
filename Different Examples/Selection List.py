# This script executes a dialog that allows the users to select
# an item in a list and returns the index (of the list) of the chosen item
# It uses the .selection_list() function of the appuifw module
# appuifw.selection_list(choices=list , search_field=0 or 1)


# import the application user interface framework module
import appuifw

# define the list of items (items must written in unicode! -> put a u in front)
L = [u'cakewalk', u'com-port', u'computer', u'bluetooth', u'mobile', u'screen', u'camera', u'keys']

# create the selection list
index = appuifw.selection_list(choices=L , search_field=1)

# use the result of the selection to trigger some action (here we just print something)
if index == 0:
    print "cakewalk was selected"
else:
    print "thanks for choosing"


# the search_field=1 (set to 1) enables a search functionality for looking
# up items in the list. IMPORTANT: to activate the find pane
# (search functionality) you need to press a keyboard key when the script
# is executed and the list has appeared on the screen.
# if search_field=0 no search functionality is enabled.