# this file lets 2 phones exchange a file via OBEX
# this file is the client side
# the corresponding server side file is called obex_server.py

from socket import *
import appuifw
import e32

# JL: you don't need a socket for this!
## create socket
#s=socket(AF_BT,SOCK_STREAM)

# scan for other phones offering OBEX service
addr,services=bt_obex_discover()
print "Discovered: %s, %s"%(addr,services)
if len(services)>0:
    choices=services.keys()
    choices.sort()
    choice=appuifw.popup_menu([unicode(services[x])+": "+x
                               for x in choices],u'Choose port:')
    port=services[choices[choice]]
else:
    port=services[services.keys()[0]]
address=(addr,port)

# create file to be sent
send_path = u"c:\\test.txt"
f=open(send_path, 'w')
f.write("hello")
f.close() # NOTE: parens were missing here before!

# send file via OBEX
print "Sending file %s to host %s port %s"%(send_path, address[0], address[1])
bt_obex_send_file(address[0], address[1], send_path)
print "File sent."
