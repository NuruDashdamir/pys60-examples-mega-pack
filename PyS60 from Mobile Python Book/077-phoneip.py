
import socket
ap_id = socket.select_access_point()
apo = socket.access_point(ap_id)
apo.start()
print "PHONE IP IS", apo.ip()
