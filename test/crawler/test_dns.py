#encoding: utf-8

from unittest import TestCase
import time
import socket

from crawler.dns import DNS


class TestDNS(TestCase):

    def test_open(self):
        DNS.open_cache()
        stime = time.time()
        for _ in range(1000):
            socket.getaddrinfo('www.baidu.com', 80)

        interval = time.time() - stime

        self.assertLess(interval, 0.1)

    def test_close(self):
        DNS.close_cache()
        stime = time.time()
        for _ in range(1000):
            socket.getaddrinfo('www.baidu.com', 80)

        interval = time.time() - stime

        self.assertGreater(interval, 0.5)