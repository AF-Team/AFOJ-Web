# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150125_0903'),
        ('problemlist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('private', models.IntegerField(default=0)),
                ('visible', models.BooleanField(default=False)),
                ('langmask', models.IntegerField(default=0)),
                ('mode', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to='account.UserOJ')),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contest_Privilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('user', models.ForeignKey(to='account.UserOJ')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contest_problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=200)),
                ('num', models.IntegerField()),
                ('sorce', models.IntegerField(default=10)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('problem', models.ForeignKey(to='problemlist.Problem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
