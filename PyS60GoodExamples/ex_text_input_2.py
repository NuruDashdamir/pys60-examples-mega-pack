
import appuifw


data1 = appuifw.query(u"Type your first name:", "text")

appuifw.note(u"Your first name is: " + data1, "info")

data2 = appuifw.query(u"Type your surname:", "text")

appuifw.note(u"Your surname is: " + data2, "info")

appuifw.note(u"Your full name is: " + data1 +u" " + data2, "info")

