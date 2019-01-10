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


class LFI(CommonVulnerability):

    NAME = '本地文件包含'
    RANK = Serverity.HIGH

    NIL = lambda *args, **kwargs: None

    def __init__(self):
        self.__white_params = []

    def check(self, request):
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
            response = callback(request.url, **{key : params})

            if not response.body or re.search(pattern, response.body, re.I) is None:
                continue

            vul = Vulnerability(self.NAME, self.RANK, request.url.url,
                                    request.method, name, poc)
            logger.info(vul)
            rt_list.append(vul)

        return rt_list

    def __get_playloads(self, params):
        playloads = []
        for name, value in params.items():
            poc = copy.deepcopy(params)
            value = "".join(value) if isinstance(value, (list, )) else value
            tpl = "{0}-->''''''\"\"\"\"\"\">>>>>>;;;;;;</ScRiPt>{1}//"
            poc[name] = tpl.format(value, xss_key)
            playloads.append((name, poc))
        return playloads