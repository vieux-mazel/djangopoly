# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0010_auto_20150311_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='in_jail_for',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
