# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0007_auto_20150301_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='money',
            field=models.IntegerField(default=1500),
        ),
    ]
