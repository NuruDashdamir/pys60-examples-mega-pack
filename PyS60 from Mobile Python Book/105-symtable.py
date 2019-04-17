
import appuifw

def bark():
    appuifw.note(u"Ruff ruff!")

def sing():
    appuifw.note(u"Tralala") 

func_name = appuifw.query(u"What shall I do?", "text")
func = globals()[func_name]
print globals()
func()
