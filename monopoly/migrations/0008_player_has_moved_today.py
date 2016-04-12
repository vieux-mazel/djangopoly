# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0007_auto_20160411_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='has_moved_today',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
