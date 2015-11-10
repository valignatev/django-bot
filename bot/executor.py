#! -*- coding: utf-8 -*-
from functools import reduce
import threading
import time
from urllib.request import urlopen, HTTPError

from django.utils import timezone

from bs4 import BeautifulSoup
from omnibus.api import publish

from .models import Bot, Storage


def deep_getattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    return reduce(getattr, attr.split('.'), obj)


class Executor:

    def __init__(self, method, user_param, human):
        self.method = getattr(self, method)
        self.user_param = user_param
        self.human = human

    def _get_html(self, url):
        page = urlopen(url)
        return BeautifulSoup(page, 'html.parser')

    def _get_content(self, content, url):
        try:
            soup = self._get_html(self.user_param)
            result = deep_getattr(soup, content)
            if not result:
                raise AttributeError
        except AttributeError:
            result = \
                'Запрашиваемая информация на {url} отсутствует'.format(url=url)
        except HTTPError as e:
            result = '{url} отвечает с ошибкой: {e}'.format(url=url, e=e.msg)
        return result

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

    def get_title(self, send=True):
            title = self._get_content('title.text', self.user_param)
            if send:
                self.send_message(title)
            return title, self.user_param

    def get_h1(self, send=True):
        h1 = self._get_content('body.h1.text', self.user_param)
        if send:
            self.send_message(h1)
        return h1, self.user_param

    def save_info(self):
        if self.user_param:
            Storage.objects.create(info=self.user_param)
        self.send_message('Информация сохранена')

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
            self.user_param = url
            title, _ = self.get_title(send=False)
            if ('Запрашиваемая информация на' in title and
                    'отсутствует' in title) or 'отвечает с ошибкой' in title:
                missings.append((title, url))
            else:
                founds.append((title, url))

        titles, sites = zip(*founds)
        message = message.format(titles=', '.join(titles),
                                 sites=', '.join(sites))
        self.send_message(message)

        for missing in missings:
            self.send_message(missing)
