from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserOJ(models.Model):
	user=models.OneToOneField(User,primary_key=True)
	submit=models.IntegerField(default=0)
	solved=models.IntegerField(default=0)
	team=models.IntegerField(default=1,max_length=2)
	realName=models.CharField(max_length=12)
	studentId=models.CharField(max_length=12)
	portrait=models.ImageField(upload_to="/")
	scoreOne=models.IntegerField(default=0)
	scoreTwo=models.IntegerField(default=0)
	def __unicode__(self):
		return self.user.username
class Privilege(models.Model):
    user = models.ForeignKey(UserOJ)
    authority = models.IntegerField()
    defunct = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.user.username + ' - authority - ' + str(self.authority)
