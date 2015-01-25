from django.db import models
from account.models import *
# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    user=models.ForeignKey(UserOJ)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
    	return str(self.title)

class Notice(models.Model):
    content = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
