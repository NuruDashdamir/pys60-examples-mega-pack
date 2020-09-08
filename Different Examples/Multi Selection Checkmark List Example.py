# This script executes a dialog that allows the users to make multiple selections
# of items in a list and returns the indexes (of the list) of the chosen items
# It uses the .multi_selection_list() function of the appuifw module
# appuifw.multi_selection_list(choices=list , style='checkmark', search_field=0 or 1)


# import the application user interface framework module
import appuifw

# define the list of items (items must written in unicode! -> put a u in front)
L = [u'cakewalk', u'com-port', u'computer', u'bluetooth', u'mobile', u'screen', u'camera', u'keys']

# create the multi-selection list
tuple = appuifw.multi_selection_list(L , style='checkmark', search_field=1)

# create a new list (Lnew) that inlcudes only the selected items and print the new list (Lnew)
Lnew = tuple
print Lnew
print tuple 


# Note: if you set the style parameter to style='checkmark' like here, then you can put
# a mark behind the items by pressing the EDIT key once you have navigated to an item to
# make your selection.

# the search_field=1 (set to 1) enables a search functionality for looking
# up items in the list (applies only when style='checkmark').
# IMPORTANT: to activate the find pane
# (search functionality) you need to press a keyboard key when the script
# is executed and the list has appeared on the screen.
# if search_field=0 no search functionality is enabled.