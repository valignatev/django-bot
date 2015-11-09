# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='user_param',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='queue',
            name='command',
            field=models.ForeignKey(to='bot.Command'),
        ),
    ]
