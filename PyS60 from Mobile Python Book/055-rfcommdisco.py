
import btsocket
address, services = btsocket.bt_discover()
print "Chosen device:", address, services
