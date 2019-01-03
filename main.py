#encoding: utf-8

import logging
import urllib3

from crawler import Crawler

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    urllib3.disable_warnings()

    crawler = Crawler()
    crawler.crawl('http://zhidao.baidu.com/uteam?fr=daohang')

    print('-' * 20)
    f = open('urls.txt', 'wt', encoding='utf-8')
    for url in crawler.urls:
        print(url.url)
        f.write(url.url)
        f.write('\n')