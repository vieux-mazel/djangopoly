# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0002_property'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(default=0)),
                ('mortgage_price', models.IntegerField(default=0)),
                ('is_mortgaged', models.BooleanField(default=False)),
                ('tax_site', models.IntegerField(default=0)),
                ('owned_by', models.ForeignKey(to='monopoly.Player')),
                ('square', models.OneToOneField(to='monopoly.Square')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
