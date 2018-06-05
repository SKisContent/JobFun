import json
import logging
from datetime import datetime
import requests
import tornado.web
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
from urllib.parse import urlencode

REGISTRY_PORT = 9000
REGISTRY_URL = 'http://localhost'

logger = logging.getLogger("microservice")
logger.setLevel(logging.INFO)

HTTP_STATUS_OK = 200
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_BAD_REQUEST = 400

HEARTBEAT_INTERVAL = 10 # seconds

CHALLENGE = 'It jolly well looks like it might rain'
RESPONSE = 'That is why I carry an umbrella'


class VerificationHandler(tornado.web.RequestHandler):
    def initialize(self, info):
        logger.info("Initializing verification handler for service {0}".format(self.__class__.__name__))
        self.info = info

    def post(self):
        logger.info("Service {0} got a verification challenge".format(self.info.name))
        challenge = self.get_argument("challenge")
        if challenge == CHALLENGE:
            self.info.secret = self.get_argument('secret', None)
            resp = json.dumps({'name': self.info.name,
                               'url': self.info.url,
                               'port': self.info.port,
                               'reply': RESPONSE,
                               'secret': self.info.secret})
            self.write(resp)
            self.set_header('Content-Type', 'application/json')
            self.set_status(HTTP_STATUS_OK)
            logger.info("Service {0} accepted the challenge".format(self.info.name))


def handle_pong(response):
    pass


class Microservice:
    """
    An abstract base class that defines some basic behavior of a microservice.
    Subclasses need to define a Meta nested class with name, url and port properties, and
    they need to implement a handlers() method that returns an array of tuples consisting of
    URLs, references to handler classes, and optional additional paramters, basically the Tornado
    e.g. [(r'/api/v1/my_endpoint', MyEndPointHandler),]
    """
    def __new__(cls, *args, **kwargs):
        new_class = super(Microservice, cls).__new__(cls, *args, **kwargs)
        opts = getattr(new_class, 'Meta', None)
        new_class._meta = opts
        return new_class

    def register_service(self):
        data = {'name': self._meta.name, 'url': self._meta.url, 'port': self._meta.port}
        logger.info('Initiating registration of self: {0}'.format(data))
        response = requests.post('{0}:{1}/api/v1/register/'.format(REGISTRY_URL, REGISTRY_PORT), data=data)

    def make_app(self):
        handlers = self.handlers()
        handlers.append((r"/api/v1/verify/", VerificationHandler, dict(info=self._meta)))
        return tornado.web.Application(handlers)

    def handlers(self):
        raise NotImplementedError()

    def ping(self):
        logger.info("Pinging registry from: {0}".format(self._meta.name))
        http_client = AsyncHTTPClient()
        data = urlencode({'name': self._meta.name, 'url': self._meta.url,
                          'port': self._meta.port, 'secret': self._meta.secret})
        http_client.fetch('{0}:{1}/api/v1/ping/'.format(REGISTRY_URL, REGISTRY_PORT),
                          handle_pong, method='POST', headers=None, body=data)

    def start(self):
        logger.info("Starting service: {0}".format(self._meta.name))
        app = self.make_app()
        app.listen(self._meta.port)
        self.register_service()
        pinger = tornado.ioloop.PeriodicCallback(self.ping, HEARTBEAT_INTERVAL*1000)
        pinger.start()
#        tornado.ioloop.IOLoop.current().start()

