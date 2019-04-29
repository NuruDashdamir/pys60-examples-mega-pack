# this file lets your PC read from a TCP/IP socket to which a phone has been connected to.
# this file is the PC server 
# the corresponding client file on the phone is called tcp_phone_client.py


import socket

HOST = ''                 # Symbolic name meaning the local host
PORT = 12008              # Arbitrary non-privileged port
print "define the socket"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "bind the socket"
s.bind((HOST, PORT))
s.listen(1)
print "waiting of the client to connect"
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.send(data)
conn.close()