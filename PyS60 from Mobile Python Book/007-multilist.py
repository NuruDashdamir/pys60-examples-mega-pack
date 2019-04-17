
import appuifw

colors = [u"red", u"green", u"blue", u"brown"]

selections = appuifw.multi_selection_list(colors, 'checkbox', 1)
print "Checkbox selected:", selections

selections = appuifw.multi_selection_list(colors, 'checkmark', 1)
print "Checkmark selected:", selections

