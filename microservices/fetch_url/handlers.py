import base64
import tornado.web
import requests
from microservice import HTTP_STATUS_OK, HTTP_STATUS_NO_CONTENT

def get_data(url):
    if not url:
        return None
    try:
        response = requests.get(url)
        response64 = base64.encodebytes(response.content)
        return response64.decode()
    except Exception as e:
        return None


class URLHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.get_argument("url")
        data = get_data(url)
        if not data:
            self.set_status(HTTP_STATUS_NO_CONTENT, 'There was no content')
        else:
            self.write({'data': data})
            self.set_header('Content-Type', 'application/json')
            self.set_status(HTTP_STATUS_OK)
