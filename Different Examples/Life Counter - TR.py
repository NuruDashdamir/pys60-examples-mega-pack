import appuifw
import e32

def ru(x):
    return x.decode('utf-8')



def exit_key_handler():
    app_lock.signal()



def dalee():
    y = appuifw.query(ru('Do\xc4\x9fum tarihiniz:'), 'date')
    x = appuifw.query(ru('Do\xc4\x9fum saatiniz :)'), 'time')
    round.add(ru('\nHayat k\xc4\xb1sa, onun i\xc3\xa7in her saniyenin k\xc4\xb1ymetini bil ;)'))
    round.add(u'\n')
    d = appuifw.query(ru('\xc5\x9eu anki tarih:'), 'date')
    f = appuifw.query(ru('\xc5\x9eu anki saat :)'), 'time')
    k = ((d + f) - (y + x))
    u = int(k)
    round.add((ru('\nDo\xc4\x9fdu\xc4\x9fundan\nbu yana ge\xc3\xa7en s\xc3\xbcre:\n\n') + str(u)))
    round.add(ru(' saniye...'))
    s = (u / 60)
    round.add(ru('\n'))
    round.add((ru('veya ') + str(s)))
    round.add(ru(' dakika...'))
    i = (s / 60)
    round.add(ru('\n'))
    round.add((ru('veya ') + str(i)))
    round.add(ru(' saat...'))
    j = (i / 24)
    round.add(ru('\n'))
    round.add((ru('veya ') + str(j)))
    round.add(ru(' g\xc3\xbcn...'))
    mes = (j / 30)
    round.add(ru('\n'))
    round.add((ru('veya yakla\xc5\x9f\xc4\xb1k ') + str(mes)))
    round.add(ru(' ay...'))
    god = (j / 365)
    round.add(ru('\n'))
    round.add((ru('veya yakla\xc5\x9f\xc4\xb1k ') + str(god)))
    round.add(ru(' y\xc4\xb1l...'))
    appuifw.app.screen = 'full'



def infa():
    appuifw.note(ru('(Merakl\xc4\xb1s\xc4\xb1na)\ndo\xc4\x9fdu\xc4\x9fundan bu\nyana ne kadar s\xc3\xbcre\nge\xc3\xa7ti\xc4\x9fini hesaplar :)'), 'info')



def start():
    z = appuifw.query(ru('\xc4\xb0sminizi girin:'), 'text')
    round.set((ru('\nSevgili, ') + z))
    round.add(u'\n')
    dalee()



def exit():
    if (appuifw.query(ru('Uygulama kapat\xc4\xb1ls\xc4\xb1n m\xc4\xb1?'), 'query') == 1):
        appuifw.note(ru('G\xc3\xbcle g\xc3\xbcle...\nCepTeam.gen.tr'))
        appuifw.app.set_exit()
        appuifw.note(ru('Ziyaret etmeyi unutma:)'))



def about():
    appuifw.note(ru('Yazan:\n\xd0\x90\xd0\xa0\xd0\xa2\xd0\x95\xd0\x9c (My7610)\n\xc3\x87eviren:\nScHeCk'), 'info')


app_lock = e32.Ao_lock()
round = appuifw.Text()
round.font = u'LatinBold12'
round.style = appuifw.HIGHLIGHT_ROUNDED
round.color = 0
round.set(ru('Hayat Sayac\xc4\xb1n\xc4\xb1za\nho\xc5\x9f geldiniz...\n\nBu uygulama ile do\xc4\x9fdu\xc4\x9funuz g\xc3\xbcnden bu yana ge\xc3\xa7en s\xc3\xbcreyi \xc3\xb6\xc4\x9frenebilirsiniz:) \n\nTR \xc3\x87eviri: ScHeCk\nCepTeam 2oo8\nwww.CepTeam.gen.tr'))
appuifw.app.title = ru('Hayat Sayac\xc4\xb1m')
appuifw.app.screen = 'normal'
appuifw.app.body = round
appuifw.app.menu = [(ru('Ba\xc5\x9flat'),
  start),
 (ru('Bilgi'),
  ((ru('Bu nedir?'),
    infa),
   (ru('Yazan hakk\xc4\xb1nda'),
    about))),
 (ru('\xc3\x87\xc4\xb1k\xc4\xb1\xc5\x9f'),
  exit)]
appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()

