#encoding: utf-8

from unittest import TestCase

from crawler.curl import Curl


class TestCurl(TestCase):

    def test_get(self):
        curl = Curl()
        response = curl.get('http://www.baidu.com')
        self.assertEquals(response.status_msg, 'OK')