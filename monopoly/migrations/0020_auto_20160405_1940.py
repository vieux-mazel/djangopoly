# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0019_player_dice_left'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='money',
            field=models.IntegerField(default=25000),
            preserve_default=True,
        ),
    ]
