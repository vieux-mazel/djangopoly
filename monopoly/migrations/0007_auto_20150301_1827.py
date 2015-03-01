# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0006_auto_20150301_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='special',
            name='effect',
            field=models.ForeignKey(to='monopoly.Effect', null=True),
        ),
    ]
