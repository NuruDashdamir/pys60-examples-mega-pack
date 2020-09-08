
import appuifw

names = appuifw.multi_query(u"First name:", u" Last name:")
if names: 
        first, last = names
        appuifw.note(u"Your full name is: " + first + " " + last)
else:
        appuifw.note(u"Cancel!")
