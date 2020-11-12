__server_name__ = '' 
__server_port__ = 8080

from http.server import HTTPServer, BaseHTTPRequestHandler

class HelloWorld(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('hello from xmaek!'.encode('utf-8'))

def run(server_address, handler):
    httpd = HTTPServer(server_address, handler)
    print('starting server on %s' % str(server_address))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print('stopping server')

if __name__ == '__main__':
    server_address = (__server_name__, __server_port__)
    handler = HelloWorld
    run(server_address, handler)