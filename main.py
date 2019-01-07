#encoding: utf-8

import logging
import urllib3

from crawler import Crawler, DNS, Request
from fingerprint import Finger
from scanner import SQL

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
    f = open('urls.txt', 'wt', encoding='utf-8')
    sql = SQL()

    for url in crawler.urls:
        print(sql.check(Request(url)))
        f.write(url.raw_url)
        f.write('\n')


