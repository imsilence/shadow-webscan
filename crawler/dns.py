#encoding: utf-8

import socket

class DNS(object):
    __cached = {}
    __getaddrinfo = None

    @classmethod
    def open_cache(cls):
        if cls.__getaddrinfo is not None:
            return
        cls.__getaddrinfo = socket.getaddrinfo

        def getaddrinfo(*args, **kwargs):
            rt = cls.__cached.get(args)
            if rt is None:
                rt = cls.__getaddrinfo(*args, **kwargs)
                cls.__cached[args] = rt
            return rt

        socket.getaddrinfo = getaddrinfo

    @classmethod
    def close_cache(cls):
        if cls.__getaddrinfo is None:
            return

        socket.getaddrinfo = cls.__getaddrinfo
        cls.__getaddrinfo = None
