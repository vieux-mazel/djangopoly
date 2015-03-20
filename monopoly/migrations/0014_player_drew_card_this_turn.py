# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0013_player_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='drew_card_this_turn',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
