
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.0.2", 9000))
out = sock.makefile("rw", 0)
print >> out, "Hi! I'm the TCP client"
out.close()
print "Client ok"
