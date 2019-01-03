#encoding: utf-8

from functools import wraps

def parse(method):

    @wraps(method)
    def wrapper(object_, *args, **kwargs):
        if not object_.parsed:
            object_()

        return method(object_, *args, **kwargs)

    return wrapper
