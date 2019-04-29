def enc(t):

	f=""

	k=0

	l=len(t)

	for i in range(0,l):

	

		h = ord(t[i])

 		k=k+1

		if(k%2==0):

			f = f+hex(h)

		else:

			f = f+oct(h)

	return f

#message sending is similar to  6.2.1.1
