#encoding: utf-8

from .browser import Browser

class AjaxCrawler(object):

    def crawl(self, url):
        browser = Browser()
        browser.init()
