#encoding: utf-8

import logging
import random
import copy

from simhash import Simhash

from crawler import Curl

from . import register
from .base import CommonVulnerability
from .vul import Vulnerability
from .serverity import Serverity


logger = logging.getLogger(__name__)


@register('xss')
class XSS(CommonVulnerability):

    NAME = '跨站脚本攻击'
    RANK = Serverity.MEDIUM

    NIL = lambda *args, **kwargs: None

    def __init__(self):
        self.__xss_key = '<A>XSS_FLAG</A>'
        self.__white_params = []

    def check(self, request):
        xss_key = self.__xss_key
        white_params = self.__white_params

        curl = Curl()

        key = ''
        callback = None
        params = {}
        if request.method == 'GET':
            key = 'data'
            callback = curl.post
            params = request.params
        else:
            key = 'params'
            callback = curl.get
            params = request.post

        playloads = self.__get_playloads(params)
        rt_list = []
        for name, poc in playloads:
            if name in white_params:
                continue

            response = callback(request.url, **{key : poc})
            logger.debug('check result: %s, %s, %s, %s',
                            request.url, key, poc, response)

            if not response.body or response.body.find(xss_key) == -1:
                continue

            vul = Vulnerability(self.NAME, self.RANK, request.url.url,
                                    request.method, name, poc)
            logger.info(vul)
            rt_list.append(vul)

        return rt_list

    def __get_playloads(self, params):
        xss_key = self.__xss_key
        playloads = []
        for name, value in params.items():
            poc = copy.deepcopy(params)
            value = "".join(value) if isinstance(value, (list, )) else value
            tpl = "{0}-->''''''\"\"\"\"\"\">>>>>>;;;;;;</ScRiPt>{1}//"
            poc[name] = tpl.format(value, xss_key)
            playloads.append((name, poc))
        return playloads