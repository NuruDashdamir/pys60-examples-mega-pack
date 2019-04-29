# This script lets 2 phones exchange a file via OBEX.
# This is the server, the corresponding client is obex_client.py
from socket import *
import appuifw

# Create a bluetooth socket in waiting state to be connected to
s = socket(AF_BT, SOCK_STREAM)
port = bt_rfcomm_get_available_server_channel(s)
print "Binding service to port %s"%port
s.bind(("", port))
print "Service bound."

# Advertise the OBEX service, so it can be seen by other phones
service_name=u"Test OBEX service"

print "Advertising service as %s"%repr(service_name)
bt_advertise_service(service_name, s, True, OBEX)

try: 
    print "Setting security to AUTH."
    set_security(s, AUTH)

    receive_path = u"c:\\obex.txt"
    print "Receiving file."
    bt_obex_receive(s, receive_path)
    print "File received."

    import e32
    e32.ao_sleep(1)
finally:
    print "Stopping service advertising."
    bt_advertise_service(service_name, s, False, OBEX)

print "Closing socket."
s.close()
print "Socket closed."
print "Finished."
