import appuifw
import e32

def exit_key_handler():
    app_lock.signal()

def info():
    appuifw.note(u'Calculate how long you lived until now', 'info')

def start():
    z = appuifw.query(u'Enter your name:', 'text')
    round.set(u'\nDear ' + z + u'\n')
    y = appuifw.query(u'Birth date:', 'date')
    x = appuifw.query(u'Birth hour:', 'time')
    d = appuifw.query(u'Current date:', 'date')
    f = appuifw.query(u'Current hour:', 'time')
    
    round.add(u'Life is short, enjoy it while you can! :)\n')
    u = int((d + f) - (y + x))
    round.add(u'\nTime passed since you were born:\n\n')
    round.add(unicode(u) + u' second...\n')
    s = (u / 60)
    round.add(u'or ' + str(s) + u' minute...\n')
    i = (s / 60)
    round.add(u'or ' + str(i) + u' hour...\n')
    j = (i / 24)
    round.add(u'or ' + str(j) + u' day...\n')
    month = (j / 30)
    round.add(u'or ' + str(month) + u' month...\n')
    year = (j / 365)
    round.add(u'or ' + str(year) + u' year...\n')
    appuifw.app.screen = 'full'


def exit():
    if (appuifw.query(u'Exit?', 'query') == 1):
        appuifw.app.set_exit()

app_lock = e32.Ao_lock()
round = appuifw.Text()
round.font = u'LatinBold12'
round.style = appuifw.HIGHLIGHT_ROUNDED
round.color = 0
round.set(u'Life Counter\n\nWith this app, you can learn how much time passed since the day you were born\n')
appuifw.app.title = u'Life Counter'
appuifw.app.screen = 'normal'
appuifw.app.body = round
appuifw.app.menu = [(u'Start',start), (u'Exit', exit)]
appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()

