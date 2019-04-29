# this file lets your phone connect to a TCP/IP socket
# this file is the phone client 
# the corresponding server side file on the net is called tcp_pc_server.py

import socket

HOST = '217.30.180.11'    # The remote host
PORT = 12008              # The same port as used by the server
print "define socket"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "trying to connect to socket"
s.connect((HOST, PORT))
print "connected"
s.send('Hello, world')
print "data send"
data = s.recv(1024)
s.close()
print 'Received', `data`