#!/usr/bin/env python3

import logging
import os
import signal


from datetime import datetime
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

DEFAULT_PORT = 8080
DEFAULT_FOLDER = "/data"

LOGGER = logging.getLogger(__name__)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode('utf-8') # <--- Gets the data itself
        LOGGER.debug("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data)

        self.send_response(200)
        self.end_headers()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
   
        H2J.process_data(post_data)

class Http2json():
    def __init__(self, conf: dict):
        # Initialize the class.
        super().__init__()
        os.makedirs(DEFAULT_FOLDER, exist_ok=True)

        self.port = conf.get("Port")

    def listen(self):
        server = ThreadingHTTPServer(('0.0.0.0', self.port), HTTPRequestHandler)
        LOGGER.info(f"Starting server at http://127.0.0.1:{self.port}")
        server.serve_forever()

    def read_testfile(self, filename):
        with open(filename) as f:
            self.process_data(f.read())

    def process_data(self, data):

        try:
            j = json.loads(data)
        except ValueError as e:
            return

        # print(json.dumps(j, indent=2))

        fn = os.path.join(DEFAULT_FOLDER, datetime.strftime(datetime.now(),"%Y%m%d_%H%M%S.%f")[:-3] + ".json")

        with open(fn, 'w', encoding='utf-8') as f:
            json.dump(j, f, ensure_ascii=False, indent=2)
        
        LOGGER.info(f"Written file: {fn}")



if __name__ == '__main__':
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    logging.basicConfig(level=log_level)


    def sig_handler(sig_num, frame):
        logging.debug(f"Caught signal {sig_num}: {frame}")
        logging.info("Exiting program.")
        exit(0)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    
    config = {}
    config["Port"] = os.environ.get("PORT", DEFAULT_PORT)

    H2J = Http2json(config)
    # H2J.read_testfile('SamplePost.json')
    H2J.listen()
    


