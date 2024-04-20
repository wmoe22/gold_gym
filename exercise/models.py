from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass



class Exercises(models.Model):
    DIFFICULTY = [
        ('easy','Easy'),
        ('medium','medium'),
        ('hard','Hard')
    ]

    id = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=300)
    bodyPart = models.CharField(max_length=200)
    equipment = models.CharField(max_length=300)
    gifUrl = models.URLField()
    target = models.CharField(max_length=100)
    secondaryMuscles = models.JSONField(default=list)
    instructions = models.JSONField(default=list)
    saved = models.ManyToManyField(User,related_name="save_exc",blank=True,null=True)
    completed = models.ManyToManyField(User,related_name="complete_exercise",blank=True,null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY,blank=True,null=True)

    def __str__(self):
        return self.name
    

class Streak(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.DateField()
    current_streak = models.IntegerField(default=0,max_length=6)
    longest_day_streak = models.CharField(default=0,max_length=6)

    def __str__(self):
        return f"{self.user.username}'s streak"
    