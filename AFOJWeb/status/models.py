from django.db import models
from problemlist.models import *
from contest.models import *
from account.models import *

# Create your models here.
class Solution(models.Model):
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(UserOJ)
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    in_date = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(default=0)
    language = models.IntegerField(default=0)
    ip = models.CharField(max_length=15)
    contest = models.ForeignKey(Contest, null=True)
    valid = models.IntegerField(default=1)
    num = models.IntegerField(default=-1)
    code_length = models.IntegerField(default=0)
    judgetime = models.DateTimeField(null=True)
    pass_rate = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    ######

    class Meta:
        # db_table = 'solution'
        ordering = ['-id']
    def __unicode__(self):
         return "%s-%s-%s" %(str(self.problem.id),self.problem.title, self.user.user.username)


class Compile_info(models.Model):
    solution = models.ForeignKey(Solution, primary_key=True)
    error = models.TextField()

class Source_code(models.Model):
    solution = models.ForeignKey(Solution)
    source  = models.TextField()