import tornado.ioloop
from microservice import Microservice
from cloud_creator.handlers import WordCloudHandler


class WordcloudService(Microservice):
    """
    This is the setup class for the microservice
    """
    class Meta:
        name = 'wordcloud'
        url = 'http://localhost'
        port = 8886

    def handlers(self):
        return [
            (r"/api/v1/wordcloud", WordCloudHandler),
        ]

if __name__ == '__main__':
    WordcloudService().start()
    tornado.ioloop.IOLoop.current().start()
