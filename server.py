from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Lock
from random import shuffle
from untagged import *
from sys import argv
import json

lock = Lock()
retriever.init("hotels")

def rank_hotels(data):
    query = data['query']
    hotels = data['list']
    lock.acquire()
    rank = retriever.retrieveContainer(query, hotels)
    lock.release()
    rank = map(lambda x : [x, 0, 0, 0], rank)
    return rank

def rank_comments(data):
    query = data['query']
    hotel = data['hotel']
    comments = data['list']
    lock.acquire()
    rank = retriever.retrieveContent(query, hotel, comments)
    lock.release()
    rank = map(lambda x : [x, 0, 0], rank)
    return ranked

def process(post_data):
    data = json.loads(post_data)
    command = data['command']
    if(command == 'hotels'):
        return rank_hotels(data)
    else:
        return rank_comments(data)

class Webserver(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_headers()
        out = process(post_data)
        out_json = json.dumps(out)
        self.wfile.write(out_json)


def run(port=80, server_class=HTTPServer, handler_class=Webserver):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting web server...'
    httpd.serve_forever()

if __name__ == "__main__":
    if len(argv) == 2:
        value = int(argv[1])
        run(value)
    else:
        run()