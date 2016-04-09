# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0003_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='effect',
            field=models.CharField(default=b'g', max_length=1, choices=[(b'g', b'givemoney'), (b'a', b'adddice'), (b'm', b'moveanywhere'), (b's', b'shield'), (b'f', b'freebuy')]),
            preserve_default=True,
        ),
    ]
