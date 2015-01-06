from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class users(models.Model):
	user=models.ForeignKey(User, unique=True)
	submit=models.IntegerField(default=0)
	solved=models.IntegerField(default=0)
	team=models.IntegerField(default=1,max_length=2)
	nickName=models.CharField(max_length=32)
	motto=models.CharField(max_length=300)
	realName=models.CharField(max_length=12)
	studentId=models.CharField(max_length=12)
	scoreOne=models.IntegerField(default=0)
	scoreTwo=models.IntegerField(default=0)
	def __unicode__(self):
		return self.user