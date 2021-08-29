from bottle import Bottle, HTTPResponse, BaseRequest, request, response, route, run, template, static_file
from http.server import BaseHTTPRequestHandler, HTTPServer

import os
import base64
import logging
import binascii
import threading

BaseRequest.MEMFILE_MAX = 10000000 # (or whatever you want)

class Server:

    def __init__(self, host, port, config):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

        self.config = config

    def _route(self):
        self._app.route('/ping', method="GET", callback=self._index)
        self._app.route('/remove/<filename>', method="DELETE", callback=self._remove)
        self._app.route('/download/<filename>', method="GET", callback=self._download)
        self._app.route('/list', method="GET", callback=self._list)
        self._app.route('/upload', method="POST", callback=self._upload)

    def start(self):
        self._app.run(host=self._host, port=self._port)

    def _index(self):
        return 'Server running... (200 OK)!'

    def _list(self):

        files = [f for f in os.listdir("../files/") if os.path.isfile(os.path.join("../files/", f))]
        return self._response(200, { 'files': files })

    def _save(self):

        body = request.json

        if not 'name' in body:
            return self._message(400, 'PARAMETER NAME IS REQUIRED')

        if not 'data' in body:
            return self._message(400, 'DATA IS REQUIRED')

        name = body['name']
        data = body['data']

        try:

            b64data = base64.b64decode(data)

            if os.path.isfile("../files/" + name):
                return self._message(409, 'FILE ALREADY EXISTS')

            f = open("../files/" + name, "wb")
            f.write(b64data)
            f.close()

        except binascii.Error:
            return self._message(400, 'INVALID PAYLOAD')

        return self._message(200, 'UPLOADED')

    def _download(self, filename):

        if not os.path.isfile("../files/" + filename):
            return self._message(400, 'FILE NOT EXISTS')

        return static_file(filename, root='../files/', download=filename)

    def _upload(self):

        body = request.json

        if not 'name' in body:
            return self._message(400, 'PARAMETER NAME IS REQUIRED')

        if not 'data' in body:
            return self._message(400, 'DATA IS REQUIRED')

        name = body['name']
        data = body['data']

        try:

            b64data = base64.b64decode(data)

            if os.path.isfile("../files/" + name):
                return self._message(409, 'FILE ALREADY EXISTS')

            f = open("../files/" + name, "wb")
            f.write(b64data)
            f.close()

        except binascii.Error:
            return self._message(400, 'INVALID PAYLOAD')

        return self._message(200, 'UPLOADED')

    def _remove(self, filename):

        if not os.path.isfile("../files/" + filename):
            return self._message(400, 'FILE NOT EXISTS')

        os.remove("../files/" + filename)
        return self._message(200, 'REMOVED')

    def _response(self, code, json):
        return HTTPResponse(status=code, body={'code': code, 'response': json}, headers={'Access-Control-Allow-Origin': '*'})

    def _message(self, code, message):
        return HTTPResponse(status=code, body={'code': code, 'message': message}, headers={'Access-Control-Allow-Origin': '*'})

    '''
    def _banner(self):
        return static_file(filename=self.config['static']['banner'], root=self.config['static']['path'])

    def _xml(self, id):

        response.content_type = 'application/xml'

        tcall = self.controller.get_twilio_call_by_id(id)

        stream_name = 'Call Audio Stream'
        stream_url = tcall.ngrok_url.replace('http', 'wss')

        xml = '<Response><Connect><Stream url="' + stream_url + '" /></Connect></Response>'
        return xml
    '''

def run_server(hostname, port, config):
    threading.Thread(target=th, args=[hostname, port, config,], daemon=True).start()

def th(hostname, port, config):
    server = Server(host=hostname, port=port, config=config)
    server.start()