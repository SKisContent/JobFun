import logging
import tornado.ioloop
import tornado.web
from registry.handlers import RegistryHandler

logger = logging.getLogger("registry")
logger.setLevel(logging.INFO)


class RegistryService:
    """
    A microservice that registers other services and returns the endpoint information needed to connect
    """
    def make_app(self):
        return tornado.web.Application([
            (r"/api/v1/register/", RegistryHandler),
        ])

    def start(self):
        logger.info('Starting registry')
        app = self.make_app()
        app.listen(9000)
#        tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    RegistryService().start()
    tornado.ioloop.IOLoop.current().start()
