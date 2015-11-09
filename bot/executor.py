#! -*- coding: utf-8 -*-
import threading
from urllib.request import urlopen, HTTPError

from django.utils import timezone

from bs4 import BeautifulSoup
from omnibus.api import publish

from .models import Bot

class Executor:

    def __init__(self, method, user_param):
        self.method = getattr(self, method)
        self.user_param = user_param

    def _get_html(self, url):
        page = urlopen(url)
        return BeautifulSoup(page, 'html.parser')

    def send_message(self, message):
        message = Bot.objects.create(message=message, date=timezone.now(),
                                     nickname='Бот').__str__()
        publish(
            'mychannel',
            'message',
            {'message': message},
            sender='server'
        )

    def execute(self):
        threading.Thread(target=self.method).start()
        return 'Принял задачу на обработку'

    def get_title(self):
        try:
            soup = self._get_html(self.user_param)
            self.send_message(soup.title.text)
        except AttributeError:
            self.send_message('title на {url} отсутствует'.format(
                url=self.user_param))
        except HTTPError as e:
            self.send_message(e.msg)

    def get_h1(self):
        try:
            soup = self._get_html(self.user_param)
            self.send_message(soup.body.h1.text)
        except AttributeError:
            self.send_message('h1 на {url} отсутствует'.format(
                url=self.user_param))
        except HTTPError as e:
            self.send_message(e.msg)

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
