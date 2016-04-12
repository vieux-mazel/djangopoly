# -*- encoding: UTF-8 -*-
from django.db import models
from django.conf import settings
from pprint import pprint
import json
import board
import random, string

class Game(models.Model):
    private = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)

    def __str__(self):
        return "ID: {0}\nPrivate: {1}\nIn progress: {2}".format(
                self.pk, self.private, self.in_progress)

class Square(models.Model):
    position = models.IntegerField(default=0)
    game = models.ForeignKey(Game)
    title = models.CharField(default="Square", max_length=255)

    def __str__(self):
        return "Game ID: {0}\nPosition: {1}\nTitle: {2}".format(
                self.game.pk, self.position, self.title)

class Player(models.Model):
    joined = models.IntegerField(default=0)
    game = models.ForeignKey(Game)
    name = models.CharField(default="Player", max_length=255)
    money = models.IntegerField(default=15000)
    square = models.ForeignKey(Square)
    plays_in_turns = models.IntegerField(default=0)
    in_jail_for = models.IntegerField(default=0)
    rolled_this_turn = models.BooleanField(default=False)
    drew_card_this_turn = models.BooleanField(default=False)
    dice_left = models.IntegerField(default=1)
    free_move = models.IntegerField(default=0)
    free_buy = models.IntegerField(default=0)
    free_protection = models.IntegerField(default=0)
    has_moved_today = models.BooleanField(default=False)
    def is_in_jail(self):
        assert self.in_jail_for >=0 and self.in_jail_for <= 3, "Unexpected number of jail turns: {0}.".format(self.in_jail_for)
        return self.in_jail_for > 0

    def __str__(self):
        return "Game ID: {game}\nName: {name}\nMoney: {money}\nSquare: {square}\nPlays in turns: {plays}".format(
            game=self.game.pk,
            name=self.name,
            money=self.money,
            square=self.square.position,
            plays=self.plays_in_turns)
    def __unicode__(self):
        return self.name
    def can_free_buy(self):
        if self.free_buy > 0:
            return True
        return False
    def can_free_move(self):
        if self.free_move > 0:
            return True
        return False
    def is_protected(self):
        if self.free_protection > 0:
            return True
        return False
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

class Street(models.Model):
    color = models.CharField(max_length=16)
    game = models.ForeignKey(Game)

    def __str__(self):
        return "Game ID: {0}\nColor: {1}".format(
            self.game.pk, self.color)

class Property(models.Model):
    square = models.OneToOneField(Square)
    street = models.ForeignKey(Street)
    owned_by = models.ForeignKey(Player, null=True)
    price = models.IntegerField(default=0)
    tax_site = models.IntegerField(default=0)
    tax_1house = models.IntegerField(default=0)
    tax_2house = models.IntegerField(default=0)
    tax_3house = models.IntegerField(default=0)
    tax_4house = models.IntegerField(default=0)
    tax_hotel = models.IntegerField(default=0)
    build_house = models.PositiveSmallIntegerField(default=0)
    house_price = models.PositiveSmallIntegerField(default=0)
    house_sell_price = models.PositiveSmallIntegerField(default=0)
    mortgage_price = models.IntegerField(default=0)
    is_mortgaged = models.BooleanField(default=False)

    def __str__(self):
        return "Square: {0}\nOwned by: {1}\nStreet: {2}\nIs mortgaged: {3}".format(
            self.square.position, (self.owned_by.game.pk if self.owned_by is not None else "Nobody"), self.street.color, self.is_mortgaged)

class Utility(models.Model):
    square = models.OneToOneField(Square)
    owned_by = models.ForeignKey(Player, null=True)
    price = models.IntegerField(default=0)
    mortgage_price = models.IntegerField(default=0)
    is_mortgaged = models.BooleanField(default=False)
    tax_site = models.IntegerField(default=0)

    def __str__(self):
        return "Square: {0}\nOwned by: {1}\nIs mortgaged: {2}".format(
            self.square.position, (self.owned_by.game.pk if self.owned_by is not None else "Nobody"), self.is_mortgaged)

class Effect(models.Model):
    type = models.CharField(max_length=128, unique=True)
    param = models.IntegerField(default=0, null=True)

    def __str__(self):
        return "Type: {0}\nParam: {1}".format(
            self.type, self.param)


class Special(models.Model):
    square = models.OneToOneField(Square)
    effect = models.ForeignKey(Effect, null=True)

    def __str__(self):
        return "Square: {0}\nEffect: {1}".format(
            self.square.position, (self.effect.type if self.effect is not None else "None"))

class UserProfile(models.Model):
    django_user = models.OneToOneField(settings.AUTH_USER_MODEL,
        related_name='profile',
        primary_key=True)
    groupe = models.ForeignKey(Player)

    def __str__(self):
        return "Groupe {groupe} : {user}".format(
            groupe=self.groupe.name,
            user=self.django_user)

def my_random_key():

    return 'C' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))

EFFECTS = (
    ('g','givemoney'),
    ('a','adddice'),
    ('m', 'moveanywhere'),
    ('s','shield'),
    ('f','freebuy'),
)
class Code(models.Model):
    is_used = models.BooleanField(default=False)
    hash = models.CharField(max_length=10, default=my_random_key, unique=True)
    effect = models.CharField(max_length=1, choices=EFFECTS, default='g')

    def __unicode__(self):
        return "Cheat code, ID : {pk} , {hash}, {effect} ".format(pk=self.pk, hash=self.hash, effect=self.get_effect_display())
