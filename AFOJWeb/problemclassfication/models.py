#encoding=utf-8
from django.db import models

from account import *
# Create your models here.
class Category(models.Model):
	""""""
	user=models.ForeignField(UserOJ)
	parent_id=models.IntegerField(default=0)#父节点id
	title=models.CharField(max_length=100) #分类名
	define=models.CharField(max_length=255)#分类描述
	sequence=models.IntegerField(default=1)#排序
	count=models.IntegerField(default=0)#该分类下有多少题目
	add_time=models.DateTimeField(auto_now=True,auto_now_add=True)#添加时间
	def __unicode__(self):
		return "%s-%s" %(self.title,self.user.user.username)