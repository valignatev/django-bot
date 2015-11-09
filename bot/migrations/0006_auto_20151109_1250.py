# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20151109_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
