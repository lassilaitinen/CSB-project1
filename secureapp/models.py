import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Notice(models.Model):
    notice_title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.notice_title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
class Choice(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
class Comment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    commenttext = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.commenttext