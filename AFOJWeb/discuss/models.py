  # -*- coding: utf-8 -*-
from django.db import models
from problemlist.models import *
from account.models import *
# Create your models here.
class Topic(models.Model):
	problem=models.ForeignKey(Problem)
	user=models.ForeignKey(UserOJ)
	time=models.DateTimeField(auto_now_add=True)
	content=models.TextField()

class Reply(models.Model):
	Topic=models.ForeignKey(Topic)
	user=models.ForeignKey(UserOJ)
	time=models.DateTimeField(auto_now_add=True)
	content=models.TextField()

