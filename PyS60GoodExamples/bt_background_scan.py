# install first the following files to your phone
# (they will install automatically the needed libraries for the script below):
# aosocket-series60_v20.sis, pdis.sis
# found at: http://pdis.hiit.fi/pdis/download/pdis/

# this script was found from forum.nokia.com

import e32
import appuifw
import aosocketnativenew
from pdis.lib.logging import *
import httplib, urllib

init_logging(FileLogger("c:\\bt_probing.txt"))

def tell(string):
    logwrite(string)
    if e32.is_ui_thread():
        print string
        e32.ao_yield()

# ----------------------------------
from aosocket.symbian.bt_device_discoverer import *
from socket import * # for obex file send

def discovered(error, devices, cb_param):
    if error == 0:
       #tell("devices: " + str(devices))
        tell(" ")
        for address, name in devices:      
            tell("Found: " + address + " | " + name)
      
        for address, name in devices:
                tell(" ")
                try:
                    address2, services = bt_discover(address)	#find services and port number                    
                    tell("Probing: " + address + " | " + name)
                    tell("RFCOMM Services: ")
                    tell(services)
                    tell(services.values()[0]) # port number of first RFCOMM service found
                    tell(" ")
                except:
                    pass
                    #tell("ooooops with " + name)
                    #log_exception()
                    
        for address, name in devices:
                try:
                    address3, services2 = bt_obex_discover(address)	#find obex service port number              
                    tell("Probing: " + address + " | " + name)
                    tell("OBEX SERVICES: ")
                    tell(services2)
                    tell(services2.values()[0]) # port number of first OBEX service found
                    tell(" ")
                except:
                    pass
                    
    else:
        tell("device discovery failure: error %d" % error)
    _discoverer.close()

    
# -----------------------------------------------------------------------------


while(1):
    try:
        _discoverer = BtDeviceLister()
        _discoverer.discover_all(discovered, None)
        tell("discovering")
        e32.ao_sleep(30)
        print "scanning again"
    except:
        tell("init failure")
        appuifw.note(u"Fatal error.", "error")