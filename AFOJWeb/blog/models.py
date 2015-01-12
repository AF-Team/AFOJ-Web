  # -*- coding: utf-8 -*-
from django.db import models
from account.models import *
# Create your models here.

class Blog(models.Model):
	user=models.ForeignKey(UserOJ)
	title=models.CharField(max_length=225)
	content=models.TextField()
	clicked=models.IntegerField(default=0)
	goods=models.IntegerField(default=0)
	bads=models.IntegerField(default=0)
	is_top=models.IntegerField(default=0) # 置顶 1置顶；0否
	status=models.IntegerField(default=1)# 1发布；0草稿;2虚删
  	cancomment = models.IntegerField(default=1)        # 是否可以评论，1可；0不可
	comments = models.IntegerField(default=0)             # 评论数量
	add_time=models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return "%s-%s" %(self.title,self.user.user.username)