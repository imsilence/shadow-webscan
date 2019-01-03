#encoding: utf-8

import logging
import urllib3

from crawler import Crawler, DNS
from fingerprint import Finger

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    urllib3.disable_warnings()
    DNS.open_cache()

    url = 'https://lnmp.org/'
    finger = Finger()
    print(finger.scan(url))

    '''
    crawler = Crawler()
    crawler.crawl(url)

    print('-' * 20)
    f = open('urls.txt', 'wt', encoding='utf-8')
    for url in crawler.urls:
        print(url.url)
        f.write(url.url)
        f.write('\n')
    '''