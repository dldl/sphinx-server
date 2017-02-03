import SimpleHTTPServer
import SocketServer
import threading
import webbrowser
import platform
from socket import SOL_SOCKET,SO_REUSEADDR

class HTTPServer():

    def __init__(self,port=8000,url='http://localhost', handler=SimpleHTTPServer.SimpleHTTPRequestHandler):
        self.port = port
        self.thread = None
        self.httpd = None
        self.run = False
        self.url = url
        self.handler = handler



    def start(self):
        self.run = True
        self.httpd = SocketServer.TCPServer(("localhost", self.port), self.handler, bind_and_activate=False)
        self.httpd.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.httpd.allow_reuse_address = True
        self.httpd.server_bind()
        self.httpd.server_activate()
        self.thread = threading.Thread(target = self._serve)
        self.thread.start()

    def _serve(self):
        while self.run:
            self.httpd.handle_request()

    def stop(self):
        self.run = False
        self.httpd.socket.close()
        self.httpd.server_close()