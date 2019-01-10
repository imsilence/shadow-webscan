#encoding: utf-8

import logging
import urllib3

from crawler import Crawler, DNS, Request
from fingerprint import Finger
from scanner import Scanner

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    urllib3.disable_warnings()
    DNS.open_cache()

    url = 'http://testphp.vulnweb.com/index.php'
    url = 'https://www.baidu.com'
    finger = Finger()
    print(finger.scan(url))


    crawler = Crawler()
    crawler.crawl(url)

    print('-' * 20)


    print('url count:', len(crawler.urls))
    f = open('urls.txt', 'wt', encoding='utf-8')
    for url in crawler.urls:
        print(url.raw_url)
        for vul in Scanner.check(url):
            print(vul)

        f.write(url.raw_url)
        f.write('\n')


