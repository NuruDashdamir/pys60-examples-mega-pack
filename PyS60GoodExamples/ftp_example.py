# this script lets you upload a file to a URL using the FTP protocol

# NOTE: you need to install first the ftplib library to your phone before
# you can use ftp, because the Nokia Python for S60 package does not incude
# it by default. NOTE: You need to install the ftplib.py file on your phone
# as a python library (not a python script). 
# The ftplib.py (comes originally with the desktop python version)

# in order to get this script work, you need to fill in:
# - your servername (your server must be capable of using FTP)
# - username and password
# - the correct folder where to store the file


import appuifw
from ftplib import FTP


picselection = 'c:/testimg.gif'  # name of file to be uploaded (path on phones hard drive)

def fireupfile():
    global picselection
    ftp = FTP('www.exampleserver.com')     # give servername
    ftp.set_pasv('true')
    ftp.login('username','password')     # give login anonymous
    ftp.cwd('public_html/examplefolder')  # give correct folder where to store the image
    F=open(picselection,'r')
    ftp.storbinary('STOR image.gif',F,1024) # give name of image to be stored as URL
    ftp.quit()
    F.close()

if appuifw.query(u"fire up image?","query") == True:
    fireupfile()            

    


 



