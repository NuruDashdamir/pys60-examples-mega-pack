
import appuifw, e32, location, time, os.path

PATH = u"E:\\Data\\gsm_loca\\"
if not os.path.exists(PATH):
        os.makedirs(PATH)

INTERVAL = 5.0
CELL_FILE = PATH + "known_cells.txt"
LOG_FILE = PATH + "visited_cells.txt"
log = file(LOG_FILE, "a")
timer = e32.Ao_timer()

def current_location():
    gsm_loc = location.gsm_location()
    return "%d/%d/%d/%d" % gsm_loc
    
def show_location():
    loc = current_location()
    if loc in known_cells:
        here = known_cells[loc]
        print "You are currently at", here
    else:
        here = ""
        print "Unknown location", loc
    
    print >> log, time.ctime(), loc, here
    timer.after(INTERVAL, show_location)
    
def name_location():
    loc = current_location()
    name = appuifw.query(u"Name this location", "text")
    if name:    
        known_cells[loc] = name

def load_cells():
    global known_cells
    try:
        known_cells = load_dictionary(CELL_FILE)
    except:
        known_cells = {}

def quit():
    print "SAVING LOCATIONS TO", CELL_FILE
    save_dictionary(CELL_FILE, known_cells)
    print "GSM LOCATIONING APP EXITS"
    timer.cancel()
    log.close()
    app_lock.signal()

appuifw.app.exit_key_handler = quit
appuifw.app.title = u"GSM location App"
appuifw.app.menu = [(u"Name this location", name_location)]

print "RECORDING VISITED CELLS TO", LOG_FILE
print "LOADING LOCATIONS FROM", CELL_FILE
load_cells()
print "%d KNOWN CELLS LOADED" % len(known_cells)
show_location()

print "GSM LOCATIONING APP STARTED"
app_lock = e32.Ao_lock()
app_lock.wait()
