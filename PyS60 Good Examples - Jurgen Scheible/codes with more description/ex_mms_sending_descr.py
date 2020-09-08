# Copyright (c) 2007 Jurgen Scheible
# this script lets you send an mms to another phone including text and an image

import appuifw
import messaging

# create text input field
data = appuifw.query(u"Type your name:", "text")

# define the mobile number here where to send the MMS
nbr = "123456" # change the mobile number here

# define the text that the sms shall contain
txt = u"Greetings from:" +data


# image attachment: You must have an picture already available with the name picture1.jpg
# inside the folder called Images on your memory card. ('e:\\Images\\picture1.jpg') 
# otherwise the script won't work. (use video or sound file instead of image)

# send out the mms; include the mobile number, the text and the attachement to be sent
messaging.mms_send(nbr, txt, attachment='e:\\Images\\picture1.jpg')

# confirm with a pop-up note that the sms has been sent out
appuifw.note(u"MMS sent", "info")



