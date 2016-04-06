import board
from .models import Game, Street, Property, Utility, Special, Square, Effect, Player
from django.conf import settings
from jchat.models import Room
from math import floor
@classmethod
def create(cls):
    newGame = cls()
    newGame.save()
    # Create game board
    # Streets
    for x in board.streets:
        street = Street(color=x['color'], game=newGame)
        street.save()

    # 40 squares that are either properties, utilities, or "specials"
    for x in sorted(board.squares, key=lambda k: k['position']):
        square = Square(position=x['position'], game=newGame)

        # Create square identity
        identity = None # Identity of the square (property/utility/special)
        if x['type'] == 'property':
            identity = Property()
            identity.street = Street.objects.get(color=x['street'], game=newGame)
            identity.tax_site = x['tax_site']
            identity.price = x['price']
            identity.tax_1house = floor(x['tax_site'] * 5)
            identity.tax_2house = floor(x['tax_site'] * 15)
            identity.tax_3house = floor(x['tax_site'] * 45)
            identity.tax_4house = floor(x['tax_site'] * 62.5)
            identity.tax_hotel = floor(x['tax_site'] * 75)
            identity.house_price = x['house_price']
        elif x['type'] == 'utility':
            identity = Utility()
            identity.price = x['price']
            identity.tax_site = x['tax_site']
        elif x['type'] == 'special':
            identity = Special()
            identity.effect, created = Effect.objects.get_or_create(type=x['effect']['type'], param=x['effect']['param'])
        assert identity is not None, "A square MUST have an identity that is Property, Utility or Special."
        square.title = x['title']
        square.save()
        identity.square = square
        identity.save()

    for i in settings.GROUP_NAMES:
        player = Player(game=newGame,
                         square=Square.objects.get(game=newGame, position=0),
                         name='Groupe %s' % i,
                         joined=len(newGame.player_set.all()),
                         dice_left = 2,
                         )
        player.save()
        r = Room.objects.get_or_create(player)
        r.save()
    r = Room.objects.get_or_create(newGame)
    r.is_commun = True
    r.save()

    return newGame

Game.add_to_class("create",create)
