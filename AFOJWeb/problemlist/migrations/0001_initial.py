# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('problem_id', models.IntegerField(max_length=10, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('pro_input', models.TextField(null=True)),
                ('pro_output', models.TextField(null=True)),
                ('sample_input', models.TextField(null=True)),
                ('sample_output', models.TextField(null=True)),
                ('spj', models.IntegerField(default=0, max_length=1)),
                ('hint', models.TextField(blank=True)),
                ('source', models.CharField(max_length=100, null=True, blank=True)),
                ('in_date', models.DateTimeField(auto_now_add=True)),
                ('time_limit', models.IntegerField(max_length=1)),
                ('memory_limit', models.IntegerField(max_length=1)),
                ('visible', models.BooleanField(default=False)),
                ('defunct', models.BooleanField(default=False, max_length=1)),
                ('submit', models.IntegerField(default=0, max_length=1)),
                ('solved', models.IntegerField(default=0, max_length=1)),
                ('difficulty', models.IntegerField(default=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Problem_Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'/')),
                ('problem', models.ForeignKey(to='problemlist.Problem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=20)),
                ('score', models.IntegerField(default=200)),
                ('problem', models.OneToOneField(to='problemlist.Problem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
