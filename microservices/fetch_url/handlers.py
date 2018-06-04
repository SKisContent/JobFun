import base64
import tornado.web
import requests
from microservice import HTTP_STATUS_OK, HTTP_STATUS_NO_CONTENT


class URLHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        url = self.get_argument("url")
        if not url:
            self.set_status(HTTP_STATUS_NO_CONTENT, 'There was no content')
        else:
            def handle_response(response):
                response64 = base64.encodebytes(response.content)
                self.write({'data': response64.decode()})
                self.set_header('Content-Type', 'application/json')
                self.set_status(HTTP_STATUS_OK)

            response=requests.get(url)
            handle_response(response)
