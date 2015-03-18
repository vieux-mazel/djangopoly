# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0011_player_in_jail_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='rolled_this_turn',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
