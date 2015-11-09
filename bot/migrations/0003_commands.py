# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_bot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commands',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('command', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=100)),
            ],
        ),
    ]
