# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0004_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='owned_by',
            field=models.ForeignKey(to='monopoly.Player', null=True),
        ),
        migrations.AlterField(
            model_name='utility',
            name='owned_by',
            field=models.ForeignKey(to='monopoly.Player', null=True),
        ),
    ]
