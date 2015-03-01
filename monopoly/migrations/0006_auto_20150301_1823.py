# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0005_auto_20150301_1737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='position',
            new_name='square',
        ),
        migrations.AddField(
            model_name='square',
            name='id',
            field=models.AutoField(default=0, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='square',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
