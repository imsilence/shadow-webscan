#encoding: utf-8

import logging
import traceback
import re
from urllib.parse import urljoin, urlencode

from lxml import etree

from utils.decorators import parse

from .url import URL
from .form import Form
from .request import Request


logger = logging.getLogger(__name__)


class HTMLParser(object):

    URL_HEADERS = ('location', )
    URL_TAGS = ('link', 'script', 'iframe', 'frame', 'object',
                'a', 'img', 'form')
    URL_ATTRS = ('href', 'src', 'data', 'action')
    URL_RES = [
        re.compile(r'(https?://[\w:@\-\./=?#]*)', re.U|re.I),
        re.compile(r'''((/\w+)+\.(asp|html|jsp|php|aspx|htm|do|action)
                    (\?[\w%]+=[\w%]+(&[\w%]+=[\w%]+)*)?(\#[\w]*)?)''',
                    re.U|re.I|re.X)
    ]

    NIL = lambda *args, **kwargs: None

    def __init__(self, response):
        self.__base_url = response.request_url.url
        self.__response = response
        self.__urls_header = set()
        self.__urls_re = set()
        self.__urls_tag = set()
        self.__forms = []
        self.__in_form = False
        self.__requests = []
        self.__parsed = False

    def __call__(self):
        if self.__parsed:
            return
        self.__parsed = True
        try:
            self.__header_parse()
            self.__regex_parse()
            self.__xml_parse()
        except Exception as e:
            logger.error('error parse response: %s', self.__base_url)
            logger.error(traceback.format_exc())

    def __header_parse(self):
        for name in self.URL_HEADERS:
            value = self.__response.headers.get(name)
            url = self.__make_url(value)
            if url:
                self.__urls_header.add(url)

    def __regex_parse(self):
        for regex in self.URL_RES:
            for url in regex.findall(self.__response.body):
                if isinstance(url, tuple):
                    url = url[0]
                url = self.__make_url(url)
                if url:
                    self.__urls_re.add(url)

    def __xml_parse(self):
        parser = etree.HTMLParser(target=self)
        etree.fromstring(self.__response.body, parser)

    def start(self, tag, attrs):
        tag = tag.lower()

        callback = getattr(self, '_handle_{0}_tag_start'.format(tag), self.NIL)
        callback(attrs)

        if tag in self.URL_TAGS:
            self.__find_tag_urls(attrs)

    def end(self, tag):
        tag = tag.lower()
        callback = getattr(self, '_handle_{0}_tag_end'.format(tag), self.NIL)
        callback()

    def comment(self, text):
        pass

    def data(self, data):
        pass

    def close(self):
        pass

    def __find_tag_urls(self, attrs):
        for name, value in attrs.items():
            if name.lower() in self.URL_ATTRS and value:
                url = self.__make_url(value)
                if url:
                    self.__urls_tag.add(url)

    def __make_url(self, url):
        if not url or url.startswith('javascript:'):
            return None

        if url.startswith('http'):
            return URL(url)
        else:
            return URL(urljoin(self.__base_url, url))

    def _handle_form_tag_start(self, attrs):
        self.__in_form = True
        method = attrs.get('method', 'GET').upper()
        name = attrs.get('name', '')
        action = attrs.get('action', self.__base_url)
        if action and not action.startswith('http'):
            action = urljoin(self.__base_url, action)

        form = Form(name, action, method)
        self.__forms.append(form)

    def _handle_form_tag_end(self):
        self.__in_form = False
        form = self.__forms[-1]
        url = form.action
        method = form.method
        data = form.data
        if method == 'GET':
            url = '{0}?{1}'.format(url, urlencode(data))
            data = None

        self.__requests.append(Request(url, method, data=data))

    def _handle_input_tag_start(self, attrs):
        side = 'inside' if self.__in_form else 'outside'
        callback = getattr(self, '_handle_input_tag_{0}'.format(side), self.NIL)
        callback(attrs)

    def _handle_input_tag_inside(self, attrs):
        form = self.__forms[-1]
        name = attrs.get('name', '')
        value = attrs.get('value', '')
        type_ = attrs.get('type', '').lower()
        form.push_data(name, value, type_)

    @property
    def parsed(self):
        return self.__parsed

    @property
    @parse
    def urls(self):
        return self.__urls_header | self.__urls_tag | self.__urls_re

    @property
    @parse
    def requests(self):
        return self.__requests
