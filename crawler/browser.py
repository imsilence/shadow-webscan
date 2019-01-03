#encoding: utf-8

import os

from selenium import webdriver

from gconf import BIN_DIR

class Page(object):

    def __init__(self, ''):
        self._data = ''

    @property
    def urls(self):
        return []

    @property
    def events(self):
        return []



class Browser(object):

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        exec_path = os.path.join(BIN_DIR, 'bin', 'chromedriver.exe')
        self.__dirver = webdriver.Chrome(executable_path=exec_path,
                                            options=options)

    def open(self, url):
        self.__dirver.get(url)


    def do(self, event):
        return Page('')