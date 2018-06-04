import json
from datetime import datetime
import tornado.web
from tornado.httpclient import AsyncHTTPClient
import logging
from urllib.parse import urlencode
from microservice import CHALLENGE, RESPONSE, HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST

logger = logging.getLogger("registry")


# This is where the services for lookup
# TODO: This is really simplistic. Is it thread-safe? How can it be?
registry = {}


class ServiceMeta:
    """
    A simple class for keeping track of microservice properties. Who knows what else
    we may want to keep track of in the future.
    """
    name = None
    url = None
    port = None
    secret = None
    last_contact = None

    def __init__(self, name, url, port):
        self.name = name
        self.url = url
        self.port = port
        self.last_contact = datetime.now()

    def __unicode__(self):
        return '{0}|{1}|{2}'.format(self.name, self.url, self.port)

    def json(self):
        return json.dumps({'name':self.name, 'url':self.url, 'port':self.port})


def handle_challenge(response):
    """
    This is a handler for the async tornado HTTPClient call to the microservice
    :param response:
    :return:
    """
    if not response.body:
        logger.warning("Response failed for challenge: {0}".format(response.effective_url))
        return
    resp_j = json.loads(response.body.decode())
    logger.info("Got payload from {0}: {1}".format(response.effective_url, resp_j))
    reply = resp_j['reply']
    if reply == RESPONSE:
        service_name = resp_j['name']
        service_url = resp_j['url']
        service_port = resp_j['port']
        logger.info("Got a verification response from service {0}".format(service_name))
        service = ServiceMeta(service_name, service_url, service_port)
        registry[service_name] = service
        logger.info("Added service {0} to the registry".format(service_name))


class RegistryHandler(tornado.web.RequestHandler):
    def get(self):
        """
        get will be used by microservice clients/consumers to get the URL and port of a microservice
        :return:
        """
        service_name = self.get_argument('service_name')
        logger.info("Got a lookup request for service {0}".format(service_name))
        if service_name in registry:
            service = registry[service_name]
            #TODO: check last_contact and refresh if necessary
            self.write(json.dumps({'data': {'name':service.name, 'url':service.url, 'port':service.port}}))
            self.set_header('Content-Type', 'application/json')
            self.set_status(HTTP_STATUS_OK)


    def post(self):
        """
        post will be used by microservices to register themselves
        :return:
        """
        logger.info("New registration request")
        service_name = self.get_argument('name')
        service_url = self.get_argument('url')
        service_port = self.get_argument('port')
        service_secret = self.get_argument('secret', None)
        # TODO: verify that URL is well-formed and that port is a valid integer
        logger.info("Registry got a registration request from service {0}".format(service_name))
        if service_name in registry and service_secret:
            service = registry[service_name]
            # If the service is already registered with the same parameters, refresh the contact
            # If we're getting different URL and port, just fail the request
            if service.name == service_name and service.url == service_url and service.port == service_port:
                service.last_contact = datetime.now()
                self.set_status(HTTP_STATUS_OK)
            else:
                self.set_status(HTTP_STATUS_BAD_REQUEST, 'Service attempted to re-register on different URL and port: {0}'.format(service))
        else:
            # make sure this is one of "our" services that we want to register
            logger.info("Sending challenge to service {0}".format(service_name))
            http_client = AsyncHTTPClient()
            params = urlencode({'challenge': CHALLENGE})
            http_client.fetch('{0}:{1}/api/v1/verify/?{2}'.format(service_url, service_port, params), handle_challenge)

