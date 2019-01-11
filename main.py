#encoding: utf-8

import logging
import urllib3

from crawler import Crawler, DNS, Request
from fingerprint import Finger
from vulnerability import Manager

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    stream = open('logs/main.log', 'w', encoding="utf-8")
    logging.basicConfig(
        level=logging.DEBUG,
        stream=stream
    )

    urllib3.disable_warnings()
    DNS.open_cache()

    url = 'http://testphp.vulnweb.com/index.php'
    url = 'https://www.baidu.com'
    url = 'http://127.0.0.1:8000/'
    finger = Finger()
    print('finger:', finger.scan(url))

    crawler = Crawler()
    crawler.crawl(url)

    print('-' * 20)


    print('url count:', len(crawler.urls))
    f = open('logs/urls.txt', 'wt', encoding='utf-8')

    for url in crawler.urls:
        print(url.raw_url)
        f.write(url.raw_url)
        f.write('\n')

    manager = Manager()
    print('request count:', len(crawler.requests))
    for request in crawler.requests:
        for vul in manager.check(request):
            print(vul)

    manager.clear()