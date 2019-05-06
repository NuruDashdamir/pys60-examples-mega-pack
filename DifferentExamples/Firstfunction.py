
import appuifw

def askword():
     word = appuifw.query(u"Type a word", "text")
     appuifw.note(u"The word was: " + str(word))

askword()
askword()
