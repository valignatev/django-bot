from django.db import models


class Human(models.Model):
    username = models.CharField(max_length=20, verbose_name='Представьтесь')


class Bot(models.Model):
    nickname = models.CharField(max_length=20)
    date = models.DateTimeField()
    message = models.TextField(verbose_name='Введите команду')

    def __str__(self):
        date = self.date.strftime('%d.%m.%Y %H:%M:%S')
        return ' '.join([date, self.nickname, ':', str(self.message)])


class Command(models.Model):
    command = models.CharField(max_length=255)
    method = models.CharField(max_length=100)

    def __str__(self):
        return self.command


class Queue(models.Model):
    command = models.ForeignKey(Command)
    user_param = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()
