# This script executes a dialog that allows the users to make multiple selections
# of items in a list via checkbox. It returns the indexes (of the list) of the chosen items
# It uses the .multi_selection_list() function of the appuifw module
# appuifw.multi_selection_list(choices=list , style='checkbox', search_field=1)


# import the application user interface framework module
import appuifw

# define the list of items (items must written in unicode! -> put a u in front)
L = [u'cakewalk', u'com-port', u'computer', u'bluetooth', u'mobile', u'screen', u'camera', u'keys']

# create the multi-selection list
index = appuifw.multi_selection_list(L , style='checkbox', search_field=1)

# create a new list (Lnew) that inlcudes only the selected items and print the new list (Lnew)
Lnew = index
print Lnew
