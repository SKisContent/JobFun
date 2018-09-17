from os import environ
import tornado.ioloop
from microservice import Microservice
from fetch_url.handlers import URLHandler


class FetchUrlService(Microservice):
    """
    This is the setup class for the microservice
    """
    class Meta:
        name = 'fetch_url'
        url = 'http://' + environ.get("SERVICE_URL", "localhost")
        port = environ.get("SERVICE_PORT", 8888)
        secret = None

    def handlers(self):
        return [
            (r"/api/v1/fetchurl/", URLHandler),
        ]


if __name__ == '__main__':
    FetchUrlService().start()
    tornado.ioloop.IOLoop.current().start()
