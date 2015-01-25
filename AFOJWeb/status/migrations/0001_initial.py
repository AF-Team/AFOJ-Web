# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150125_0903'),
        ('problemlist', '0001_initial'),
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField(default=0)),
                ('memory', models.IntegerField(default=0)),
                ('in_date', models.DateTimeField(auto_now_add=True)),
                ('result', models.IntegerField(default=1)),
                ('language', models.IntegerField(default=0)),
                ('ip', models.CharField(max_length=15)),
                ('valid', models.IntegerField(default=1)),
                ('num', models.IntegerField(default=-1)),
                ('code_length', models.IntegerField(default=0)),
                ('judgetime', models.DateTimeField(null=True)),
                ('pass_rate', models.DecimalField(null=True, max_digits=3, decimal_places=2)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Compile_info',
            fields=[
                ('solution', models.ForeignKey(primary_key=True, serialize=False, to='status.Solution')),
                ('error', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source_code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.TextField()),
                ('solution', models.ForeignKey(to='status.Solution')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='solution',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solution',
            name='problem',
            field=models.ForeignKey(to='problemlist.Problem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solution',
            name='user',
            field=models.ForeignKey(to='account.UserOJ'),
            preserve_default=True,
        ),
    ]
