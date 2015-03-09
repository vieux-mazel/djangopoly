# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0008_auto_20150308_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Street',
            fields=[
                ('color', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('game', models.ForeignKey(to='monopoly.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='property',
            name='street',
            field=models.ForeignKey(default='black', to='monopoly.Street'),
            preserve_default=False,
        ),
    ]
