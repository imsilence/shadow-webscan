#encoding: utf-8

from unittest import TestCase

from crawler.form import Form


class TestForm(TestCase):

    def test_fill_value(self):

        form = Form('', '', '')
        self.assertEquals('webscan', form.fill_value('name', ''))
        self.assertEquals('kk', form.fill_value('name', 'kk'))