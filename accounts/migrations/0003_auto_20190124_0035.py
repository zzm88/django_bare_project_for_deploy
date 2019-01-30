# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_myprofile_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='credit',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
