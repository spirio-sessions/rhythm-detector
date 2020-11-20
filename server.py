from http.server import HTTPServer, BaseHTTPRequestHandler
from numpy import empty

ctx = {
    'handle': lambda _: None
}

class Server:

    class AudioStreamHandler(BaseHTTPRequestHandler):
        def read_payload(self, unit_size, payload):
            if len(payload) % unit_size != 0:
                raise ValueError(f'unit size {unit_size} and payload length {len(payload)} are incompatible')
            
            frame_length = len(payload) // unit_size
            frames = empty((frame_length,))
            for i in range(0, len(payload), unit_size):
                frame = float(payload[i:i+unit_size])
                frames[i // unit_size] = frame
            return frames


        def do_POST(self):
            chunk_size = int(self.headers['Content-Length'])
            chunk_format = int(self.headers['Chunk-Format'])
            
            raw_chunk = self.rfile.read(chunk_size)
            chunk = self.read_payload(chunk_format, raw_chunk)

            ctx['handle'](chunk)

            self.send_response(200)

    def __init__(self, address):
        name, port = address
        address = (name, int(port))
        self.httpd = HTTPServer(address, self.AudioStreamHandler)

    def with_handle(self, callback):
        ctx['handle'] = callback
        return self

    def run(self):
        print('starting server on %s' % str(self.httpd.server_address))
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
        print('stopping server')