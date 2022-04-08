
import appuifw, socket, e32

ECHO = True

def choose_service(services):
        names = []
        channels = []
        for name, channel in services.items():
                names.append(name)
                channels.append(channel)
        index = appuifw.popup_menu(names, u"Choose service")
        return channels[index]

def read_and_echo(fd):
        buf = r = ""
        while r != "\n" and r != "\r":
                r = fd.read(1)
                if ECHO: fd.write(r)
                buf += r
        if ECHO: fd.write("\n")
        return buf

address, services = socket.bt_discover()
channel = choose_service(services)
conn = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
conn.connect((address, channel))
to_peer = conn.makefile("rw", 0)

while True:
        msg = appuifw.query(u"Send a message", "text")
        if msg:
                print >> to_peer, msg + "\r"
                print "Sending: " + msg
                print "Waiting for reply..."
                reply = read_and_echo(to_peer).strip()
                appuifw.note(unicode(reply), "info")
                if reply.find("bye!") != -1:
                        break
        else:
                break
to_peer.close()
conn.close()
print "bye!"
