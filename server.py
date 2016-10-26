import sphinx_autobuild
import os
import sys
from contextlib import contextmanager
import base64
from livereload import Server
import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
import yaml

key = ""
config_file = '.sphinx-server.yml'
build_folder = "_build/html"
default_v = ""

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


class Config(yaml.YAMLObject):
  yaml_tag = '!config'

  def __init__(self, autobuild,credentials,ignore):
    self.autobuild = autobuild
    self.credentials = credentials
    self.ignore = ignore



@contextmanager
def pushd(newDir):
    previousDir = os.getcwd()
    os.chdir(newDir)
    yield
    os.chdir(previousDir)

if __name__ == "__main__":

    source_dir = os.path.realpath(".")
    dest_dir = os.path.realpath(build_folder)


    yaml.add_path_resolver('!config', ['Config'], dict)


    with open(config_file,"r") as stream :
        try:
            default_v = yaml.load(stream)

            if os.path.isfile("/web/"+config_file):
                with open("/web/"+config_file,"r") as new_stream :
                    try:
                        new_v = yaml.load(new_stream)

                        default_v.update(new_v)


                    except yaml.YAMLError as exc:
                        print(exc)

            print default_v

        except yaml.YAMLError as exc:
            print(exc)

    if default_v['Config'].autobuild :

        ignored_files = default_v['Config'].ignore

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

        if default_v['Config'].credentials["username"] is not None :

            auth = default_v['Config'].credentials["username"]+":"+default_v['Config'].credentials["password"]

            key = base64.b64encode(auth)
            with pushd(dest_dir):
                test()

        else:

            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer(("", 8000), Handler)
            httpd.serve_forever()
