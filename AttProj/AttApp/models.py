import datetime
from django.db import models

# Create your models here.
'''
'''
class Device(models.Model):
    dev_no = models.CharField(max_length=64, primary_key=True)
    pass


class Student(models.Model):
    stu_no = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    pass


class StuDevMap(models.Model):
    stu = models.ForeignKey(Student, on_delete=models.CASCADE)
    dev = models.ForeignKey(Device, on_delete=models.CASCADE)
    pass


class Test(models.Model):
    date_time = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['-date_time']


class ReactionTime(models.Model):
    stu = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    dev = models.ForeignKey(Device, on_delete=models.SET(None), default=None)
    pass


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024)
    answer = models.PositiveIntegerField()
    options_str = models.CharField(max_length=1024) 

    def getOptions(self):
        return self.options_str.split('\n')
    pass


class QuizTest(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)


class QuizAnswer(models.Model):
    stu = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz_test = models.ForeignKey(QuizTest, on_delete=models.CASCADE)
    choice = models.PositiveIntegerField()
    time = models.PositiveIntegerField()
    dev = models.ForeignKey(Device, on_delete=models.SET(None), default=None)
