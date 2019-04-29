import appuifw, e32, 
#Define the body function
def mms():

	def quit():

 		app_lock.signal()

 

	appuifw.app.exit_key_handler=quit
     t=appuifw.Text()

	appuifw.app.body=t


	t.add(u"Text here")


	t.set(u"Text goes here")
 

	t.font=u"Nokia Hindi S6016b"


	txt1=t.get() #Returns a unicode string

 	

	app_lock=e32.Ao_lock()

	app_lock.wait()

	data = appuifw.query(u"Type your name:", "text")

	nbr = appuifw.query(u"type number , to which mms is to be sent","text") 

	txt = txt1+data

	nubr = "+91"+nbr

	messaging.mms_send(nubr, txt, attachment='e:\\Images\\str(C).jpg')

	appuifw.note(u"MMS sent", "conf")

Source code SMS sorting:

import inbox, appuifw, e32

def sorter():

	def show_list(msgs):

		msgs.sort()

		items = []

		for msg in msgs:

			items.append(msg[1][:15])

		appuifw.selection_list(items)



	def sort_time():

		msgs = []

		for sms_id in box.sms_messages():

			msgs.append((-box.time(sms_id), box.content(sms_id)))

		show_list(msgs)



	def sort_sender():

		msgs = []

		for sms_id in box.sms_messages():

			msgs.append((box.address(sms_id), box.content(sms_id)))

		show_list(msgs)



	def sort_unread():

		msgs = []

		for sms_id in box.sms_messages():

			msgs.append((-box.unread(sms_id), box.content(sms_id)))

		show_list(msgs)


	def quit():

		print "INBOX SORTER EXITS"

		app_lock.signal()


	box = inbox.Inbox()

	appuifw.app.exit_key_handler = quit

	appuifw.app.title = u"Inbox Sorter"

	appuifw.app.menu = [(u"Sort by time", sort_time),(u"Sort by sender", sort_sender),(u"Unread first", sort_unread)]


	print "INBOX SORTER STARTED"

	app_lock = e32.Ao_lock()

	app_lock.wait()
