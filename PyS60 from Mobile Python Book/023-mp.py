
import audio

sound = audio.Sound.open("E:\\Sounds\\mysound.mp3")

def playMP3():
     sound.play()
     print "PlayMP3 returns.."

playMP3()
