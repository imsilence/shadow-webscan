#encoding: utf-8

import logging
import urllib3

from crawler import Crawler, DNS

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    urllib3.disable_warnings()
    DNS.open_cache()

    crawler = Crawler()
    crawler.crawl('http://testphp.vulnweb.com/')

    print('-' * 20)
    f = open('urls.txt', 'wt', encoding='utf-8')
    for url in crawler.urls:
        print(url.url)
        f.write(url.url)
        f.write('\n')