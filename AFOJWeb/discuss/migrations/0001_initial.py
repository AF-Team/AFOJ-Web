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
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('problem', models.ForeignKey(to='problemlist.Problem')),
                ('user', models.ForeignKey(to='account.UserOJ')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reply',
            name='Topic',
            field=models.ForeignKey(to='discuss.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(to='account.UserOJ'),
            preserve_default=True,
        ),
    ]
