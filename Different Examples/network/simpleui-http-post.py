# this script lets you upload an XML file to a server.
import httplib, urllib
import appuifw

def senddata():
    # read the xml file from the c drive and put it into a variable called xmlfile
    f=open('c:/xml_btscan.xml','rt')
    xmlfile = f.read()
    f.close()    

    # define your parameters that shall be posted and assign its content: the parameter 'data' gets assigned the content of variable xmlfile   
    params = urllib.urlencode({'data': xmlfile, 'eggs': 0, 'bacon': 0})
    # define your headers
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    try:
        # connect to the server: put here your server URL
        conn = httplib.HTTPConnection("www.exampleserver.com")
        # make the post request to call the example.php file and handover the parameters and headers (put the correct folder structure here!)
        conn.request("POST", "/examplefolder/example.php", params, headers)
        response = conn.getresponse()
        # close the connection
        conn.close()
        appuifw.note(u"Data sent", "info")
    except:
        appuifw.note(u"ok something went wrong", "info")

        
if appuifw.query(u"Upload XML file?","query") == True:
    senddata()