#encoding: utf-8

import logging
import urllib3

from crawler import Crawler

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    urllib3.disable_warnings()

    crawler = Crawler()
    crawler.crawl('www.baidu.com')

    print('-' * 20)
    for url in crawler.urls:
        print(url.url)