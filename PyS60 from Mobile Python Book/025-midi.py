
import audio

midi = audio.Sound.open("E:\\Sounds\\mysound.mid")

def playMIDI():
     midi.play()
     print "PlayMIDI returns.."

playMIDI()
