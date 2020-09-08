# Copyright (c) 2007 Jurgen Scheible
# this script lets you send an mms to another phone including text and an image

import appuifw
import messaging

data = appuifw.query(u"Type your name:", "text")
nbr = '12345'   # change this number
txt = u"Greetings from:" +data

messaging.mms_send(nbr, txt, attachment='e:\\Images\\picture1.jpg')
appuifw.note(u"Message sent", "info")



