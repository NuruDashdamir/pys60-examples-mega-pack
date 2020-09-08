
import socket

ap_id = socket.select_access_point()
apo = socket.access_point(ap_id)
socket.set_default_access_point(apo)
