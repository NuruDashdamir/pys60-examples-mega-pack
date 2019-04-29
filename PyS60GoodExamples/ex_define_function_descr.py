# defining a simple function


import appuifw

# a function is definded with: def nameoffunction():
# be aware of the indentation! (4 x spacebar)

def afunction():
    data = appuifw.query(u"Type a word:", "text")
    appuifw.note(u"The typed word was: " +data, "info")


# a function is called with its name and brackets behind it
afunction()       




