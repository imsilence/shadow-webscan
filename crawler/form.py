#encoding: utf-8

import logging

logger = logging.getLogger(__name__)

class Form(object):

    def __init__(self, name, action, method):
        self.__name = name
        self.__action = action
        self.__method = method
        self.__data = []

    @property
    def action(self):
        return self.__action

    @property
    def method(self):
        return self.__method

    @property
    def data(self):
        return self.__data

    def push_data(self, name, value, type):
        self.__data.append((name, self.fill_value(name, value)))

    def fill_value(self, name, value):
        if value:
            return value

        name = name.lower()
        if name in ['user', 'username', 'uname', 'name', 'nickname']:
            return 'webscan'
        elif name in ['password', 'pwd', 'pass', 'passwd']:
            return 'abc1234.C'
        elif name in ['mail', 'email', 'usermail']:
            return 'test@webscan.com'
        elif name in ['tel', 'telphone', 'phone']:
            return '15200000000'
        elif name in ['context', 'text', 'query', 'search',
            'data', 'comment', 'q', 'searchfor']:
            return 'test'
        elif name in ['domain', 'website']:
            return 'www.test.com'
        elif name in ['url', 'link']:
            return 'http://www.test.com'
        elif name in ['page', 'number', 'size', 'index']:
            return 2
        elif name in ['age']:
            return 28

        logger.info('fill value error, not found: %s', name)
        return 'unkonw'