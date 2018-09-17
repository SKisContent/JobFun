from django.shortcuts import render
from django.views.generic import TemplateView
from jobfun.cloudfun.forms import WordCloudForm
from urllib.parse import urlparse
import requests
import base64

from jobfun import settings


class MicroserviceException(Exception):
    pass


def lookup_microservice(service_name):
    resp = requests.get('http://{0}:9000/api/v1/registry/'.format(settings.REGISTRY), params={'service_name': service_name})
    if resp.status_code == 200:
        return resp.json()
    raise MicroserviceException('Unable to get internal handler to complete the task')


def do_api_get(path, service, params):
    resp = requests.get('http://{0}:{1}{2}'.format(service['url'], service['port'], path), params=params)
    if resp.status_code == 200:
        return resp.json()
    raise MicroserviceException('Problem during processing of the task.')


def do_api_post(path, service, data):
    resp = requests.post('http://{0}:{1}{2}'.format(service['url'], service['port'], path), data=data)
    if resp.status_code == 200:
        return resp.json()
    raise MicroserviceException('Problem during processing of the task.')


class WordCloudView(TemplateView):
    template_name = "cloudfun/wordcloud.html"
    form_class = WordCloudForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        results = None
        message = None
        if form.is_valid():
            try:
                words = ''
                urls = form.cleaned_data['urls'].split('\n')
                for url in urls:
                    # Call the service that we dynamically looked up in the registry
                    # The path is hard-coded, but it would be for any API call
                    parse_result = urlparse(url)
                    if parse_result.netloc.endswith('dice.com'):
                        # Look up the microservice in the registry
                        fetch_url_service = lookup_microservice('fetch_url')['data']
                        # call the microservice api
                        html64 = do_api_get('/api/v1/fetchurl/', fetch_url_service, {'url': url})['data']
                        html = base64.decodebytes(html64.encode())

                        dice_scraper_service = lookup_microservice('dice_scraper')['data']
                        words += do_api_post('/api/v1/words/', dice_scraper_service, data={'html': html})['data']
                    else:
                        message = "Only dice.com is currently supported"
                if len(words) > 0:
                    word_cloud_service = lookup_microservice('cloud_creator')['data']
                    results = do_api_post('/api/v1/wordcloud/', word_cloud_service, data={'words': words})['data']
                else:
                    message = 'Unable to extract any words'
            except MicroserviceException:
                message = 'Unable to complete the request at this time'

        return render(request, self.template_name, {'form': form, 'results': results, 'message': message})
