# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'monopoly', '0001_initial'), (b'monopoly', '0002_property'), (b'monopoly', '0003_utility'), (b'monopoly', '0004_special'), (b'monopoly', '0005_auto_20150301_1737'), (b'monopoly', '0006_auto_20150301_1823'), (b'monopoly', '0007_auto_20150301_1827'), (b'monopoly', '0008_auto_20150308_1455'), (b'monopoly', '0009_auto_20150309_2045'), (b'monopoly', '0010_auto_20150311_1650'), (b'monopoly', '0011_player_in_jail_for'), (b'monopoly', '0012_player_rolled_this_turn'), (b'monopoly', '0013_player_joined'), (b'monopoly', '0014_player_drew_card_this_turn'), (b'monopoly', '0015_auto_20150321_1837'), (b'monopoly', '0016_userprofile'), (b'monopoly', '0017_auto_20160401_1455'), (b'monopoly', '0018_auto_20160401_1731'), (b'monopoly', '0019_player_dice_left'), (b'monopoly', '0020_auto_20160405_1940'), (b'monopoly', '0021_auto_20160405_1949')]

    dependencies = [
        ('auth', '0001_initial'),
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
                ('square', models.OneToOneField(to='monopoly.Square')),
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
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('effect', models.ForeignKey(to='monopoly.Effect', null=True)),
                ('square', models.OneToOneField(to='monopoly.Square')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='player',
            old_name='position',
            new_name='square',
        ),
        migrations.AddField(
            model_name='square',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='square',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='money',
            field=models.IntegerField(default=1500),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('color', models.CharField(max_length=16)),
                ('game', models.ForeignKey(to='monopoly.Game')),
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
        migrations.AlterField(
            model_name='effect',
            name='param',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='in_jail_for',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='rolled_this_turn',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='joined',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='drew_card_this_turn',
            field=models.BooleanField(default=False),
            preserve_default=True,
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
        migrations.RemoveField(
            model_name='player',
            name='session_id',
        ),
        migrations.AddField(
            model_name='player',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
        migrations.AddField(
            model_name='player',
            name='dice_left',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='money',
            field=models.IntegerField(default=25000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
            preserve_default=True,
        ),
    ]
