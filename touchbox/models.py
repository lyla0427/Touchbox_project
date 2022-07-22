from django.db import models


# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=64, null=True)
    initial = models.CharField(max_length=4, null=True)
    profile_pic = models.CharField(max_length=1024, null=True)
    number = models.IntegerField()
    season = models.IntegerField(null=True)
    most_touched_area = models.CharField(max_length=6, null=True)


class Competition(models.Model):
    name = models.CharField(max_length=64, null=True)
    matchdate = models.DateField()
    opponent = models.CharField(max_length=64, null=True)
    location = models.CharField(max_length=64, null=True)  # home/away
    wdl = models.CharField(max_length=1, null=True)
    season = models.IntegerField()


class TouchMap(models.Model):
    competition = models.ForeignKey("Competition", related_name="touchmap", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", related_name="touchmap", on_delete=models.CASCADE)
    playingtime = models.IntegerField()
    rating = models.FloatField()
    area1 = models.IntegerField()
    area2 = models.IntegerField()
    area3 = models.IntegerField()
    area4 = models.IntegerField()
    area5 = models.IntegerField()
    area6 = models.IntegerField()
    area7 = models.IntegerField()
    area8 = models.IntegerField()
    area9 = models.IntegerField()
    area10 = models.IntegerField()
    area11 = models.IntegerField()
    area12 = models.IntegerField()
    area13 = models.IntegerField()
    area14 = models.IntegerField()
    area15 = models.IntegerField()
    area16 = models.IntegerField()
    area17 = models.IntegerField()
    area18 = models.IntegerField()
    area19 = models.IntegerField()
    area20 = models.IntegerField()
    area21 = models.IntegerField()
    area22 = models.IntegerField()
    total = models.IntegerField()
