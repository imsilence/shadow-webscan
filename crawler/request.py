#encoding: utf-8

from .config import DEFAULT_USER_AGENT
from .url import URL

class Request(object):

    DEFAULT_METHOD = 'GET'

    def __init__(self, url, method=DEFAULT_METHOD, headers=None, cookies=None,
                    referer=None, data=None, user_agent=DEFAULT_USER_AGENT,
                    **kwargs):

        if not isinstance(url, URL):
            url = URL(url)

        self.__url = url
        self.__method = method.upper()
        self.__headers = headers if headers else {}
        self.__cookies = cookies
        self.__referer = referer
        self.__user_agent = user_agent
        self.__query_string = url.query_string
        self.__data = data

        if self.__referer:
            self.__headers['Referer'] = self.__referer

        if self.__user_agent:
            self.__headers['User-Agent'] = self.__user_agent

        if self.__cookies:
            self.__headers['Cookie'] = self.__cookies

    @property
    def url(self):
        return self.__url

    @property
    def method(self):
        return self.__method

    @property
    def headers(self):
        return self.__headers

    @property
    def cookies(self):
        return self.__cookies

    @property
    def referer(self):
        return self.__referer

    @property
    def user_agent(self):
        return self.__user_agent

    @property
    def query_string(self):
        return self.__query_string

    @property
    def data(self):
        return self.__data

    def __repr__(self):
        return '<{0}>{1}'.format(self.__class__.__name__, vars(self))
