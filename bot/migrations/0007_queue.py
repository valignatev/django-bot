# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_auto_20151109_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
