# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('monopoly', '0015_auto_20150321_1837'),
    ]

    operations = [
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
    ]
