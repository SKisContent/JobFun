from django.shortcuts import render
from django.views.generic import TemplateView
from jobfun.cloudfun.forms import WordCloudForm
from urllib.parse import urlparse
import requests
import base64

# Create your views here.
class WordCloudView(TemplateView):
    template_name = "cloudfun/wordcloud.html"
    success_url = '/cloudfun/'
    form_class = WordCloudForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        results = None
        message = None
        if form.is_valid():
            # Look up the microservice in the registry
            # So the registry is hard-coded, it could be added to django settings
            # The service name is hard-coded. Here or elsewhere, there's no getting around it.
            resp = requests.get('http://localhost:9000/api/v1/register/', params={'service_name': 'fetch_url'})
            if resp.status_code == 200:
                # Here we extract the service information
                service = resp.json()['data']
                words = ''
                urls = form.cleaned_data['urls'].split('\n')
                for url in urls:
                    # Call the service that we dynamically looked up in the registry
                    # The path is hard-coded, but it would be for any API call
                    resp = requests.get('{0}:{1}/api/v1/fetchurl/'.format(service['url'], service['port']), params={'url': url})
                    if resp.status_code == 200:
                        html64 = resp.json()['data']
                        html = base64.decodebytes(html64.encode())

                        parse_result = urlparse(url)
                        # could/should check this before fetching the page
                        if parse_result.netloc.endswith('dice.com'):
                            # Completely hard-coded way of calling the microservice--not using registry
                            resp = requests.post('http://localhost:8887/api/v1/words', data={'html': html})
                            if resp.status_code == 200:
                                words += resp.json()['data']
                        else:
                            message = "Only dice.com is currently supported"
                    else:
                        message = 'Unable to retrieve data from at least one URL'
                if words:
                    # Completely hard-coded way of calling the microservice--no registry
                    resp = requests.post('http://localhost:8886/api/v1/wordcloud', data={'words': words})
                    if resp.status_code == 200:
                        results = resp.json()['data']
                else:
                    message = 'Unable to extract any words'
            else:
                message = 'Unable to complete the request at this time'

        return render(request, self.template_name, {'form': form, 'results': results, 'message': message})