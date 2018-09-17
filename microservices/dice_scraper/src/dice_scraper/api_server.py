from os import environ
import tornado.ioloop
from microservice import Microservice
from dice_scraper.handlers import WordsHandler


class DiceScraperService(Microservice):
    """
    This is the setup class for the microservice
    """
    class Meta:
        name = 'dice_scraper'
        url = 'http://' + environ.get("SERVICE_URL", "localhost")
        port = environ.get("SERVICE_PORT", 8887)
        secret = None

    def handlers(self):
        return [
            (r"/api/v1/words/", WordsHandler),
        ]

if __name__ == '__main__':
    DiceScraperService().start()
    tornado.ioloop.IOLoop.current().start()
