# Copyright (c) 2006 Jurgen Scheible
# This script waits for an incoming sms, reads its
# content and shows it inside a pop-up note
# NOTE: PyS60 version 1.3.14 or higher is needed to run this script.

import inbox
import e32
import audio

#create a function that does the reading of the content of the sms 
def read_sms(id):
    e32.ao_sleep(0.1)
    # read the content out of the message that has just arrived
    sms_text = i.content(id)
    # the phone speaks out the text that just arrived by sms (you can hear it through the loudspeakers of your phone)
    audio.say(sms_text)

# create an instance of the inbox() class     
i=inbox.Inbox()
print "send now sms to this phone"
# put the phone into waiting stage to wait for an incoming message
i.bind(read_sms)

