# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privilege',
            name='id',
        ),
        migrations.AddField(
            model_name='useroj',
            name='portrait',
            field=models.ImageField(default=1, upload_to=b'/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='privilege',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to='account.UserOJ'),
            preserve_default=True,
        ),
    ]
