import board
from .models import Game, Street, Property, Utility, Special, Square, Effect, Player, Code
from django.conf import settings
from jchat.models import Room, Spy_code
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
        multiplicator = [5,15,45,62.5,75]
        if x['type'] == 'property':
            identity = Property()
            identity.street = Street.objects.get(color=x['street'], game=newGame)
            identity.tax_site = x['tax_site']
            identity.price = x['price']
            if x['position'] > 15:
                multiplicator = [5,15,40,50,65]
            if x['position'] > 20:
                multiplicator = [5,15,37.5,46.25,55]
            if x['position'] > 30:
                multiplicator = [5,15,34,42.3,50]
            if x['position'] > 34:
                multiplicator = [4,12,28,34,40]
            identity.tax_1house = floor(x['tax_site'] * multiplicator[0])
            identity.tax_2house = floor(x['tax_site'] * multiplicator[1])
            identity.tax_3house = floor(x['tax_site'] * multiplicator[2])
            identity.tax_4house = floor(x['tax_site'] * multiplicator[3])
            identity.tax_hotel = floor(x['tax_site'] * multiplicator[4])
            identity.house_price = x['house_price']
            identity.house_sell_price = x['house_price']/2 # prix de vente d'une maison
            identity.mortgage_price = x['price'] * 1.1 # prix pour dehypothequer
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
        r.groupe = player
        r.save()
    try:
        Spy_code.objects.get(pk=1)
    except Spy_code.DoesNotExist:
        for i in range(20):
            s = Spy_code()
            s.save()
    try:
        Code.objects.get(pk=1)
    except Code.DoesNotExist:
        for i in range(20):
            c = Code()
            c.effect = 'g' #give money code
            c.save()
        for i in range(20):
            c = Code()
            c.effect = 'a' # add 1 dice code
            c.save()
        for i in range(15):
            c = Code()
            c.effect = 'm' # Move anywhere code
            c.save()
        for i in range(10):
            c = Code()
            c.effect = 's' # Shield code
            c.save()
        for i in range(10):
            c = Code()
            c.effect = 'f' # Free buy code
            c.save()

    r = Room.objects.get_or_create(newGame)
    r.is_commun = True
    r.save()

    return newGame

Game.add_to_class("create",create)
