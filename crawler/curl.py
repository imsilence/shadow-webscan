#encoding: utf-8

import logging
import requests
import socket
import time
import traceback

from .config import DEFAULT_USER_AGENT
from .url import URL
from .response import Response

logger = logging.getLogger(__name__)

class Curl(object):

    DEFAULT_HEADERS ={'User-Agent': DEFAULT_USER_AGENT}
    DEFAULT_INTERVAL = 5
    DEFAULT_SPEED = 1
    DEFAULT_TIMEOUT = 2

    NIL = lambda *args, **kwargs: None

    def __init__(self, headers=DEFAULT_HEADERS, cookies=None,
        interval=DEFAULT_INTERVAL, speed=DEFAULT_SPEED,
        timeout=DEFAULT_TIMEOUT):

        self.__headers = headers.copy()
        self.__cookies = cookies.copy() if cookies else {}
        self.__timeout = timeout
        self.__hook(interval, speed)

    def get(self, url, headers=None, **kwargs):
        return self.__send(url, 'GET', headers=headers, **kwargs)

    def post(self, url, data, headers=None, **kwargs):
        return self.__send(url, 'POST', data, headers=headers, **kwargs)

    def request(self, request, **kwargs):
        return self.__send(request.url, request.method, request.data,
                    request.headers, **kwargs)

    def __send(self, url, method='GET', data=None, headers=None, **kwargs):
        if headers:
            headers.update(self.__headers)
        else:
            headers = self.__headers

        if not isinstance(url, URL):
            url = URL(url)

        callback = getattr(requests, method.lower(), self.NIL)
        response = None
        try:
            response = callback(url.url, data=data, headers=headers,
                                    timeout=self.__timeout, **kwargs)
        except Exception as e:
            logger.error('error request url: %s', url.url)
            logger.error(traceback.format_exc())

        return self.__make_response(response, url)

    def __make_response(self, response, url):
        if response is not None:
            return Response(response.status_code, response.reason,
                        response.headers, response.text,
                        request_url=url, charset=response.encoding)
        else:
            return Response(request_url=url)

    def __hook(self, interval, speed):
        connect = socket.socket.connect
        stime = time.time()
        ccount = 0
        timeout = 0.01
        speed = 1
        interval = 5

        def wrapper(object_, *args, **kwargs):
            nonlocal stime, ccount
            while True:
                ctime = time.time()
                time_diff = max(timeout, ctime - stime)
                if time_diff > interval:
                    ccount = 0
                    stime = ctime
                    break
                if ccount / time_diff <= speed:
                    break
                else:
                    time.sleep(timeout)

            ccount += 1
            return connect(object_, *args, **kwargs)

        socket.socket.connect = wrapper