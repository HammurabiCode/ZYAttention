import datetime
from django.db import models

# Create your models here.

class Player(models.Model):
    player_id = models.CharField(max_length=64, primary_key=True)
    pass


class Test(models.Model):
    date_time = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['-date_time']
        pass
            
    pass


class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    pass


        