
import socket
address, services = socket.bt_discover()
print "Chosen device:", address, services
