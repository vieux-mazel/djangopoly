# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(unique=True, max_length=128)),
                ('param', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('private', models.BooleanField(default=False)),
                ('in_progress', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('session_id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'Player', max_length=255)),
                ('money', models.IntegerField(default=0)),
                ('plays_in_turns', models.IntegerField(default=0)),
                ('game', models.ForeignKey(to='monopoly.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Square',
            fields=[
                ('position', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(default=b'Square', max_length=255)),
                ('game', models.ForeignKey(to='monopoly.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.ForeignKey(to='monopoly.Square'),
            preserve_default=True,
        ),
    ]
