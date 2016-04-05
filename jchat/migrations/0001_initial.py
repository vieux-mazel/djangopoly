# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jchat.models


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1, choices=[(b's', b'system'), (b'a', b'action'), (b'm', b'message'), (b'j', b'join'), (b'l', b'leave'), (b'n', b'notification')])),
                ('message', models.CharField(max_length=255, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('comment', models.TextField(null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(to='jchat.Room'),
            preserve_default=True,
        ),
    ]
