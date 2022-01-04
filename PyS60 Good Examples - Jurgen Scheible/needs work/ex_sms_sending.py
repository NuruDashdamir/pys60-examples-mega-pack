# Copyright (c) 2005 Jurgen Scheible
# this script lets you send an sms to 2 users at the same time

import appuifw
import messaging

data = appuifw.query(u"Type your name:", "text")

nbr1 = "123456" # change the mobile number here
nbr2 = "234567" # change the mobile number here
txt = u"Greetings from:" +data

if appuifw.query(u"Send message to your 2 friends","query") == True:
    messaging.sms_send(nbr1, txt)
    messaging.sms_send(nbr2, txt)

    appuifw.note(u"Messages sent", "info")
else:
    appuifw.note(u"Well, your Messages are not sent then", "info")


