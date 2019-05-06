import appuifw
import e32

def exit_key_handler():
    app_lock.signal()
 
def ru(t):return t.decode('utf-8')
def smartmovi():
    apprun='z:\\system\\programs\\apprun.exe'
    smartmovie='e:\\system\\apps\\smartmovie\\smartmovie.app'
    video='\\system\\apps\\svadba\\1\\1.avi'
    if os.path.exists('e:'+video): video='e:'+video
    else:video='c:'+video
    arg=smartmovie+' "'+video+'"'
    e32.start_exe(apprun,arg)

def video(): 
    apprun='z:\\system\\programs\\apprun.exe'
    MediaPlayer='z:\\system\\apps\\MediaPlayer\\MediaPlayer.app'
    video='\\system\\apps\\svadba\\1\\1.3gp'
    if os.path.exists('e:'+video):video='e:'+video
    else:video='c:'+video
    arg=MediaPlayer+' "'+video+'"'
    e32.start_exe(apprun,arg)

def item2():
    import os,e32
    apprun='z:\\system\\programs\\apprun.exe'
    imageviewer='z:\\system\\apps\\imageviewer\\imageviewer.app'
    image='\\system\\apps\\svadba\\1\\1.jpg'
    if os.path.exists('e:'+image):image= 'e:' + image
    else:image='c:'+image
    arg=imageviewer+' "'+image+'"'
    e32.start_exe(apprun,arg,1)
def item1():
    round.set(u'item one was selected')

def subitem1():
    round.set(u'subitem one was selected')

def subitem2():
    round.set(u'subitem two was selected')


app_lock = e32.Ao_lock()
round = appuifw.Text()
round.set(ru('жми функции'))
appuifw.app.screen='large'
appuifw.app.body = round
appuifw.note(ru('Привет') , "info")
appuifw.app.menu = [(ru('Картинки'), item2),
                    (ru('Видео'), ((ru('3gp'), video),(ru('avi'), smartmovi)))]


appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()
appuifw.note(ru('Желаю счастья в семейной жизни') , "info")