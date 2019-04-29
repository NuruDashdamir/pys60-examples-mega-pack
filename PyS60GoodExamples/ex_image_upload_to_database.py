
import httplib, urllib
import e32

def main_menu_setup():
    appuifw.app.menu = [(u"send file", senddata)]

def quit():
    appuifw.app.set_exit()


def senddata():
    dep = appuifw.query(u"Anotate:", "text")
    if dep == None:
        test1 = (u"...")
    else:
        test1 = (u""+dep)

    e32.ao_yield()
    f=open('e:\\picture.jpg','rt')
    test3 = f.read()
    f.close()

    params = urllib.urlencode({'data': test1, 'eggs': 0, 'bacon': test3})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    e32.ao_yield()
    conn = httplib.HTTPConnection("www.leninsgodson.com")
    conn.request("POST", "/courses/pys60/php/insert_moblog.php", params, headers)
    response = conn.getresponse()
    conn.close()
    e32.ao_yield()
    appuifw.note(u"Data sent", "info")

    
script_lock = e32.Ao_lock()

main_menu_setup()

script_lock.wait()



        


 



