# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(unique=True, max_length=128)),
                ('param', models.IntegerField(default=0, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('joined', models.IntegerField(default=0)),
                ('name', models.CharField(default=b'Player', max_length=255)),
                ('money', models.IntegerField(default=25000)),
                ('plays_in_turns', models.IntegerField(default=0)),
                ('in_jail_for', models.IntegerField(default=0)),
                ('rolled_this_turn', models.BooleanField(default=False)),
                ('drew_card_this_turn', models.BooleanField(default=False)),
                ('dice_left', models.IntegerField(default=1)),
                ('game', models.ForeignKey(to='monopoly.Game')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(default=0)),
                ('tax_site', models.IntegerField(default=0)),
                ('tax_1house', models.IntegerField(default=0)),
                ('tax_2house', models.IntegerField(default=0)),
                ('tax_3house', models.IntegerField(default=0)),
                ('tax_4house', models.IntegerField(default=0)),
                ('tax_hotel', models.IntegerField(default=0)),
                ('mortgage_price', models.IntegerField(default=0)),
                ('is_mortgaged', models.BooleanField(default=False)),
                ('owned_by', models.ForeignKey(to='monopoly.Player', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('effect', models.ForeignKey(to='monopoly.Effect', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Square',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(default=0)),
                ('title', models.CharField(default=b'Square', max_length=255)),
                ('game', models.ForeignKey(to='monopoly.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=16)),
                ('game', models.ForeignKey(to='monopoly.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('django_user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('groupe', models.ForeignKey(to='monopoly.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Utility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(default=0)),
                ('mortgage_price', models.IntegerField(default=0)),
                ('is_mortgaged', models.BooleanField(default=False)),
                ('tax_site', models.IntegerField(default=0)),
                ('owned_by', models.ForeignKey(to='monopoly.Player', null=True)),
                ('square', models.OneToOneField(to='monopoly.Square')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='special',
            name='square',
            field=models.OneToOneField(to='monopoly.Square'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='property',
            name='square',
            field=models.OneToOneField(to='monopoly.Square'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='property',
            name='street',
            field=models.ForeignKey(to='monopoly.Street'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='square',
            field=models.ForeignKey(to='monopoly.Square'),
            preserve_default=True,
        ),
    ]
