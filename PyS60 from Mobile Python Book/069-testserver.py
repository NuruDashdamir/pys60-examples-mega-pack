
import SocketServer

class Server(SocketServer.TCPServer):
    allow_reuse_address = True

class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
        print "CLIENT IP %s:%d" % self.client_address
        print "Message: " + self.rfile.readline()

server = Server(('', 9000), Handler)
print "WAITING FOR NEW CONNECTIONS.."
server.serve_forever() 
