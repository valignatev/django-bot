# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20151109_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='command',
            new_name='message',
        ),
        migrations.AddField(
            model_name='bot',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 9, 12, 17, 33, 77407, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bot',
            name='nickname',
            field=models.CharField(max_length=20, default='Бот'),
            preserve_default=False,
        ),
    ]
