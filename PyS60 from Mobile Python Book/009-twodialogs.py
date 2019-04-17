
import appuifw

word = appuifw.query(u"Type your name", "text")
appuifw.note(u"Greetings from " + str(word))
