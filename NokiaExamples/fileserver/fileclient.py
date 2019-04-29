#
# fileclient.py 
#
# A client library for the simple file transfer server for Series 60 Python environment.
#     
# Copyright (c) 2005 Nokia. All rights reserved.

import os
import sys
import binascii
import ntpath

symbianbasename=ntpath.basename

class fileclient:
    def __init__(self,sock,verbose=0):
        self.sock=sock
        self.verbose=verbose
        if verbose:
            self.log=sys.stdout.write
        else:
            self.log=lambda x:0        
    def recvdata(self):
        #self.log("Waiting for content length..."
        header_lines=[self.readline() for x in range(2)]
        header=dict([x.rstrip().split(': ') for x in header_lines])
        content_length=int(header['Content-Length'])
        crc32=int(header['CRC32'])
        self.log("Content-Length: %d"%content_length+"\n")
        recvbytes=0
        content=[]
        #self.log("Receiving data...")
        while recvbytes<content_length:
            recvstring=self.sock.recv(min(content_length-recvbytes,2048))
            recvbytes+=len(recvstring)
            self.log("Received: %d bytes (%3.1f%%)\r"%(recvbytes,(100.*recvbytes/content_length)))
            sys.stdout.flush()
            content.append(recvstring)
        self.log("Received: %d bytes.        "%(recvbytes)+"\n")
        content=''.join(content)
        if crc32 != binascii.crc32(content):
            raise IOError("CRC error while receiving data")
        return content
    def senddata(self,data):
        #print "Sending data..."
        self.log("Content-Length: %d"%len(data)+"\n")
        self.write('Content-Length: '+str(len(data))+'\n'+
                   'CRC32: '+str(binascii.crc32(data))+'\n')
        sentbytes=0        
        # Send the data in little bits because the Bluetooth serial
        # connection may lose data on large sends.
        MAX_SEND=2048
        while sentbytes<len(data):
            n=min(len(data)-sentbytes,MAX_SEND)
            self.write(data[sentbytes:sentbytes+n])
            sentbytes+=n
            self.log("Sent: %d bytes (%3.1f%%)\r"%(sentbytes,(100.*sentbytes/len(data))))
            sys.stdout.flush()
        self.log("Sent: %d bytes.            "%(sentbytes)+"\n")
    def get(self,filename):
        self.log("get "+filename+"\n")
        self.write("get "+repr(filename)+"\n")
        return self.recvdata()
    def put(self,filename,content):
        self.log("put "+filename+"\n")
#        self.write("put "+repr(filename)+" "+str(len(content))+'\n')
        self.write("put "+repr(filename)+"\n")
        self.senddata(content)
    def download(self,remotefile,localfile=None):
        if localfile is None:
            localfile=symbianbasename(remotefile)
        content=self.get(remotefile)
        f=open(localfile,'wb')
        f.write(content)
        f.close()
    def upload(self,remotefile,localfile=None):
        if localfile is None:
            localfile=symbianbasename(remotefile)
        f=open(localfile,'rb')
        content=f.read()
        f.close()
        self.put(remotefile,content)            
    def eval(self,expr):
        self.log("eval "+expr+"\n")
        self.write("eval\n")# "+repr(expr)+"\n")
        self.senddata(repr(expr))
        result=eval(self.recvdata())
        if result[0]!=0:
            raise "Exception on server side: "+''.join(result[1])
        else:
            return result[1]
    def exec_(self,expr):
        self.log("exec "+expr+"\n")
        self.write("exec\n")
        self.senddata(repr(expr))
        #self.write("exec "+repr(expr)+"\n")
        result=eval(self.recvdata())
        if result[0]!=0:
            raise "Exception on server side: "+''.join(result[1])
    def killserver(self):
        self.log("Sending quit command to server..."+"\n")
        self.write('quit\n')
    def readline(self):
        s=[]
        while 1:
            c=self.sock.recv(1)
            if c=='':
                continue
            #self.sock.send(c)
            s.append(c)
            # We support just sane line-endings here.
            if c=='\n':
                break
        return ''.join(s)
    def write(self,msg):
        self.sock.send(msg)
    
class filesocket:
    def __init__(self,file):
        self.file=file
    def recv(self,n=1):
        return self.file.read(n)
    def send(self,msg):
        n=self.file.write(msg)
        self.file.flush()
        return n

def connect(port='/dev/ttyS4',use_tcp=0,verbose=0):
    if use_tcp:
        import socket
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr=('127.0.0.1',1025)
        print "Connecting via TCP to "+`addr`+"...",
        sys.stdout.flush()
        s.connect(addr)
        client=fileclient(s,verbose)
        print "ok."
    else:
        print "Connecting to serial port "+port+"...",
        sys.stdout.flush()
        f=open(port,'r+b',0)
        fs=filesocket(f)
        client=fileclient(fs,verbose)
        print "ok."
    return client
