from django.db import models
from account.models import *
from problemlist.models import *
# Create your models here.

class Contest(models.Model):
    title = models.CharField(max_length=255, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    defunct = models.BooleanField(default=False)
    description = models.TextField()
    private = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    langmask = models.IntegerField(default=0)
    #mode 0 -> acm, 1->OI
    mode = models.IntegerField(default=0)
    user = models.ForeignKey(UserOJ)
    
    def start_or_not(self):
        return self.start_time <= timezone.now()

    def end_or_not(self):
        return self.end_time > timezone.now()

    def __unicode__(self):
         return "%s-%s-%s" %(str(self.id),self.title,self.user.user.username)

    class Meta:
        # db_table = 'contest'
        ordering = ['-id']
class Contest_problem(models.Model):
    problem = models.ForeignKey(Problem)
    contest = models.ForeignKey(Contest)
    title = models.CharField(max_length=200, default='')
    num = models.IntegerField(default=0)
    sorce = models.IntegerField()
    
    def __unicode__(self):
        return "%s-%s-%s" %(str(self.id),self.problem.title,str(self.problem.id))
class Contest_Privilege(models.Model):
    user = models.ForeignKey(UserOJ)
    contest = models.ForeignKey(Contest)
    def __unicode__(self):
    	return "%s-%s" %(self.user.user.username,self.contest.title)

