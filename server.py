import SimpleHTTPServer
import SocketServer

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/yolo.png'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

def run(port):
	Handler = MyRequestHandler
	server = SocketServer.TCPServer(('0.0.0.0', port), Handler)

	server.serve_forever()

