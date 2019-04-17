import appuifw
import e32
import location
import sysinfo

appuifw.app.screen = 'normal'
textbox = appuifw.Text()
textbox.style = appuifw.STYLE_BOLD
textbox.set(unicode('Mobile Info\n'))
appuifw.app.body = textbox
appuifw.app.title = u'Mobile Info'

def imei():
    imei_number = sysinfo.imei()
    appuifw.note(imei_number)
    textbox.add(u'\nThe IMEI of phone is: \n' + imei_number + u'\n')

def phone():
    (p_x, p_y) = sysinfo.display_pixels()
    textbox.add(u'\nSoftware version:\n' + sysinfo.sw_version())
    textbox.add(u'\nDisplay pixel size:\n' + str(p_x) + u'x' + str(p_y))
    textbox.add(u'\nSelected profile:\n' + sysinfo.active_profile())
    textbox.add(u'\nRingtone type:\n' + sysinfo.ring_type() + u'\n')

def net():
    if not location.gsm_location():
        textbox.add(u'\nNetwork not available\n')
        return
    (mcc, mnc, lac, cellid) = location.gsm_location()
    si = sysinfo.signal_bars()
    textbox.add(u'\nMCC: ' + unicode(mcc))
    textbox.add(u'\nMNC: ' + unicode(mnc))
    textbox.add(u'\nLAC: ' + unicode(lac))
    textbox.add(u'\nCell id: ' + unicode(cellid))
    textbox.add(u'\n\nSignal strength: \n' + str(si) + u'\n')

def battery():
    b = sysinfo.battery()
    textbox.add(u'\nBattery level: ' + str(b) + u'%\n')

def memory():
    tram = sysinfo.total_ram() / 1048576
    trom = sysinfo.total_rom() / 1048576
    fram = sysinfo.free_ram() / 1048576
    textbox.add(u'\nTotal RAM:\n' + str(tram) + u' MB')
    textbox.add(u'\nFree RAM:\n' + str(fram) + u' MB')
    textbox.add(u'\nTotal ROM size is:\n' + str(trom) + u' MB')
    textbox.add(u'\n\nDrive free space in bytes:\n' + str(sysinfo.free_drivespace()) + u'\n')

def quit():
    if (appuifw.query(unicode('Are you Sure?'), 'query')):
        app_lock.signal()


appuifw.app.menu = [
(unicode('Phone IMEI'), imei),
(unicode('Phone Info'), phone),
(unicode('Memory Info'), memory),
(unicode('Network Info'), net),
(unicode('Battery Info'), battery),
(unicode('Exit'), quit)]

appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()

