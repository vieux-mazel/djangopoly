# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0017_auto_20160401_1455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
    ]
