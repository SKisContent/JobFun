from bs4 import BeautifulSoup
import tornado.web
import json
from microservice import HTTP_STATUS_OK, HTTP_STATUS_NO_CONTENT


def get_words(html):
    """
    Converts the provided string input to HTML, finds the Dice.com job-listing page-specific <div>
    element and extracts all text content contained within. There's not a whole lot of complex
    processing here.
    :param html:
    :return:
    """
    try:
        soup = BeautifulSoup(html, "html5lib")
        job_desc = soup.find("div", id="jobdescSec")
        if not job_desc:
            return None
        else:
            job_text = job_desc.stripped_strings
            words = ' '.join(job_text)
            json_response = json.dumps({'data':words})
            return json_response
    except:
        return None


class WordsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Breaking with all conventions, this API does not support GET")

    def post(self):
        html = self.get_argument("html")
        json_response = get_words(html)
        if not json_response:
            self.set_status(HTTP_STATUS_NO_CONTENT, 'There was no content')
        else:
            self.write(json_response)
            self.set_header('Content-Type', 'applicaton/json')
            self.set_status(HTTP_STATUS_OK)
