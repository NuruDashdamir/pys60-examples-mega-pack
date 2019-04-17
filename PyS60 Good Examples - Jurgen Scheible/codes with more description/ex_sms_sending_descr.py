# Copyright (c) 2005 Jurgen Scheible
# this script lets you send an sms to 2 users at the same time.


# import the messaging module
import appuifw
import messaging

# create text input field
data = appuifw.query(u"Type your name:", "text")

# define the mobile numbers here
nbr1 = "123456" 
nbr2 = "234567"

# define the text that the sms shall contain
txt = u"Greetings from:" +data

# create a query with type: "query" -> appuifw.query(label, type)
# by using an if statement one can check whether the user has pressed "ok" -> True or "cancel" -> False
if appuifw.query(u"Send message to your 2 friends","query") == True:
    # send out the sms; include the mobile number and the text to be sent
    messaging.sms_send(nbr1, txt)
    messaging.sms_send(nbr2, txt)
    
    # confirm with a pop-up note that the sms has been sent out
    appuifw.note(u"Messages sent", "info")
else:
    # in case the user had pressed "cancel", send a pop-up note that the messages have not been sent out
    appuifw.note(u"Well, your Messages are not sent then", "info")


