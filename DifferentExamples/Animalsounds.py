
import appuifw, audio

animals = [u'dog', u'cat', u'cow']

def record_animal_sounds():
    for animal in animals:
        noise = audio.Sound.open('e:\\' + animal + '.wav')
        if appuifw.query(u"Record sound of a " + animal, "query"):
            noise.record()
            appuifw.query(u"Press OK to stop recording", "query")
            noise.stop()
            noise.close()

def select_sound():
    global funny_noise
    funny_noise = None
    while True:
        index = appuifw.popup_menu(animals, u"Select sound:")
        if funny_noise:
            funny_noise.stop()
        if index == None:
            break
        else:
            play_animal_sound(u'e:\\' + animals[index] + '.wav')

def play_animal_sound(soundfile):
    global funny_noise
    funny_noise = audio.Sound.open(soundfile)
    funny_noise.play()
    
record_animal_sounds()
select_sound()
