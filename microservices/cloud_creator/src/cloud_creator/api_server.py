from os import environ
import tornado.ioloop
from microservice import Microservice
from cloud_creator.handlers import WordCloudHandler


class WordcloudService(Microservice):
    """
    This is the setup class for the microservice
    """
    class Meta:
        name = 'cloud_creator'
        url = 'http://' + environ.get("SERVICE_URL", "localhost")
        port = environ.get("SERVICE_PORT", 8886)
        secret = None

    def handlers(self):
        return [
            (r"/api/v1/wordcloud/", WordCloudHandler),
        ]


if __name__ == '__main__':
    WordcloudService().start()
    tornado.ioloop.IOLoop.current().start()
