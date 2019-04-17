
import appuifw

colors = [u"red", u"green", u"blue", u"brown"]

index = appuifw.selection_list(colors, 1)
if index == 2:
    print "blue is correct!"
else:
    print "Bzz! " + colors[index] + " is not correct"
