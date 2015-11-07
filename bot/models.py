from django.db import models


class Human(models.Model):
    username = models.CharField(max_length=20, verbose_name='Представьтесь')


class Bot(models.Model):
    command = models.TextField(verbose_name='Введите команду')

