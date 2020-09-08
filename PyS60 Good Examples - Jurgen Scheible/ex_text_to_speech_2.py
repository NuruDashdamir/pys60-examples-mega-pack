# Copyright (c) 2006 Jurgen Scheible
# This script waits for an incoming sms, reads its
# content and shows it inside a pop-up note
# NOTE: PyS60 version 1.3.14 or higher is needed to run this script.

import inbox
import e32
import audio

def read_sms(id):
    e32.ao_sleep(0.1)
    sms_text = i.content(id)
    audio.say(sms_text)
    
i=inbox.Inbox()
print "send now sms to this phone"
i.bind(read_sms)

