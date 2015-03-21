# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0014_player_drew_card_this_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='street',
            name='id',
            field=models.AutoField(default=0, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='street',
            name='color',
            field=models.CharField(max_length=16),
        ),
    ]
