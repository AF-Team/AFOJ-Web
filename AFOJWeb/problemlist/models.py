from django.db import models

# Create your models here.
class Problem(models.Model):
	problem_id=models.IntegerField(max_length=10,primary_key=True) 	
	title=models.CharField(max_length=50)
	description=models.TextField()
	pro_input=models.TextField()
	pro_output=models.TextField()
	sample_input=models.TextField()
	sample_output=models.TextField()
	spj=models.IntegerField(default=0,max_length=1)
	hint=models.TextField(blank=True)
	source=models.CharField(max_length=100,blank=True)
	in_date=models.DateTimeField()
	time_limit=models.IntegerField(max_length=1)
	memory_limit=models.IntegerField(max_length=1)
	visible=models.BooleanField(default=False)
	defunct=models.BooleanField(default=False,max_length=1)
	submit=models.IntegerField(default=0,max_length=1)
	solved=models.IntegerField(default=0,max_length=1)
	mark=models.IntegerField(default=5)
	difficulty=models.IntegerField(default=2)
	def  __unicode__(self):
		return u"%s -%s" % (self.title,self.title)
		# return must unicode rather than int 


