
import btsocket

address, services = btsocket.bt_discover()
print "Discovered: %s, %s" % (address, services)
target = (address, services.values()[0])

conn = btsocket.socket(btsocket.AF_BT, btsocket.SOCK_STREAM)
conn.connect(target)
to_gps = conn.makefile("r", 0)

while True:
        msg = to_gps.readline()
        if msg.startswith("$GPGGA"):
                gps_data = msg.split(",")
                lat = gps_data[2]
                lon = gps_data[4]
                break

to_gps.close()
conn.close()
print "You are now at latitude %s and longitude %s" % (lat, lon)
