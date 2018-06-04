import unittest
from handlers import ServiceMeta


class MyTestCase(unittest.TestCase):
    def test_myservice_json(self):
        name = 'example'
        url = 'https://example.com'
        port = 80
        service = ServiceMeta(name, url, port)
        msj = service.json()
        self.assertEqual(msj, '{"name":"example", "url":"https://example.com", "port":80}')


if __name__ == '__main__':
    unittest.main()
