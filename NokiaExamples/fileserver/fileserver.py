# fileserver.py
#
# A simple file transfer server for Series 60 Python environment.
#     
# Copyright (c) 2005 Nokia. All rights reserved.

import binascii

#DEBUGLOG=lambda x: sys.stdout.write(x+"\n")
DEBUGLOG=lambda x: 0

def file_checksums(filelist):
    retval={}
    for fname in filelist:
        try: 
            f=open(fname,'rb')
            checksum=binascii.crc32(f.read())
            f.close()
        except:
            checksum=None
        retval[fname]=checksum
    return retval

class fileserver:
    def __init__(self,sock):
        self.sock=sock
        self.commands={'quit': self.cmd_quit,
                       'get': self.cmd_get,
                       'put': self.cmd_put,
                       'exec': self.cmd_exec,
                       'eval': self.cmd_eval}
    def cmd_quit(self,line):
        self.finished=True
    def cmd_invalid(self,line):
        print >>sys.stderr,'Invalid command '+line,
        self.finished=True        
    def cmd_get(self,cmdline):
        filename=eval(cmdline[4:])
        DEBUGLOG("get "+filename)
        f=open(filename,'rb')
        content=f.read()
        f.close()
        self.senddata(content)
    def cmd_put(self,cmdline):
        words=cmdline.split()
        filename=eval(words[1])
        DEBUGLOG("put "+filename)
        content=self.recvdata()
        f=open(filename,'wb')
        f.write(content)
        f.close()
        print "Wrote %d bytes to %s."%(len(content),filename)
    def senddata(self,data):
        DEBUGLOG("Content-Length: %d"%len(data))
        self.write('Content-Length: '+str(len(data))+'\n'+
                   'CRC32: '+str(binascii.crc32(data))+'\n')
        sentbytes=0        
        # Send the data in little bits because the Bluetooth serial
        # connection may lose data on large sends.
        MAX_SEND=2048
        while sentbytes<len(data):
            n=min(len(data),MAX_SEND)
            self.write(data[sentbytes:sentbytes+n])
            sentbytes+=n
        print "Sent %d bytes."%sentbytes
    def recvdata(self):
        DEBUGLOG("Waiting for data...")
        header_lines=[self.readline() for x in range(2)]
        header=dict([x.rstrip().split(': ') for x in header_lines])
        content_length=int(header['Content-Length'])
        crc32=int(header['CRC32'])
        DEBUGLOG("Content-Length: %d"%content_length)
        recvbytes=0
        content=[]
        DEBUGLOG("Receiving data...")
        while recvbytes<content_length:
            recvstring=self.sock.recv(min(content_length-recvbytes,2048))
            recvbytes+=len(recvstring)
            #print "Received: %d bytes (%3.1f%%)\r"%(recvbytes,(100.*recvbytes/content_length)),
            content.append(recvstring)
        print "Received %d bytes."%recvbytes
        content=''.join(content)
        if crc32 != binascii.crc32(content):
            print "*** CRC error!"        
        return content
    def cmd_exec(self,cmdline):
#        command=eval(cmdline[5:])
        command=eval(self.recvdata())
        DEBUGLOG("exec "+command)
        try:
            exec command in globals()
            result=(0,'')
        except:
            import traceback
            result=(1,apply(traceback.format_exception,sys.exc_info()))
        self.senddata(repr(result))

    def cmd_eval(self,cmdline):
        expr=eval(self.recvdata())
        #expr=eval(cmdline[5:])
        DEBUGLOG("eval "+expr)
        # two eval's because we need to first get rid of one level of
        # quoting.
        result=''
        try:
            value=eval(expr,globals())
            result=(0,value)
        except:
            import traceback
            result=(1,apply(traceback.format_exception,sys.exc_info()))
        self.senddata(repr(result))

    def readline(self):
        s=[]
        while 1:
            c=self.sock.recv(1)
            #self.sock.send(c)
            s.append(c)
            # We support just sane line-endings here.
            if c=='\n':
                break
        return ''.join(s)
    def write(self,msg):
        self.sock.send(msg)
    def run(self):
        self.finished=False
        while not self.finished:
            cmdline=self.readline().rstrip()
            print "Received: "+cmdline
            words=cmdline.split()
            if len(words)>0:
                cmd=words[0]
                DEBUGLOG("Running command: "+cmdline)
                self.commands.get(cmd,self.cmd_invalid)(cmdline)

if __name__ == '__main__':
    import sys
    from e32socket import *
    import e32
    if not e32.is_ui_thread():
        f=open('c:/pythonout.txt','at')
        sys.stdout=f
        sys.stderr=f

    print "Starting server"
    use_tcp=0
    
    if use_tcp:
        s=socket(AF_INET,SOCK_STREAM)
        addr=('127.0.0.1',1025)
        s.bind(addr)
        s.listen(1)
    
        while 1:
            print "Waiting"
            (sock,remoteaddr)=s.accept()
            print "Connected"
            server=fileserver(sock)
            try:
                server.run()
            except:
                import traceback
                traceback.print_exc()
            sock.close()
    else:
        s=socket(AF_BT,SOCK_STREAM)
        try:
            f=open('c:/system/apps/python/fileserver_conf.txt')
            conf=eval(f.read())
            f.close()
            addr=conf['target']
        except:
            addr=('00:20:e0:76:c3:52',10)
            conf={}
        #addr=('00:20:e0:76:c3:52',9)
        print "Connecting to "+`addr`
        s.connect(addr)
        server=fileserver(s)
        try:
            server.run()
        except:
            import traceback
            traceback.print_exc()
        s.close()
        print "Server finished."
    
