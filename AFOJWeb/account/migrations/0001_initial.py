# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authority', models.IntegerField()),
                ('defunct', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserOJ',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('submit', models.IntegerField(default=0)),
                ('solved', models.IntegerField(default=0)),
                ('team', models.IntegerField(default=1, max_length=2)),
                ('realName', models.CharField(max_length=12)),
                ('studentId', models.CharField(max_length=12)),
                ('scoreOne', models.IntegerField(default=0)),
                ('scoreTwo', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='privilege',
            name='user',
            field=models.ForeignKey(to='account.UserOJ'),
            preserve_default=True,
        ),
    ]
