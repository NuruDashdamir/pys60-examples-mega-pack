
def itq(x):
    return x.decode('utf-8')


import appuifw
import e32
import location
import sysinfo
appuifw.app.screen = 'normal'
osama = appuifw.Text()
osama.style = appuifw.STYLE_BOLD
osama.set(itq('ITQPDA Mobile info V 1.0\n\tAUTHOR:OsaMa\n\twww.i-tich.net\nFind Out More info About UR Phone\nCome to you By\n\tITQPDA Team\n\n'))
appuifw.app.body = osama
appuifw.app.title = u'Mobile info By OsaMa'

def about():
    appuifw.note(itq('ITQPDA mobile info\nv1.0      BY OsaMa'), 'info')



def imie():
    i = sysinfo.imei()
    appuifw.note(i)
    osama.add(((itq('\n\t...................\nThe IMEI of phone is : \n') + i) + itq('\n\t...................\n')))



def phoinfo():
    k = sysinfo.sw_version()
    (pi, pi2,) = sysinfo.display_pixels()
    rin = sysinfo.ring_type()
    pro = sysinfo.active_profile()
    osama.add((itq('\n\t...................\nThe Software Ver. of phone is: \n') + k))
    osama.add((((itq('\n_____\nThe Display Pixle is: \n') + str(pi)) + u'x') + str(pi2)))
    osama.add((itq('\n_____\nThe Selected Profile  is: \n') + pro))
    osama.add(((itq('\n_____\nThe Type of ringtone  is: \n') + rin) + itq('\n\t...................\n')))



def net():
    (mcc, mnc, lac, cellid,) = location.gsm_location()
    si = sysinfo.signal_bars()
    osama.add((u'\n\t...................\nMCC: ' + unicode(mcc)))
    osama.add((u'\nMNC: ' + unicode(mnc)))
    osama.add((u'\nLAC: ' + unicode(lac)))
    osama.add((u'\nCell id: ' + unicode(cellid)))
    osama.add(((itq('\n\t...................\nSignal Strength is : \n') + str(si)) + itq('/7\n\t...................\n')))



def bat():
    b = sysinfo.battery()
    osama.add(((itq('\n\t...................\nBattery level: ') + str(b)) + u'/7\n\t...................\n'))



def mem():
    r = sysinfo.total_ram()
    r1 = str(r)
    r2 = int(r1)
    r3 = (r2 / 1024000)
    ro = sysinfo.total_rom()
    ro1 = str(ro)
    ro2 = int(ro1)
    ro3 = (ro2 / 1024000)
    fr = sysinfo.free_ram()
    f = str(fr)
    fre = int(f)
    fo = (fre / 1024)
    dr = sysinfo.free_drivespace()
    osama.add(((itq('\n\t...................\nTotal ram is :\n') + str(r3)) + itq('  MB')))
    osama.add(((itq('\nThe Free ram is :\n') + str(fo)) + itq('  KB')))
    osama.add(((itq('\nTotal ROM size is :\n') + str(ro3)) + itq('  MB')))
    osama.add(((itq('\n_______\n\nDRIVES Disk space in byte is :\n') + str(dr)) + itq('  Byte\n\t...................\n')))



def quit():
    if (appuifw.query(itq('Are you Sure ? '), 'query') == True):
        appuifw.note(itq('Keep Visit\nwww.i-tich.net'), 'info')
        app_lock.signal()
    else:
        print 'www.i-tich.net\nOsaMa'


appuifw.app.menu = [(itq('Phone IMEI'),
  imie),
 (itq('Phone Info'),
  phoinfo),
 (itq('Memory Info'),
  mem),
 (itq('Network Info'),
  net),
 (itq('Battery Info'),
  bat),
 (itq('About'),
  about),
 (itq('Exit'),
  quit)]
appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()

