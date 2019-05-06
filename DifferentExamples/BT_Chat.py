
import socket, appuifw

def chat_server():
    server = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
    channel = socket.bt_rfcomm_get_available_server_channel(server)
    server.bind(("", channel))
    server.listen(1)
    socket.bt_advertise_service(u"btchat", server, True, socket.RFCOMM)
    socket.set_security(server, socket.AUTH | socket.AUTHOR)
    print "Waiting for clients..."
    conn, client_addr = server.accept()
    print "Client connected!"
    talk(conn, None)

def chat_client():
    conn = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
    address, services = socket.bt_discover()
    if 'btchat' in services:
        channel = services[u'btchat']
        conn.connect((address, channel))
        print "Connected to server!"
        talk(None, conn)
    else:
        appuifw.note(u"Target is not running a btchat server",
                "error")


def receive_msg(fd):
        print "Waiting for message.."
        reply = fd.readline()
        print "Received: " + reply
        appuifw.note(unicode(reply), "info")

def send_msg(fd):
        msg = appuifw.query(u"Send a message:", "text")
        print "Sending: " + msg
        print >> fd, msg

def talk(client, server):
        try:
                if server:
                        fd = server.makefile("rw", 0)
                        receive_msg(fd)
                if client:
                        fd = client.makefile("rw", 0)
                while True:
                        send_msg(fd)
                        receive_msg(fd)
        except:
                appuifw.note(u"Connection lost", "info")
                if client: client.close()
                if server: server.close()
                print "Bye!"

index = appuifw.popup_menu([u"New server", u"Connect to server"], 
                            u"BTChat mode")
if index != None:
        if index:
                chat_client()
        else:
                chat_server()
