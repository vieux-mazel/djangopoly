import board
from .models import Game, Street, Property, Utility, Special, Square, Effect


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
    return newGame


Game.add_to_class("create",create)