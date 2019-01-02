#encoding: utf-8

from unittest import TestCase


from crawler.curl import Curl
from crawler.page_404 import Page404


class TestPage404(TestCase):

    def test_status_code_404(self):
        page404 = Page404()
        curl = Curl()
        response = curl.get('https://blog.csdn.net/fffffffffffff')
        print(response.status_code)
        self.assertTrue(page404.is_404(response))


    def test_body(self):
        page404 = Page404()
        curl = Curl()
        response = curl.get('http://github.com/imsilence/test/')
        print(response.status_code)
        self.assertTrue(page404.is_404(response))