#encoding: utf-8

from urllib.parse import urljoin
from random import sample
from string import ascii_letters

from simhash import Simhash

from .curl import Curl

class Page404(object):

    def __init__(self):
        self.__404_features = {}
        self.__404_code_list = [200, 301, 302]

    def __generate_features(self, url):
        rand_file = '{0}.html'.format(''.join(sample(ascii_letters, 8)))
        url_404 = urljoin('{0}://{1}'.format(url.scheme, url.netloc), rand_file)
        curl = Curl()
        response_200 = curl.get(url.hostname)
        response_404 = curl.get(url_404)

        if not self.__is_similar(response_200.body, response_404.body):
            self.__404_features[url.hostname] = response_404

    def is_404(self, response):
        if response.status_code == 404:
            return True

        if response.status_code in self.__404_code_list:
            for _ in range(2):
                feature = self.__404_features.get(response.request_url.hostname)

                if feature is None:
                    self.__generate_features(response.request_url)
                elif self.__is_similar(feature.body, response.body):
                    return True
        return False

    def __is_similar(self, body01, body02):
        return Simhash(body01).distance(Simhash(body02)) <= 3
