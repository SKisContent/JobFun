import json
import base64
import tornado.web
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from microservice import HTTP_STATUS_OK, HTTP_STATUS_NO_CONTENT

class WordCloudHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.write("Breaking with all conventions, this API does not support GET")

    def post(self):
        words = self.get_argument("words")
        if not words:
            self.set_status(HTTP_STATUS_NO_CONTENT, 'There was no content')
        # Generate a word cloud image
        else:
            wordcloud = WordCloud(max_font_size=80, width=960, height=540).generate(words)

            # Display the generated image:
            # the matplotlib way:
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            pf = io.BytesIO()
            plt.savefig(pf, format='jpg')

            jpeg64 = base64.b64encode(pf.getvalue())
            self.write({'data':jpeg64.decode()})
            self.set_header('Content-Type', 'application/json')
            self.set_status(HTTP_STATUS_OK)