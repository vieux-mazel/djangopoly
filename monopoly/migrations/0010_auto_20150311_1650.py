# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0009_auto_20150309_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effect',
            name='param',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
