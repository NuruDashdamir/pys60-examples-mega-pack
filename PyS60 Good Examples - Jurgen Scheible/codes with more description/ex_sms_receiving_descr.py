# Copyright (c) 2006 Jurgen Scheible
# This script waits for an incoming sms, reads its
# content and shows it inside a pop-up note
# NOTE: PyS60 version 1.3.1 or higher is needed to run this script.

#import the module inbox (that handles incoming sms things)
import inbox
import e32

#create a function that does the content sms reading
def read_sms(id):
    e32.ao_sleep(0.1)       
    # create once more an instance of the inbox() class
    i=inbox.Inbox()
    # read the content out of the message that has just arrived
    sms_text = i.content(id) 
    # display the content inside a pop-up note    
    appuifw.note(u"sms content: " + sms_text , "info") 

# create an instance of the inbox() class    
i=inbox.Inbox()
print "send now sms to this phone"
# put the phone into waiting stage to wait for an incoming message
i.bind(read_sms)

