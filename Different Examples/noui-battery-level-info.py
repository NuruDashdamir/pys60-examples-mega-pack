# Copyright (c) 2006 Jurgen Scheible
# sysinfo: check_battery_level

import appuifw, e32, sysinfo

def check_battery_level():
    battery_level = sysinfo.battery()
    appuifw.note(u"Battery Level:\n" + unicode(battery_level) + u"%")

def exit_key_handler():
    script_lock.signal()
    appuifw.app.set_exit()
    

script_lock = e32.Ao_lock()

appuifw.app.title = u"Battery level"

appuifw.app.menu = [(u"Check Battery Level", check_battery_level)]

appuifw.app.exit_key_handler = exit_key_handler
script_lock.wait()


 

