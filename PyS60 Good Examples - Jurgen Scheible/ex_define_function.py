# defining a function


import appuifw


def afunction():
    data = appuifw.query(u"Type a word:", "text")
    appuifw.note(u"The typed word was: " +data, "info")


afunction()       




