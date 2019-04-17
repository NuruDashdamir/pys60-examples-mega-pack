# Copyright (c) 2006 Jurgen Scheible

import httplib, urllib, e32


def senddata():
    dep = appuifw.query(u"Anotate:", "text")
    if dep == None:
        test1 = (u"...")
    else:
        test1 = (u""+dep)

    params = urllib.urlencode({'data': test1, 'eggs': 0, 'bacon': 0})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("www.leninsgodson.com")
    conn.request("POST", "/courses/pys60/php/set_text.php", params, headers)
    conn.close()
    e32.ao_yield()
    appuifw.note(u"Data sent", "info")

def quit():
    script_lock.signal()

appuifw.app.menu = [(u"send file", senddata)]

appuifw.app.exit_key_handler = quit
script_lock = e32.Ao_lock()
script_lock.wait()



        


 



