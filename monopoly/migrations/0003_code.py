# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import monopoly.models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0002_auto_20160406_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_used', models.BooleanField(default=False)),
                ('spy_hash', models.CharField(default=monopoly.models.my_random_key, unique=True, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
