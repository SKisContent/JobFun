import unittest
from .handlers import get_words

class MockRequest:
    COOKIES = {'': 'secure', 'Domain': 'None', 'expires': 'None', 'Max-Age': 'None', 'Path': '/'}
    FILES = None #
    GET = None  # < QueryDict: {} >
    META = None #
    POST = None
    content_params = None
    content_type = None
    encoding = None
    method = None
    path = None
    scheme = None
    session = None
    user = None

class MockApplication:
    ui_methods = {'items': None}

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        request = MockRequest()
        app = MockApplication


    def test_bad_html(self):
        html = 'This is not html'
        j_resp = get_words(html)
        self.assertIsNone(j_resp)


if __name__ == '__main__':
    unittest.main()
