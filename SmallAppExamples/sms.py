import appuifw, e32, messaging

#Define the body function

def txtss():

	app_lock=e32.Ao_lock()

 	def quit():

		app_lock.signal()

	appuifw.app.exit_key_handler=quit

	t=appuifw.Text()

 	appuifw.app.body=t

#To write text in unicode at the current position of the cursor:

 
	t.font=u"Nokia Hindi S6016b"

	appuifw.app.exit_key_handler=quit

	#To read the text that's on the screen:

	g=appuifw.query(u"type text","text",u" ")

	#To make the entire text that is displayed into your text:

t.set(g)

 	app_lock.wait()

	txt1=t.get() #Returns a unicode string

	nbr = []

	data = appuifw.query(u"Type your name:", "text")

	data1= appuifw.query(u"Type no. of contacts, mesage is to be 	sent:","number")

	for i in range(data1):

		nubr = "+91"+appuifw.query(u"type number:","text")

		nbr.append(nubr)

	txt = txt1 +data

	#txt=e.enc(txt2)

	if appuifw.query(u"Send message to your friends","query") == True:

    		for i in range(data1):

    			messaging.sms_send(nbr[i], txt)


    		appuifw.note(u"Messages sent", "conf")

	else:

    		appuifw.note(u"Well, your Messages are not sent then", "error")
