# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0012_player_rolled_this_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='joined',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
