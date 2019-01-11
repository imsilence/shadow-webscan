#encoding: utf-8

import logging

from crawler import Request

from .packed import Packed

logger = logging.getLogger(__name__)

class Scanner(object):
    PLUGINS = {}

    NIL = lambda *args, **kwargs: []

    @classmethod
    def check(cls, url):
        for name, plugin in cls.PLUGINS.items():
            logger.debug('plugin: %s check %s', name, url)
            check = getattr(plugin(), 'check', cls.NIL)
            yield from check(Request(url))

    @classmethod
    def check_packed(cls, url):
        check = getattr(Packed(), 'check', cls.NIL)
        return check(Request(url))


def register(name):
    def wrapper(cls):
        Scanner.PLUGINS[name] = cls
        return cls
    return wrapper

