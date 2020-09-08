
import appuifw, audio, os

MENU = [u"Play sound", u"Record sound", u"Delete sound"]
SOUNDFILE = u"E:\\sound.wav"
sound = None

while True:
        index = appuifw.popup_menu(MENU, u"Select operation")
        if sound:
                sound.stop()
        sound = audio.Sound.open(SOUNDFILE)
        if index == 0:
                sound.play()
        elif index == 1:
                sound.record()
                appuifw.query(u"Press OK to stop recording", "query")
                sound.stop()
        elif index == 2:
                os.remove(SOUNDFILE)
        else:
                break
