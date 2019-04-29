# this file lets 2 phones exchange data via RFCOMM
# this file is the server side
# the corresponding client side file is called rfcomm_client.py

from socket import *
import appuifw

server_socket = socket(AF_BT, SOCK_STREAM)
p = bt_rfcomm_get_available_server_channel(server_socket)
server_socket.bind(("", p))
print "bind done"
server_socket.listen(1)
bt_advertise_service( u"jurgen", server_socket, True, RFCOMM)
set_security(server_socket, AUTH)
print "I am listening"

# Note: Don't call .send or .recv on the server_socket!
# Use the sock object returned by server_socket.accept().
(sock,peer_addr) = server_socket.accept()
print "Connection from %s"%peer_addr
test = appuifw.query(u"Type words", "text", u"")
sock.send(test+'\n')
print "sending done"
import e32
# Allow time for data to be sent to work around a bug in the socket
# module.
e32.ao_sleep(1)
sock.close()
