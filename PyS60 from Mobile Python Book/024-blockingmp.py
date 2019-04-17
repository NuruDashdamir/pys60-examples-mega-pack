
import audio, e32

snd_lock = e32.Ao_lock()

def sound_callback(prev_state, current_state, err):
     if current_state == audio.EOpen:
             snd_lock.signal()

def playMP3():
     mp3 = audio.Sound.open("E:\\Sounds\\mysound.mp3")
     mp3.play(callback = sound_callback)
     snd_lock.wait()
     mp3.close()
     print "PlayMP3 returns.."

playMP3()
