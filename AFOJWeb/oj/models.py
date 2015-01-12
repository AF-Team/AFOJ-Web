from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Notice(models.Model):
    content = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
