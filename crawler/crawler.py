#encoding: utf-8

import logging
from collections import namedtuple
from utils.mqueue import Queue
from datetime import timedelta

from utils.timeutil import now, datetime_format

from .config import WHITE_EXTS, BLACK_EXTS
from .url import URL
from .request import Request
from .curl import Curl
from .page_404 import Page404
from .parser import HTMLParser

logger = logging.getLogger(__name__)

RequestEvent = namedtuple('RequestEvent', 'request,depth')

class Crawler(object):

    DEFAULT_DEPTH_LIMIT = 3
    DEFAULT_TIME_LIMIT = 30
    DEFAULT_REQ_LIMIT = 10

    def __init__(self, depth_limit=DEFAULT_DEPTH_LIMIT,
        time_limit=DEFAULT_TIME_LIMIT, req_limit=DEFAULT_REQ_LIMIT):

        self.__depth_limit = depth_limit
        self.__time_limit = time_limit
        self.__req_limit = req_limit
        self.__urls = set()
        self.__requests = set()


    def crawl(self, url):
        queue = Queue()
        white_list = WHITE_EXTS
        black_list = BLACK_EXTS
        depth_limit = self.__depth_limit
        time_limit = timedelta(minutes=self.__time_limit)
        req_limit = self.__req_limit

        urls = self.__urls
        requests = self.__requests

        start_time = now()
        req_count = 0

        curl = Curl()
        page_404 = Page404()

        curl_request = curl.request
        is_404 = page_404.is_404

        if not isinstance(url, URL):
            url = URL(url)

        urls.add(url)
        queue.put(RequestEvent(Request(url), 0))

        while True:
            if queue.empty():
                break

            if now() - start_time > time_limit:
                logger.debug(('over, scanning time on over: %s seconds, ',
                                'start_time: %s, current_time: %s'),
                                time_limit.seconds,
                                datetime_format(start_time),
                                datetime_format(now()))
                break

            if req_count > req_limit:
                logger.debug('over, request count on over: %s', req_limit)
                break

            request_event = queue.get()

            req = request_event.request
            depth = request_event.depth

            if req.url.fileext in white_list:
                logger.debug('skip, ext is white: %s', req.url.url)
                continue

            if depth > depth_limit:
                logger.debug('skip, depth on over: %s', req.url.url)
                continue

            if req in requests:
                logger.debug('skip, request already: %s', req.url.url)
                continue

            response = curl_request(req)

            if response is None or is_404(response):
                continue

            requests.add(req)
            parser = HTMLParser(response)

            depth += 1

            for url in parser.urls:
                if url in urls:
                    continue
                urls.add(url)
                queue.put(RequestEvent(Request(url), depth))

            for _req in parser.requests:
                if _req in requests:
                    continue
                urls.add(_req.url)
                queue.put(RequestEvent(_req, depth))

            req_count += 1

            logger.debug('already request size: %s, left request size: %s',
                req_count, queue.size())

    @property
    def urls(self):
        return self.__urls

    @property
    def requests(self):
        return self.__requests
