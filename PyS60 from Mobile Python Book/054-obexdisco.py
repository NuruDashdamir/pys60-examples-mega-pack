
import btsocket
address, services = btsocket.bt_obex_discover()
print "Chosen device:", address, services
