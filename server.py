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


class AuthHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Authentication handler used to support HTTP authentication
    """
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
        if self.headers.getheader('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write('Credentials required.')
            pass
        elif self.headers.getheader('Authorization') == 'Basic ' + key:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write('Credentials required.')
            pass


@contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(previous_dir)


if __name__ == '__main__':

    key = ''
    config_file = '.sphinx-server.yml'
    build_folder = os.path.realpath('_build/html')
    source_folder = os.path.realpath('.')
    configuration = None

    with open(config_file, 'r') as config_stream:
        configuration = yaml.load(config_stream)

        if os.path.isfile(source_folder + '/' + config_file):
            with open(source_folder + '/' + config_file, "r") as custom_stream:
                configuration.update(yaml.load(custom_stream))

    if not os.path.exists(build_folder):
        os.makedirs(build_folder)

    if configuration.get('autobuild'):
        builder = sphinx_autobuild.SphinxBuilder(
            outdir=build_folder,
            args=['-b', 'html', source_folder, build_folder],
            ignored=configuration.get('ignore')
        )

        server = Server(watcher=sphinx_autobuild.LivereloadWatchdogWatcher())
        server.watch(source_folder, builder)
        server.watch(build_folder)

        builder.build()

        server.serve(port=8000, host='0.0.0.0', root=build_folder)
    else:
        # Building once when server starts
        builder = sphinx_autobuild.SphinxBuilder(outdir=build_folder, args=['-b', 'html', source_folder, build_folder])
        builder.build()

        sys.argv = ['nouser', '8000']

        if configuration.get('credentials')['username'] is not None:
            auth = configuration.get('credentials')['username'] + ':' + configuration.get('credentials')['password']
            key = base64.b64encode(auth)

            with pushd(build_folder):
                BaseHTTPServer.test(AuthHandler, BaseHTTPServer.HTTPServer)
        else:
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer(('', 8000), Handler)
            httpd.serve_forever()
