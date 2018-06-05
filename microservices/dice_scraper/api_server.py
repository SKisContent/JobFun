import tornado.ioloop
from microservice import Microservice
from dice_scraper.handlers import WordsHandler


class DiceScraperService(Microservice):
    """
    This is the setup class for the microservice
    """
    class Meta:
        name = 'dice_scraper'
        url = 'http://localhost'
        port = 8887
        secret = None

    def handlers(self):
        return [
            (r"/api/v1/words", WordsHandler),
        ]

if __name__ == '__main__':
    DiceScraperService().start()
    tornado.ioloop.IOLoop.current().start()
