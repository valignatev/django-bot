from django.db import models


class Human(models.Model):
    username = models.CharField(max_length=20, verbose_name='Представьтесь')


class Bot(models.Model):
    command = models.TextField(verbose_name='Введите команду')


class Command(models.Model):
    command = models.CharField(max_length=255)
    method = models.CharField(max_length=100)

    def __str__(self):
        return self.command
