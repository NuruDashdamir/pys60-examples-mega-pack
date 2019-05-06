# Copyright (c) 2007 Jurgen Scheible
# connect phone to an external GPS reader via Bluetooth and read GPS data out

import appuifw, socket, e32

target = ''
# target = ('00:02:76:fd:c4:3a',1)    alternatively you can type here the Bluetooth address in HEX 
#                                     of your GPS reader. Then the phone connects directly to the GPS reader without
#                                     bringing up the BT device search dialog

def connectGPS():
    global sock, target
    # create a bluetooth socket and connect to GPS receiver:  (if it is a Nokia LD-3W the PIN is: 0000)
    try:
    	sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
    	if target == '':
            address,services = socket.bt_discover()
            print "Discovered: %s, %s"%(address, services)
            target = (address, services.values()[0])
        print "Connecting to " + str(target)
        sock.connect(target)
        appuifw.note(u"GPS successfully connected!", "info")
        print "connected!"
        readData()
    except:
        if appuifw.query(u"GPS device problem. Connect again to GPS?","query") == True:
            sock.close()
            connectGPS()
        else:
            sock.close()

def readData():
    global sock
    packet_received = 0
    print "reading ..."
    while(packet_received == 0):
        ch = sock.recv(1)
        # Loop until packet received
        buffer = ""
        while(ch !='\n'):
            buffer+=ch
            ch = sock.recv(1)

        if (buffer[0:6]=="$GPGGA"):
            gpsData = buffer.split(",")
            lat = gpsData[2]
            lon = gpsData[4]
            if lat == '' :
                pass
            else:
                packet_received = 1
                appuifw.note(u'Sucessful GPS location reading! ' + unicode(lat) + u' ' + unicode(lon), "info")
                print "reading done!"
                print "Press Options key!"
                sock.close()
        else:
            pass


def exit_key_handler():
    script_lock.signal()
    sock.close()

script_lock = e32.Ao_lock()

print "Press Options key!"

appuifw.app.title = u"BT GPS reader"
appuifw.app.menu = [(u"get GPS location", connectGPS)]
appuifw.app.exit_key_handler = exit_key_handler
script_lock.wait()