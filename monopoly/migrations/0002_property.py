# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0001_initial'),
    ]

    operations = [
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
                ('owned_by', models.ForeignKey(to='monopoly.Player')),
                ('square', models.OneToOneField(to='monopoly.Square')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
