# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150125_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=225)),
                ('content', models.TextField()),
                ('clicked', models.IntegerField(default=0)),
                ('goods', models.IntegerField(default=0)),
                ('bads', models.IntegerField(default=0)),
                ('is_top', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('cancomment', models.IntegerField(default=1)),
                ('comments', models.IntegerField(default=0)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='account.UserOJ')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
