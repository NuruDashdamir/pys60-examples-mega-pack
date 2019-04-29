# Application skeleton with main loop (while loop)


import appuifw
import e32


appuifw.app.screen='large'


# create your application logic ...


running=1

def quit():
    global running
    running=0
    
app.exit_key_handler=quit

appuifw.app.title = u"drawing"

appuifw.app.body= ...


while running:
    # handle_redraw(())
    e32.ao_sleep(0.5)





""" description:

# 1. import all modules needed
import appuifw
import e32

# 2. set the screen size to large
appuifw.app.screen='large'



# 3. create your application logic ...
# e.g. create all your definitions (functions) or classes and build instances of them or call them etc.
# ...... application logic ....

running=1



# 4. no application menu here neccessary

# 5. create and set an exit key handler: when exit ley is pressed, the main loop stops going (because the variable running will be put to 0=
def quit():
    global running
    running=0
    
app.exit_key_handler=quit

# 6. set the application title
appuifw.app.title = u"drawing"

# 7. no active objects needed

# 8. set the application body 
appuifw.app.body= ...

# 9. create a main loop (e.g. redraw the the screen again and again)
while running:
    # #put here things that need to be run through again and again
    # #e.g. redraw the screen:
    # handle_redraw(())
    # yield needs to be here e.g. in order that key pressings can be noticed
    e32.ao_yield()


"""







        


 



