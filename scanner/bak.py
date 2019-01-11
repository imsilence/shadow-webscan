#encoding: utf-8

import logging
import random
import copy
import re
from urllib.parse import urljoin

from crawler import Curl
from crawler import Page404

from . import register
from .base import CommonVulnerability
from .vul import Vulnerability
from .serverity import Serverity


logger = logging.getLogger(__name__)


@register('bak')
class Bak(CommonVulnerability):

    NAME = '备份文件'
    RANK = Serverity.HIGH

    def __init__(self):
        self.__file_exts = ['~', '.bak', '.swp']
        self.__target_files = {
            'asp' : r'<\s*%',
            'aspx' : r'<\s*%',
            'php' : r'<?\s*php',
            'jsp' : r'<\s*%',
        }
        self.__content_types = ['application/octet-stream']

    def check(self, request):
        rt_list = []

        file_exts = self.__file_exts
        target_files = self.__target_files
        content_types = self.__content_types

        url = request.url.url
        filename = request.url.filename
        fileext = request.url.fileext
        pattern = target_files.get(fileext)
        if not filename or pattern is None:
            return []

        curl = Curl()

        for ext in file_exts:
            if ext == '.swp':
                bak_filename = '.{0}{1}'.format(filename, ext)
                bak_url = urljoin(url.rpartition('/')[0], bak_filename)

                response = curl.head(bak_url)
                logger.debug('check result: %s, %s', bak_url, response)

                content_type = response.headers.get('content-type', '').lower()
                if content_type in content_types:
                    vul = Vulnerability(self.NAME, self.RANK, bak_url, 'HEAD')
                    logger.info(vul)
                    rt_list.append(vul)
            else:
                bak_url = '{0}{1}'.format(url, ext)

                response = curl.get(url)
                logger.debug('check result: %s, %s', bak_url, response)

                if response.is_ok and not Page404().is_404(response) \
                    and re.search(pattern, response.body, re.I):

                    vul = Vulnerability(self.NAME, self.RANK, bak_url, 'GET')
                    logger.info(vul)
                    rt_list.append(vul)

        return rt_list