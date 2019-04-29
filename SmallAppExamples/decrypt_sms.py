import inbox,appuifw

def decc():

	box=inbox.Inbox()

	m=box.sms_messages()

	l=box.content(m[0])

	#print l

	f=len(l)

	k=0

	d=0

	x=""

	for i in range(0,f,4):

	

		g=l[i:i+4]	

		d=int(g,0)	

		q=chr(d)

		x = x+q

	appuifw.note(unicode(x),"info")
