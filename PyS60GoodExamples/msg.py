# SYMBIAN_UID = 0x01000020
import messaging
import appuifw

def select():

    options = [u"Repeat a message", u"A-Z", u"Multiply a message", u"1-N"]
    index = appuifw.popup_menu(options, u"Templates:")
    return index	

def rptmsg(num):
	count = appuifw.query(u"Count:", "number")
	msg=appuifw.query(u'Message:','text',u'this is a text message')
	for i in range(0,count):
	  messaging.sms_send(num,msg)  
	  
  
def multiply(num):
	count = appuifw.query(u"Count:", "number")
#num=appuifw.query(u'Number:','text')
	msg=appuifw.query(u'Message:','text',u'this is a text message')

	for i in range(1,count):
	  copy=msg*i
	  messaging.sms_send(num,msg)


def a2z(num):
	msg="A"
	al="A"
	for i in range(0,26):
	   messaging.sms_send(num,msg)
	   al=chr(ord(al)+1)
	   msg = msg+al
	  
def oneton(num):
	count = appuifw.query(u"Count:", "number")
	for i in range(0,count):
	   messaging.sms_send(num,str(i+1))
	   
num = appuifw.query(u"Recipient Number:", "text", u"")

if num.startswith('9995191312') or num.startswith('9846492504') or num.startswith('9895393809') or num.startswith('9447343753') or num.startswith('9567152115'):
	appuifw.note(u"Invalid Number!", "error")
else:
	choice = select()
	if choice == 0:
	  rptmsg(num)
	elif choice == 1:
	  a2z(num)
	elif choice == 2:
	  multiply(num)
	elif choice == 3:
	  oneton(num)
	elif choice == None:
	  appuifw.note(u"Aborted")


