#encoding: utf-8

import uuid

class Response(object):

    DEFAULT_STATUS_MSG = 'OK'

    def __init__(self, status_code=None, status_msg=DEFAULT_STATUS_MSG,
        headers=None, body='', request_url=None, uid=None, charset=None):

        self.__status_code = status_code
        self.__status_msg = status_msg
        self.__headers = headers
        self.__body = body
        self.__request_url = request_url
        self.__uid = uid if uid else str(uuid.uuid1())
        self.__charset = charset

    @property
    def status_code(self):
        return self.__status_code

    @property
    def status_msg(self):
        return self.__status_msg

    @property
    def headers(self):
        return {k.lower():v for k,v in self.__headers.items()} \
                if self.__headers else {}

    @property
    def body(self):
        return self.__body

    @property
    def request_url(self):
        return self.__request_url

    @property
    def uid(self):
        return self.__uid

    @property
    def charset(self):
        return self.__charset

    @property
    def cookies(self):
        return self.headers.get('set-cookie', None)

    def __repr__(self):
        return '<{0!r}>{1!r}'.format(self.__class__.__name__, vars(self))
