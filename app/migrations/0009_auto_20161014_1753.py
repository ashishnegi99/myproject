# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20161012_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racktestresult',
            name='Date',
            field=models.DateField(),
        ),
    ]
