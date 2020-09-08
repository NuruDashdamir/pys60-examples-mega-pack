# fsgui.py
#
# A launcher script for the simple file transfer server
# for Series 60 Python environment.
#     
# Copyright (c) 2005 Nokia. All rights reserved.

import appuifw
import socket
import os
import e32

CONFIG_DIR='c:/system/apps/python'

def discover_address(configfile):
    import appuifw
    CONFIG_FILE=os.path.join(CONFIG_DIR,configfile)
    try:        
        f=open(CONFIG_FILE,'r')
        config=eval(f.read())
        f.close()
    except:
        config={}

    address=config.get('target','')

    if address:
        choice=appuifw.popup_menu([u'Default host',
                                   u'Other...'],u'Connect to:')
        if choice==1:
            address=None
        if choice==None:
            return None # popup menu was cancelled.    
    if not address:
        print "Discovering..."
        addr,services=socket.bt_discover()
        print "Discovered: %s, %s"%(addr,services)
        if len(services)>1:
            choices=services.keys()
            choices.sort()
            choice=appuifw.popup_menu([unicode(services[x])+": "+x
                                       for x in choices],u'Choose port:')
            port=services[choices[choice]]
        else:
            port=services[services.keys()[0]]
        address=(addr,port)
        config['target']=address
        # make sure the configuration file exists.
        if not os.path.isdir(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        f=open(CONFIG_FILE,'wt')
        f.write(repr(config))
        f.close()
    return address

def startserver():
    if os.path.isfile(u'e:\\system\\libs\\fileserver.py'):
        server_script=u'e:\\system\\libs\\fileserver.py'
    elif os.path.isfile(u'c:\\system\\libs\\fileserver.py'):
        server_script=u'c:\\system\\libs\\fileserver.py'
    else:
        appuifw.note(u'fileserver.py not found','error')
        return
    addr=discover_address('fileserver_conf.txt')
    if addr:
        e32.start_server(server_script)
    appuifw.note(u'File server started','info')

startserver()
