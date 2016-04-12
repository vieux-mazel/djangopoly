# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0006_property_house_sell_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='free_buy',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='free_move',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='free_protection',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='money',
            field=models.IntegerField(default=15000),
            preserve_default=True,
        ),
    ]
