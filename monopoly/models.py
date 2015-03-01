from django.db import models
from pprint import pprint

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    private = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)

    def __str__(self):
        return unicode(pprint(vars(self)))

class Square(models.Model):
    position = models.IntegerField(primary_key=True)
    game = models.ForeignKey(Game)
    title = models.CharField(default="Square", max_length=255)

    def __str__(self):
        return unicode(pprint(vars(self)))

class Player(models.Model):
    session_id = models.CharField(primary_key=True, max_length=32)
    game = models.ForeignKey(Game)
    name = models.CharField(default="Player", max_length=255)
    money = models.IntegerField(default=0)
    position = models.ForeignKey(Square)
    plays_in_turns = models.IntegerField(default=0)

    def __str__(self):
        return unicode(pprint(vars(self)))

class Effect(models.Model):
    type = models.CharField(max_length=128, unique=True)
    param = models.IntegerField(default=0)

    def __str__(self):
        return unicode(pprint(vars(self)))
