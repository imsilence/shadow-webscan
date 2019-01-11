#encoding: utf-8

import logging
import random
import copy
import re

from crawler import Curl

from . import register
from .base import CommonVulnerability
from .vul import Vulnerability
from .serverity import Serverity


logger = logging.getLogger(__name__)

@register('cmd')
class CMD(CommonVulnerability):

    NAME = '命令注入'
    RANK = Serverity.HIGH

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
        xss_key = self.__xss_key
        playloads = []

        cmds = self.__get_cmds()

        for name, value in params.items():
            value = "".join(value) if isinstance(value, (list, )) else value

            for cmd in cmds:
                cmd_type = cmd['type']
                pattern = cmd['pattern']
                pls = cmd['playloads']
                for pl in pls:
                    poc = copy.deepcopy(params)
                    poc[name] = '{0}{1}'.format(value, pl);
                    playloads.append((name, poc, pattern))

        return playloads

    def __get_cmds(self):
        cmds = []
        cmds.append({
            'type' : 'linux',
            'pattern' : r'id',
            'playloads' : [';id;', "';id;'", '";id;"'],
        })
        cmds.append({
            'type' : 'php',
            'pattern' : r'468c7e1fa14fb25592490062c0153f4d',
            'playloads' : [
                "${print(md5('imsilence))}",
                "';${print(md5('imsilence))};'",
                "\"]=1;${print(md5('imsilence))};//",
            ],
        })
        return cmds