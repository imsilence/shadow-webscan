#encoding: utf-8

from unittest import TestCase

from crawler.url import URL

class TestURL(TestCase):

    def test_scheme(self):
        url = URL('www.baidu.com')
        self.assertEquals('http', url.scheme)

    def test_port(self):
        url = URL('http://www.baidu.com:8080')
        self.assertEquals(8080, url.port)

    def test_path(self):
        url = URL('http://www.baidu.com:8080/test/')
        self.assertEquals('/test/', url.path)

    def test_query_string(self):
        url = URL('http://www.baidu.com:8080/test/?a=1&b=2')
        self.assertEquals('a=1&b=2', url.query_string)

    def test_fragment(self):
        url = URL('http://www.baidu.com:8080/test/?a=1&b=2#top')
        self.assertEquals('top', url.fragment)

    def test_https(self):
        url = URL('https://a:b@www.baidu.com:80/test/?a=b&c=d#fragment')
        self.assertEquals('https', url.scheme)