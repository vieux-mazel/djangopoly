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

class Property(models.Model):
    square = models.OneToOneField(Square)
    owned_by = models.ForeignKey(Player)
    price = models.IntegerField(default=0)
    tax_site = models.IntegerField(default=0)
    tax_1house = models.IntegerField(default=0)
    tax_2house = models.IntegerField(default=0)
    tax_3house = models.IntegerField(default=0)
    tax_4house = models.IntegerField(default=0)
    tax_hotel = models.IntegerField(default=0)
    mortgage_price = models.IntegerField(default=0)
    is_mortgaged = models.BooleanField(default=False)

    def __str__(self):
        return unicode(pprint(vars(self)))

class Utility(models.Model):
    square = models.OneToOneField(Square)
    owned_by = models.ForeignKey(Player)
    price = models.IntegerField(default=0)
    mortgage_price = models.IntegerField(default=0)
    is_mortgaged = models.BooleanField(default=False)
    tax_site = models.IntegerField(default=0)

    def __str__(self):
        return unicode(pprint(vars(self)))

class Effect(models.Model):
    type = models.CharField(max_length=128, unique=True)
    param = models.IntegerField(default=0)

    def __str__(self):
        return unicode(pprint(vars(self)))
