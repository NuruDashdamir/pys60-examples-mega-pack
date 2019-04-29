# this script lets you read the content of the image directory
# and displays the results in a selection list (UI)

import appuifw
import e32
import os

# drefine the directory to read
imagedir=u'c:\\nokia\images'

# read the directory
files=map(unicode,os.listdir(imagedir))

# put the found items of the directory in to a selction list for showing them on the screen
index=appuifw.selection_list(files)

# show the slected item 
print files[index]