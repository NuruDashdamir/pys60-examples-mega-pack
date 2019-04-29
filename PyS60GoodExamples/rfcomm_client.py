# this file lets 2 phones exchange data via RFCOMM
# this file is the client side
# the corresponding server side file is called rfcomm_server.py

import socket
import appuifw
import e32

class BTReader:
    def connect(self):
        self.sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
        addr,services=socket.bt_discover()
        print "Discovered: %s, %s"%(addr,services)
        if len(services)>0:
            import appuifw
            choices=services.keys()
            choices.sort()
            choice=appuifw.popup_menu([unicode(services[x])+": "+x
                                       for x in choices],u'Choose port:')
            port=services[choices[choice]]
        else:
            port=services[services.keys()[0]]
        address=(addr,port)
        print "Connecting to "+str(address)+"...",
        self.sock.connect(address)
        print "OK." 
    def readline(self):
        line=[]
        while 1:
            ch=self.sock.recv(1)
            if(ch=='\n'):
                break
            line.append(ch)
        return ''.join(line)
    def close(self):
        self.sock.close()

bt=BTReader()
bt.connect()
print "Received: "+bt.readline()
bt.close()

