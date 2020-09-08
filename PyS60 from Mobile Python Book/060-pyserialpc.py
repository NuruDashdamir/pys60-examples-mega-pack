
import serial, sys, random

if sys.platform.find("win") != -1:
        PORT = 0
elif sys.platform.find("linux") != -1:
        PORT = "/dev/rfcomm0"
elif sys.platform.find("darwin") != -1:
        PORT = "/dev/tty.pybook"

num = random.randint(1, 10)

serial = serial.Serial(PORT)
print "Waiting for message..."
while True:
        msg = serial.readline().strip()
        guess = int(msg)
        print "Guess: %d" % guess
        if guess > num:
                print >> serial, "My number is smaller"
        elif guess < num:
                print >> serial, "My number is larger"
        else:
                print >> serial, "Correct! bye!"
                break
