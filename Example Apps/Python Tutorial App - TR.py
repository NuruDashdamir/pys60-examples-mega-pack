import appuifw
import keycapture
import e32
import graphics

def tr(Turk):
    return Turk.decode('utf-8')



def exit_key_handler():
    app_lock.signal()



def kode():
    round.color = 255
    round.style = appuifw.STYLE_BOLD
    appuifw.app.body.set(tr('=======RENK KODLARI========\n\nKIRMIZI : 255,0,0\n\nMAV\xc4\xb0 : 255\n\nYE\xc5\x9e\xc4\xb0L : 0,255,0\n\nPEMBE : 255,153,204\n\nSARI : 255,255,00\n\nBEYAZ : 255,255,255\n\nS\xc4\xb0YAH : 0,0,0'))



def hbok():
    round.color = 255
    round.style = appuifw.STYLE_BOLD
    appuifw.app.body.set(tr("     Bilgi Hata Onay Kodlar\xc4\xb1\n\nimport appuifw\n\nBilgi : appuifw.note(u'Bilgi','info')\n\nHata : appuifw.note(u'Hata','eror')\n\nOnay : appuifw.note(u'Onay','conf')"))



def bekle():
    round.color = 255
    round.style = appuifw.STYLE_BOLD
    appuifw.app.body.set(tr('    Bekletme Kodu\n\ne32.ao_sleep(bekletilecek s\xc3\xbcre saniye olarak)\n\n\xc3\x96rne\xc4\x9fin bu kod 5 saniye bekletir\ne32.ao_sleep(5)\n'))



def menu():
    round.color = 255
    round.style = appuifw.STYLE_BOLD
    appuifw.app.body.set(tr("    Men\xc3\xbcye Yaz\xc4\xb1 Kodu\n\nimport appuifw\nimport e32\n\napp_lock=e32.Ao_lock()\ntxt=appuifw.Text()\nappuifw.app.body=txt\ntxt.set(u'yazimizi yaziyoruz')\n"))



def cepevim():
    e32.start_exe('e:\\system\\apps\\PyHocaM\\', 'e:\\system\\apps\\PyHocaM\\')



def exe():
    round.color = 255
    round.style = appuifw.STYLE_BOLD
    appuifw.app.body.set(tr("     Exe \xc3\x87al\xc4\xb1\xc5\x9ft\xc4\xb1rma kodu\n\nimport e32\n\ne32.start_exe('z:\\system\\programs\\apprun.exe','z:\\system\\apps\\Pythoncu\\CepteaM.exe')"))



def fonks():
    round.color = 255
    round.style = appuifw.STYLE_BOLD
    appuifw.app.body.set(tr("      Fonksiyon Tan\xc4\xb1mlama\n\n\nimport appuifw\n\ndef fonks():\nappuifw.note(u'fonksiyon hazir')\n"))



def cik():
    c = int(appuifw.query(tr('EmiN MisiniZ?'), 'query'))
    if (c == 1):
        appuifw.note(u'Yeni Versiyon yakinda Sitemizde Mutlaka Bekliyoruz', 'info')
        appuifw.app.set_exit()



def screen():
    round.color = 255
    round.style = appuifw.STYLE_BOLD
    appuifw.app.body.set(tr("      Ekran Boyut Kodu\n\nimport appuifw\n\nappuifw.app.screen='full'\n\nappuifw.app.screen='normal'\n\nappuifw.app.screen='large"))



def izle():
    appuifw.note(u'Bilgi', 'info')
    appuifw.note(u'Hata', 'error')
    appuifw.note(u'Onay', 'conf')


app_lock = e32.Ao_lock()
round = appuifw.Text()
round.style = appuifw.STYLE_BOLD
round.color = (255,
 0,
 0)
round.set(u'\n\xa4          -=(PyHocaM )=-          \xa4\n\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\xa4\n\xa4       Www.CePTeaM.NeT         \xa4\n\n= => YaP\u0131MC\u0131 : By TiryaKiniM\n\n   Group PaNZeHiR (By TiryaKiniM)\n\n   iSTeK VE \xf6NeRiLeRiNiZ i\xc7iN\n\n   "adamkeserim@hotmail.com"a\n\n         MaiL aTaBiLiRSiNiz...')
appuifw.app.screen = 'full'
appuifw.app.body = round

def tr(Turk):
    return Turk.decode('utf-8')


appuifw.app.menu = [(u'Python Bilgileri',
  ((u'Menu yaz\u0131 Kodu',
    menu),
   (tr('Ekran Boyut Kodu'),
    screen),
   (tr('Bekletme \xc3\x96rne\xc4\x9fi'),
    bekle),
   (u'Fonksiyon tan\u0131mlama',
    fonks),
   (tr('Renk Kodlar\xc4\xb1'),
    kode))),
 (u'Appuifw.note Kodu',
  ((u'Bilgi Hata Onay',
    hbok),
   (tr('Kodu \xc3\x96nizle'),
    izle))),
 (u'Exe Cal\u0131\u015ft\u0131rma',
  ((u'Exe Kodu',
    exe),
   (tr('\xc3\x96nizleme'),
    cepevim))),
 (tr('\xc3\x87\xc4\xb1k\xc4\xb1\xc5\x9f'),
  cik)]
appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()

