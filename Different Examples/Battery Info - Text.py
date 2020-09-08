# Copyright (c) 2006 Jurgen Scheible
# sysinfo: check_battery_level

import appuifw
import e32
import sysinfo

def check_battery_level():
    batty = sysinfo.battery()
    print batty



def exit_key_handler():
    script_lock.signal()
    appuifw.app.set_exit()
    

script_lock = e32.Ao_lock()

appuifw.app.title = u"Battery level"

appuifw.app.menu = [(u"check battery", check_battery_level)]

appuifw.app.exit_key_handler = exit_key_handler
script_lock.wait()


 

