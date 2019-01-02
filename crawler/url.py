#encoding: utf-8
from functools import wraps

from urllib.parse import urlparse, parse_qs

def parse(method):

    @wraps(method)
    def wrapper(object_, *args, **kwargs):
        if not object_.parsed:
            object_.parse_url()

        return method(object_, *args, **kwargs)

    return wrapper


class URL(object):

    DEFAULT_PORTS = {
        'http' : 80,
        'https' : 443,
    }

    DEFAULT_ENCODING = 'utf-8'

    def __init__(self, url, encoding=DEFAULT_ENCODING):
        self.__url = url
        self.__encoding = encoding
        self.__scheme = 'http'
        self.__username = ''
        self.__password = ''
        self.__hostname = ''
        self.__port = 80
        self.__netloc = ''
        self.__path = ''
        self.__parameters = ''
        self.__query = ''
        self.__fragment = ''
        self.__parsed = False

    def parse_url(self):
        if self.__parsed:
            return

        self.__parsed = True
        url = self.__url
        if not url.startswith('http') and not url.startswith('https'):
            url = '{0}://{1}'.format(self.__scheme, url)
            self.__url = url

        result = urlparse(url)
        self.__scheme = result.scheme
        self.__username = result.username
        self.__password = result.password
        self.__hostname = result.hostname

        self.__netloc = result.netloc
        self.__port = result.port

        if result.port is None:
            self.__port = self.DEFAULT_PORTS.get(self.__scheme)
            self.__netloc = '{0}:{1}'.format(self.__netloc, self.__port)

        self.__path = result.path
        self.__parameters = result.params
        self.__query_string = result.query
        self.__fragment = result.fragment

    @property
    def parsed(self):
        return self.__parsed

    @property
    @parse
    def url(self):
        return self.__url

    @property
    @parse
    def scheme(self):
        return self.__scheme

    @property
    @parse
    def hostname(self):
        return self.__hostname

    @property
    @parse
    def port(self):
        return self.__port

    @property
    @parse
    def path(self):
        return self.__path

    @property
    @parse
    def filename(self):
        return self.__path.rpartition('/')[-1]

    @property
    @parse
    def fileext(self):
        pos = self.file.name.rfind('.')
        return self.filename[pos+1:] if pos > 0 else ''

    @property
    @parse
    def query_string(self):
        return self.__query_string

    @property
    @parse
    def fragment(self):
        return self.__fragment

    @parse
    def __repr__(self):
        return '<{0!r}>{1!r}'.format(self.__class__.__name__, vars(self))
