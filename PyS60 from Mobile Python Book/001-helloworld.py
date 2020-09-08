
import appuifw

data = appuifw.query(u"Type a word:", "text")
appuifw.note(u"The typed word was: " + str(data), "info")
