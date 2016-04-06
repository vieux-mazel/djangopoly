# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='build_house',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='property',
            name='house_price',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
