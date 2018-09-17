import logging
import tornado.ioloop
import tornado.web
from registry.handlers import RegistryHandler, HeartbeatHandler
from microservice import REGISTRY_PORT

logger = logging.getLogger("registry")
logger.setLevel(logging.ERROR)


class RegistryService:
    """
    A microservice that registers other services and returns the endpoint information needed to connect
    """
    def make_app(self):
        return tornado.web.Application([
            (r"/api/v1/registry/", RegistryHandler),
            (r'/api/v1/ping/', HeartbeatHandler)
        ])

    def start(self):
        logger.info('Starting registry')
        app = self.make_app()
        app.listen(REGISTRY_PORT)
#        tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    RegistryService().start()
    tornado.ioloop.IOLoop.current().start()
