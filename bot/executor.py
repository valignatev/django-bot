#! -*- coding: utf-8 -*-
try:
    from urllib.request import urlopen, HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError

from bs4 import BeautifulSoup


class Executor():

    def __init__(self, method, user_param):
        self.method = getattr(self, method)
        self.user_param = user_param

    def _get_html(self, url):
        page = urlopen(url)
        return BeautifulSoup(page, 'html.parser')

    def execute(self):
        return self.method()

    def get_title(self):
        try:
            soup = self._get_html(self.user_param)
            return soup.title.text
        except AttributeError:
            return 'title на {url} отсутствует'.format(url=self.user_param)
        except HTTPError as e:
            return e.msg

    def get_h1(self):
        try:
            soup = self._get_html(self.user_param)
            return soup.body.h1.text
        except AttributeError:
            return 'h1 на {url} отсутствует'.format(url=self.user_param)
        except HTTPError as e:
            return e.msg

    def save_info(self):
        pass

    def remind(self):
        pass

    def get_all_titles(self):
        urls = self.user_param.strip().split(',')
        titles = []
        for url in urls:
            self.user_param = url
            titles.append(self.get_title())
        return titles
