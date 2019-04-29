# Sound recording / playing script 

import appuifw
import e32
# import the audio module
import audio


# define a name of the file to be the sound file, incl. its full path
filename = 'c:\\boo.wav'

# define the recording part:
def recording():
    global S
    # open the sound file to be ready for recording and set an instance (S) of it
    S=audio.Sound.open(filename)
    # do the recording (has to be stopped by closing() function below)
    S.record()
    print "Recording on! To end it, select stop from menu!"

# define the playing part:
def playing():
    global S
    try:
        # open the sound file to be ready for playing by setting an instance (S) of it
        S=audio.Sound.open(filename)
        # play the sound file
        S.play()
        print "Playing"
    except:
        print "Record first a sound!"

# stopping of recording / playing and closing of the sound file
def closing():
    global S
    S.stop()
    S.close()
    print "Stopped"


def exit_key_handler():
    script_lock.signal()
    appuifw.app.set_exit()
    

script_lock = e32.Ao_lock()

appuifw.app.title = u"Sound recorder"

# define the application menu
appuifw.app.menu = [(u"play", playing),
                    (u"record", recording),
                    (u"stop", closing)]

appuifw.app.exit_key_handler = exit_key_handler
script_lock.wait()


 

