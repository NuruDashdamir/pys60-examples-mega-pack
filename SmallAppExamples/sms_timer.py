#import the module inbox (that handles incoming sms things)

import inbox

#import the module e32

import e32

#import the module appuifw

import appuifw

#import the module messaging

import messaging

 

#set application title



def timon():

# Define exit function

	appuifw.app.title=u"SMS Timer"

 

	def exit_key_handler():

    		app_lock.signal()

	def run():
 

# define the list of items (items must written in unicode! -> put a u in front)

		L = [u'Set Timer',u'Exit']

 

# create the selection list

		index = appuifw.selection_list(choices=L , search_field=1)

 

#Trigger action upon index

 

		if index == 0:

			data = appuifw.query(u"Enter SMS text","text")

			number=appuifw.query(u"Enter recepient number","text")

			appuifw.note(u"Enter time to wait before sending !", "info")

			t=appuifw.query(u"Send after time (in mins) :","number")

			t=t*60

			while t>0:

				e32.ao_sleep(1)

				t=t-1

			messaging.sms_send(number, data)

			appuifw.note(u"Message sent!", "info")

			run() # Again call the main function

		if index == 1:

			exit_key_handler()

 

	#calls the main function

	run()

	app_lock = e32.Ao_lock()

 

	appuifw.app.exit_key_handler = exit_key_handler

	app_lock.wait()
