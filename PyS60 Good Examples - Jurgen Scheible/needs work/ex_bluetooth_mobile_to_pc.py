# script that connects to the serial port of the PC
# and lets you send characters to the PC

import appuifw
import socket
import e32


def bt_connect():
    global sock
    sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
    target=''
    if not target:
        address,services=socket.bt_discover()
        print "Discovered: %s, %s"%(address,services)
        if len(services)>1:
            import appuifw
            choices=services.keys()
            choices.sort()
            choice=appuifw.popup_menu([unicode(services[x])+": "+x
                                        for x in choices],u'Choose port:')
            target=(address,services[choices[choice]])
        else:
            target=(address,services.values()[0])
    print "Connecting to "+str(target)
    sock.connect(target)
    print "OK."

    bt_typetext()
        

def bt_typetext():
    global sock
    test = appuifw.query(u"Type words", "text", u"")
    if test == None:
        exit_key_handler()
    else:
        sock.send(test)
        bt_typetext()

def exit_key_handler():
    script_lock.signal()
    appuifw.app.set_exit()

appuifw.app.title = u"bt mob to PC"

script_lock = e32.Ao_lock()

appuifw.app.exit_key_handler = exit_key_handler()

bt_connect()

script_lock.wait()


