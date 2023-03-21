import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

'''
在这个投票应用中，需要创建两个模型：问题 Question 和选项 Choice。
Question 模型包括问题描述和发布时间。
Choice 模型有两个字段，选项描述和当前得票数。每个选项属于一个问题。
'''
class Question(models.Model):
    def __str__(self):
        return self.question_text
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    def __str__(self):
        return self.choice_text
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)