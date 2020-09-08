# install first the following files to your phone
# pyexpat-series60_v20.sis
# it they will install automatically the pyexpat libraries for the script below):
# found at: http://pdis.hiit.fi/pdis/download/pdis/


import xml.parsers.expat
K=[]
# 3 handler functions
def start_element(name, attrs):
    print 'Start element:', name, attrs
def end_element(name):
    print 'End element:', name
def char_data(data):
    print 'Character data:', repr(data)
    K.append(repr(data))

p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

#tempfile = "c:/xml_btscan.xml"
#f = open(tempfile, 'r')
#weatherinfo = f.read()
#f.close()

#p.Parse(weatherinfo, 1)
p.Parse("""<xml>
<channel>
<title>Users present:</title>
<timestamp>Thu Dec 29 14:01:25 2005: logging started</timestamp>
<item_users>
<user_bt_id>00:11:9f:c1:3e:21</user_bt_id>
<user_nickname>Mrx</user_nickname>
</item_users>
<item_users>
<user_bt_id>00:0a:3a:5c:01:79</user_bt_id>
<user_nickname>Mafiosi</user_nickname>
</item_users>
<item_users>
<user_bt_id>00:12:62:e0:99:4e</user_bt_id>
<user_nickname>Jj</user_nickname>
</item_users>
</channel>
</xml>""", 1)

print K

