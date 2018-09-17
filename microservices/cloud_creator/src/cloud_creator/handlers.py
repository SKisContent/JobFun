import io
import json
import base64
import tornado.web
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from microservice import HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_NO_CONTENT


def get_image(words):
    if not words:
        return None
    try:
        # Generate a word cloud image using the wordcloud library
        wordcloud = WordCloud(max_font_size=80, width=960, height=540).generate(words)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        pf = io.BytesIO()
        plt.savefig(pf, format='jpg')
        jpeg64 = base64.b64encode(pf.getvalue())
        return jpeg64.decode()
    except Exception as ex:
        return None


class WordCloudHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Breaking with all conventions, this API does not support GET")
        self.set_status(HTTP_STATUS_BAD_REQUEST, 'There was no content')

    def post(self):
        words = self.get_argument("words")
        image = get_image(words)
        if not image:
            self.set_status(HTTP_STATUS_NO_CONTENT, 'There was no content')
        else:
            self.write(json.dumps({'data':image}))
            self.set_header('Content-Type', 'application/json')
            self.set_status(HTTP_STATUS_OK)