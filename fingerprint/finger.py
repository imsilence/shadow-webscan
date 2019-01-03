#encoding: utf-8

import re
from urllib.parse import urljoin

from utils.md5util import md5

from crawler import URL, Curl
from .config import FEATURES


class Finger(object):

    def __init__(self):
        features = {}
        for feature in FEATURES:
            path = feature[-1].get('path', '/')
            features.setdefault(path, []).append(feature)

        self.__features = features
        self.__curl = Curl()

    def scan(self, url):
        curl = self.__curl
        apps = set()

        if not isinstance(url, URL):
            url = URL(url)

        for path, features in self.__features.items():
            target = urljoin(url.site, path)
            response = curl.get(target)

            for app, type_, conf in features:
                feature = conf.get(type_)
                if type_ == 'regex' and re.search(feature, response.body, re.I) \
                    or type_ == 'md5' and md5(response.body) == feature \
                    or type_ == 'headers' and str(feature[1]).lower() in response.headers.get(feature[0], '').lower():

                    apps.add(app)

        return list(apps)