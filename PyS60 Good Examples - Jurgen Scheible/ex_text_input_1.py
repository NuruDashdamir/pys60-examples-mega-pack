# Copyright (c) 2005 Jurgen Scheible
# This script performs a query with a single-field dialog (text input field)
# and displays the users input as a pop-up note 


import appuifw

data = appuifw.query(u"Type a word:", "text")

appuifw.note(u"The typed word was: " + data, "info")




# NOTE: a text string must be defined as unicode
# u"..."
# The mobile can not diplay the text otherwise properly!

