# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jchat.models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0019_player_dice_left'),
        ('jchat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spy_code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('spy_hash', models.CharField(default=jchat.models.my_random_key, unique=True, max_length=10)),
                ('first_used', models.DateTimeField(null=True, blank=True)),
                ('linked_room', models.ForeignKey(blank=True, to='jchat.Room', null=True)),
                ('used_by', models.ForeignKey(blank=True, to='monopoly.Player', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='room',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 5, 15, 9, 14, 955637)),
            preserve_default=True,
        ),
    ]
