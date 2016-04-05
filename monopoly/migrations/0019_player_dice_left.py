# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0018_auto_20160401_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='dice_left',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
