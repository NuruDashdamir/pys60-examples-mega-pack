# Copyright (c) 2006 Jurgen Scheible
# This script waits for an incoming sms, reads its
# content and shows it inside a pop-up note
# NOTE: PyS60 version 1.3.1 or higher is needed to run this script.

import inbox, e32, appuifw

def read_sms(id):
    e32.ao_sleep(0.1)
    i=inbox.Inbox()
    sms_text = i.content(id)    
    appuifw.note(u"sms content: " + sms_text , "info")
    
i=inbox.Inbox()
print "send now sms to this phone"
i.bind(read_sms)

