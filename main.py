#encoding: utf-8
from crawler.curl import Curl
from crawler.parser import HTMLParser

if __name__ == '__main__':

    curl = Curl()
    response = curl.get('www.baixxxdu.com')

    parser = HTMLParser(response)
    parser.parse()
    print(len(parser.urls))

