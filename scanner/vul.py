#encoding: utf-8

class Vulnerability(object):

    def __init__(self, name, rank, url, method, key, playload):
        self.__name = name
        self.__rank = rank
        self.__url = url
        self.__method = method
        self.__key = key
        self.__playload = playload

    def __repr__(self):
        return '<{0!r}>{1!r}'.format(self.__class__.__name__, vars(self))