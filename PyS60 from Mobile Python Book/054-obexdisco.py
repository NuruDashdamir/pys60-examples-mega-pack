
import socket
address, services = socket.bt_obex_discover()
print "Chosen device:", address, services
