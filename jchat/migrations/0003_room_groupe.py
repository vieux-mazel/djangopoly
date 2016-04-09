# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0002_auto_20160406_1510'),
        ('jchat', '0002_room_is_commun'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='groupe',
            field=models.ForeignKey(blank=True, to='monopoly.Player', null=True),
            preserve_default=True,
        ),
    ]
