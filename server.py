import sphinx_autobuild
import os
import sys
from contextlib import contextmanager
import base64
from livereload import Server
import BaseHTTPServer
import SimpleHTTPServer
import SocketServer

key = ""
auth_file = '.credentials'
build_folder = "_build/html"

class AuthHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Restricted area\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('Credentials required.')
            pass
        elif self.headers.getheader('Authorization') == 'Basic '+key:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write('Credentials required.')
            pass

def test(HandlerClass = AuthHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
                BaseHTTPServer.test(HandlerClass, ServerClass)




@contextmanager
def pushd(newDir):
    previousDir = os.getcwd()
    os.chdir(newDir)
    yield
    os.chdir(previousDir)

if __name__ == "__main__":

    source_dir = os.path.realpath(".")
    dest_dir = os.path.realpath(build_folder)


    if os.environ.get("ENV") is not None :

        ignored_files = []

        with open(".gitignore", "r") as ins:
            for line in ins:
                ignored_files.append(os.path.abspath(line.rstrip()))

            ins.close()

        builder = sphinx_autobuild.SphinxBuilder(outdir=build_folder,
                                                 args=["-b","html",source_dir,dest_dir],
                                                 ignored=ignored_files)
        server = Server(
            watcher=sphinx_autobuild.LivereloadWatchdogWatcher(),
        )

        server.watch(source_dir, builder)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        server.watch(dest_dir)

        builder.build()

        server.serve(port=8000, host='0.0.0.0', root=dest_dir)

    else:
        builder = sphinx_autobuild.SphinxBuilder(outdir=build_folder,
                                                 args=["-b","html",source_dir,dest_dir])


        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        builder.build()

        sys.argv = ["nouser", "8000"]
        auth = ""

        if os.path.isfile(auth_file) :
            with open(auth_file) as f:
                auth = f.readlines()
                auth = auth[0].rstrip()

            key = base64.b64encode(auth)
            with pushd(dest_dir):
                test()
        else:
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer(("", 8000), Handler)
            httpd.serve_forever()