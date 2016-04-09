# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0005_auto_20160408_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='house_sell_price',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
