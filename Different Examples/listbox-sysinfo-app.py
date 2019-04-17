# Py SysInfo.py script by gauravssn
import sysinfo
import appuifw 
import e32
appuifw.app.title = u"Py SysInfo "
dev = "gauravssnl"
ru = lambda txt : str(txt).decode('utf-8','ignore')
lock = e32.Ao_lock()
def app():
    appuifw.app.exit_key_handler = lock.signal
    active_profile = sysinfo.active_profile()
    battery = sysinfo.battery()
    d1,d2 = sysinfo.display_pixels()
    free_ram = sysinfo.free_ram()/float(1024*1024)
    total_ram = sysinfo.total_ram()/float(1024*1024)
    imei = sysinfo.imei()
    sw_version_list = sysinfo.sw_version().split(' ')
    data_list = [(ru("Active Profile:"),ru(active_profile)),(ru("Battery Percentage:"),ru(battery)),(ru("Free RAM:"),ru(str(free_ram)[:6]+" MB/"+str(total_ram)[:6]+" MB")),(ru("Display:"),ru(str(d1)+" x "+str(d2))),(ru("IMEI:"),imei),(u"Software Version:",sw_version_list[0]),(u"Software Version Date:",sw_version_list[1]),(u"Type",sw_version_list[2])]
    
    list = appuifw.Listbox(data_list, lambda :None)
    appuifw.app.body = list
    appuifw.app.menu=[(u"Refresh Info",app),(u"About",about)]
def about():
    appuifw.note(ru("Developed by gauravssnl"))
app()
lock.wait()
