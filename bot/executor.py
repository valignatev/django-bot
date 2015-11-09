#! -*- coding: utf-8 -*-
import threading
import time
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
        phrase, timer = self.user_param.strip().split('через')
        count, measure = timer.strip().split(' ')
        if 'минут' in measure:
            count = int(count) * 60
        elif 'секунд' in measure:
            count = int(count)
        time.sleep(count)
        self.send_message('Напоминаю: {phrase}'.format(phrase=phrase))

    def get_all_titles(self):
        message = 'Заголовки {titles} с сайта {sites}'
        urls = self.user_param.strip().split(',')
        founds = []
        missings = []

        for url in urls:
            try:
                soup = self._get_html(url)
                founds.append((soup.title.text, url))
            except AttributeError:
                missings.append(('title на {url} отсутствует'.format(
                    url=self.user_param), url))
            except HTTPError as e:
                missings.append((e.msg, url))

        titles, sites = zip(*founds)
        message = message.format(titles=', '.join(titles),
                                 sites=', '.join(sites))
        self.send_message(message)

        for missing in missings:
            self.send_message(missing)
