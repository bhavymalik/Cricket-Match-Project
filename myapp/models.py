from django.db import models

# Create your models here.
# I modelled it as a 50-50 match where 2 teams play 2 innings 


class match(models.Model):
    runs= models.IntegerField(null=True)
    wickets= models.IntegerField(null=True)
    balls= models.IntegerField(null=True)
    wideballs = models.IntegerField(null=True)
    batsman= models.CharField(max_length=70)
    bawler= models.CharField(max_length=70)
    battingteam= models.CharField(max_length=70)
    bawlingteam = models.CharField(max_length=70)
    innings = models.IntegerField(default=1)
    team1runs = models.IntegerField(default=0)
    team1wickets = models.IntegerField(default=0)
