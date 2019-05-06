import appuifw
import e32
import e32db
import camera
import sysinfo
import time

###############
## import camera
##>>> print camera.image_sizes()
##[(640, 480), (160, 120)]
##>>> print camera.image_modes()
##['RGB12', 'RGB', 'RGB16']
##>>>



def take_photo():

    global stop
    global interval
    global directory
    global filename
    global counter
    global quality
    global size

    if (stop == 1):
        counter = counter + 1

        name = filename + str(counter) + u'.png'

        texto.add(u'Taking photo : ' + name + u'\n')

        imagedir=directory + name

        if (quality == 'high'): mode='RGB'
        elif (quality == 'medium'):   mode='RGB16'
        elif (quality == 'low'):  mode='RGB12'

        if (size == '640') :    size=(640,480)
        elif (size == '160') :    size=(160,120)

        #image = camera.take_photo(mode='RGB',  size=(640,480))
        image = camera.take_photo(mode, size)
        image.save(imagedir)

        #if ((counter % 10) == 0 ):
        #    show_free_space()
        #    if interval > 5 : interval = interval - 5 #Compensamos la perdida de tiempo de la funcion anterior

        show_time()
        e32.ao_sleep(interval, take_photo) 

def show_time():
    
        texto.add( e32db.format_time(time.time()) + u'\n')


def show_free_space():
        #Free space (duration ~5 secs)

        free = sysinfo.free_drivespace()
        unit_v = directory.split(u':')
        unit = unit_v[0]
        unit = unit + u':'
        mem_free = free[u'E:']
        mem_free = mem_free /1024
        texto.add(u'Free space : ' + str(mem_free) + u' kb\n')

#Menu functions
def p_start():
    """Start the photo capture"""

    global stop
    stop = 1
    take_photo()

    
def p_stop():
    """Stop the photo capture"""

    global stop
    stop=0


def p_interval():
    """Set the interval photos"""

    global interval
    interval = appuifw.query(u"Interval: ","number",interval)
    p_print_config()
    

def p_filename():
    """Set the filename"""

    global filename
    filename = appuifw.query(u"Filename: ","text",filename)
    p_print_config()

def p_directory():
    """Set the directory"""

    global directory
    directory = appuifw.query(u"Directory: ","text",directory)
    p_print_config()

def exit_key_handler():

    global stop
    stop = 0
    app_lock.signal()

def p_print_config():
    """Muestra la configuracion"""

    global interval
    texto.add(u'\n')
    texto.add(u'Actual configuration\n')
    texto.add(u'Interval :' + str(interval) + '\n')
    texto.add(u'Filename :' + filename + '\n')
    texto.add(u'Directory :' + directory + '\n')
    texto.add(u'Quality :' + quality + '\n')
    texto.add(u'Size :' + size + '\n')

def set_photo_high():

    global quality
    quality = 'high'

def set_photo_medium():

    global quality
    quality = 'medium'


def set_photo_low():

    global quality
    quality = 'low'

def set_photo_640():

    global size
    size = '640'

def set_photo_160():

    global size
    size = '160'
    
#Default values
interval=10
filename=u'foto'
directory=u'e:\\'
quality = u'high'
size = u'640'

counter=0


stop = 0

appuifw.app.screen='normal'

texto = appuifw.Text()

texto.clear()

texto.add(u'Welcome to AutoFoto 0.1\n')
texto.add(u'Developed by Ignacio Lopez\n')
p_print_config()

appuifw.app.body = texto

appuifw.app.menu = [(u"Start",p_start),(u"Stop",p_stop),
                    (u'Setup', ((u'Interval time',p_interval),(u'Filename',p_filename),(u'Directory',p_directory),(u'View config',p_print_config))),
                    (u'Photo quality',((u'High',set_photo_high),(u'Medium',set_photo_medium),(u'Low',set_photo_low))),
                    (u'Photo size',((u'640x480',set_photo_640),(u'160x120',set_photo_160)))]


appuifw.app.title = u"AutoFoto 0.1"


app_lock = e32.Ao_lock()

appuifw.app.exit_key_handler = exit_key_handler

app_lock.wait()
