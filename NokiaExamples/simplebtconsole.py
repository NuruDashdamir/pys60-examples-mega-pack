# Copyright (c) 2004 Nokia
# Programming example -- see license agreement for additional rights
# A simple interactive console over Bluetooth.

import socket

class socket_stdio:
    def __init__(self,sock):
        self.socket=sock
    def read(self,n=1):
        return self.socket.recv(n)
    def write(self,str):
        return self.socket.send(str.replace('\n','\r\n'))
    def readline(self,n=None):
        buffer=[]
        while 1:
            ch=self.read(1)
            if ch == '\n' or ch == '\r':   # return
                buffer.append('\n')
                self.write('\n')
                break
            if ch == '\177' or ch == '\010': # backspace
                self.write('\010 \010') # erase character from the screen
                del buffer[-1:] # and from the buffer
            else:
                self.write(ch)
                buffer.append(ch)
            if n and len(buffer)>=n:
                break
        return ''.join(buffer)
    def raw_input(self,prompt=""):
        self.write(prompt)
        return self.readline()
    def flush(self):
        pass

sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
# For quicker startup, enter here the address and port to connect to.
target='' #('00:20:e0:76:c3:52',1)
if not target:
    address,services=socket.bt_discover()
    print "Discovered: %s, %s"%(address,services)
    if len(services)>1:
        import appuifw
        choices=services.keys()
        choices.sort()
        choice=appuifw.popup_menu(
            [unicode(services[x])+": "+x for x in choices],u'Choose port:')
        target=(address,services[choices[choice]])
    else:
        target=(address,services.values()[0])        
print "Connecting to "+str(target)
sock.connect(target)
socketio=socket_stdio(sock)
realio=(sys.stdout,sys.stdin,sys.stderr)
(sys.stdout,sys.stdin,sys.stderr)=(socketio,socketio,socketio)
import code
try:
  code.interact()
finally:
  (sys.stdout,sys.stdin,sys.stderr)=realio
  sock.close()
