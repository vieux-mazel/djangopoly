# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monopoly', '0004_code_effect'),
    ]

    operations = [
        migrations.RenameField(
            model_name='code',
            old_name='spy_hash',
            new_name='hash',
        ),
    ]
