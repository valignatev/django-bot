# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_commands'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Commands',
            new_name='Command',
        ),
    ]
