# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_set_top_box'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set_top_box',
            name='VMS_02',
            field=models.CharField(max_length=30),
        ),
    ]
