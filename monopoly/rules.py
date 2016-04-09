"""Models the rules of the board game Monopoly.

Consists mainly of functions that model the game flow
and reflect changes in the game state to the database.

Ideally, all game logic should go in this module and be referred
to from the API in views.py
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import random

from monopoly.models import Game, Player, Square, Property, Utility, Special
from board import squares, streets

def roll_dice():
    """Roll two dice randomly

    Returns:
        Tuple of the form (int, int)
    """
    return (random.randint(1, 6), random.randint(1, 6))


def move_player(player, dice):
    """Attempt moving a player according to a dice roll.

    The player will not be moved if he's in jail. Otherwise, he'll be moved
    by the sum of the two dice and game logic will be run according to the type
    of square he lands on.

    Args:
        player: Player
        dice: (int, int)
    """
    assert len(dice) == 2, "Unexpected number of dice rolls. Should be exactly two."

    if not player.is_in_jail(): # Move the player only if she's not in jail
        new_position = (player.square.position + dice[0] + dice[1]) % len(squares)
    else:
        new_position = player.square.position
        handle_jail(player, dice)

    player.square = Square.objects.get(game=player.game, position=new_position)
    player.save()

    identity = identify_square(player.square)

    # Handle different types of squares
    if isinstance(identity, Special):
        assert identity.effect is not None, "A special square doesn't have an effect"
        apply_effect(player, identity.effect)

    elif isinstance(identity, Property) or isinstance(identity, Utility):
        assert identity.owned_by is None or isinstance(identity.owned_by, Player), "The property/utility is owned by a non-Player object?"
        #assert identity.owned_by is None or Player.objects.filter(session_id=identity.owned_by.session_id, game=player.game).exists(), "The property/utility is owned by an invalid player or someone from another game."

        # The identity is not owned by anyone. Nothing
        # special happens, although the player can buy it.
        if identity.owned_by is None:
            pass
        # The player has landed on his own identity,
        # nothing special happens
        elif identity.owned_by == player:
            pass
        # The player has landed on another player's
        # mortgaged property/utility, nothing special happens.
        elif identity.owned_by != player and identity.is_mortgaged:
            pass
        # The player has landed on another player's
        # unmortgaged property/utility, and should pay rent.
        elif identity.owned_by != player and not identity.is_mortgaged:
            pay_rent(player, identity.owned_by, get_rent(identity))

    else:
        assert False, "Identity of a square is not Special, Property or Utility."

def can_be_bought(player, square):
    """Determine whether a square can be bought by a player.

    See buying for the rules.

    Args:
        player: Player
        square: Square

    Returns:
        True if possible, False otherwise.
    """
    identity = identify_square(square)
    if isinstance(identity, Special): # The square is special, so it can't be bought
        return False

    if identity.owned_by != None: # The square is owned by someone else
        return False

    if player.money < identity.price: # The player doesn't have enough money to buy the square
        return False

    # The square is a property, and another property of the same street (color) is owned by another player
    #if isinstance(identity, Property) and identity.street.property_set.filter(~Q(owned_by=player) & ~Q(owned_by=None)):
    #    return False

    return True

def buy(player, square):
    """Buys a square on behalf of a player.

    Buying can fail if:
        o) The square is special.
        o) The square is owned by someone else.
        o) The player doesn't have enough money to buy it.
        o) Another player owns a property of the same color.

    Args:
        player: Player
        square: Square

    Returns:
        True upon success, False otherwise.
    """
    if not can_be_bought(player, square):
        return False
    # Do the transaction
    identity = identify_square(square)
    take_money(player, identity.price)
    identity.owned_by = player
    identity.save()
    # It has succeeded
    return True


def can_be_mortgaged(player, square):
    """Determines whether a square can be mortgaged by a player.

    See mortgaging for the rules.

    Args:
        player: Player
        square: Square

    Returns:
        True if possible, False otherwise.
    """
    identity = identify_square(square)
    if isinstance(identity, Special):
        return False # Can't mortgage a special square.

    if identity.owned_by != player:
        return False # The square is not owned by the player.

    if identity.is_mortgaged:
        return False

    #if player.plays_in_turns != 0:
    #    return False

    return True
def can_be_unmortgaged(player, square):
    identity = identify_square(square)
    if isinstance(identity, Special):
        return False # Can't mortgage a special square.

    if identity.owned_by != player:
        return False # The square is not owned by the player.

    if not identity.is_mortgaged:
        return False

    if player.money < identity.price :
        return False
    return True


def mortgage(player, square):
    """Mortgages a property/utility on
    behalf of a player.

    Mortgaging will fail if the property is not owned by the player.

    Args:
        player: Player
        square: Square

    Returns:
        True upon success, False otherwise.
    """
    if not can_be_mortgaged(player, square):
        return False

    identity = identify_square(square)
    identity.is_mortgaged = True
    identity.save()
    give_money(player, identity.price)
    return True

def unmortgage(player, square):
    if not can_be_unmortgaged(player, square):
        return False

    identity = identify_square(square)
    identity.is_mortgaged = False
    identity.save()
    take_money(player, identity.price)
    return True


def get_rent(identity):
    """Determines the rent due on a property or utility.

    Args:
        identity: Property or Utility

    Returns:
        rent: int
    """
    if isinstance(identity, Property): # If it's a property, the rent is the tax site.
        if identity.build_house == 0:
            return identity.tax_site
        elif identity.build_house == 1:
            return identity.tax_1house
        elif identity.build_house == 2:
            return identity.tax_2house
        elif identity.build_house == 3:
            return identity.tax_3house
        elif identity.build_house == 4:
            return identity.tax_4house
        elif identity.build_house == 5:
            return identity.tax_hotel
        elif identity.build_house > 5:
            return identity.tax_hotel
        else:
            return identity.tax_site
    elif isinstance(identity, Utility): # If it's a utitlity, the rent depends on how many other utilities are owned by the same player.
        if identity.owned_by is None:
            return identity.tax_site
        else:
            return identity.tax_site * identity.owned_by.utility_set.all().count()
    else:
        assert False, "Tried to determine rent on a special square"


def apply_effect(player, effect):
    """Applies an effect onto a player.

    Args:
        player: Player
        effect: Effect
    """
    # Give money to a player
    if effect.type == "give_money":
        give_money(player, effect.param)
    elif effect.type == "take_money":
        take_money(player, effect.param)
    elif effect.type == "income_tax":
        take_money(player, 200) # Pay a flat rate of 200
    elif effect.type == "supertax":
        take_money(player, 100) # Pay a flat rate of 100
    elif effect.type == "go_to_jail":
        go_to_jail(player)
    elif effect.type == "move":
        player.square = Square.objects.get(game=player.game, position=effect.param)
        player.save()
        move_player(player, (0,0))


def give_money(player, cash):
    """Gives money to a player.

    Args:
        player: Player
        cash: int, cash > 0
    """
    assert isinstance(cash, (int, long)), "Cash is not an integer."
    assert cash > 0, "Can't give non-positive cash to a player."
    player.money = player.money + cash
    player.save()


def take_money(player, cash):
    """Takes money from a player.

    Args:
        player: Player
        cash: int, cash > 0
    """
    assert isinstance(cash, (int, long)), "Cash is not an integer."
    assert cash > 0, "Can't take non-positive cash from a player."
    player.money = (player.money - cash) if (player.money - cash > 0) else 0
    player.save()


def pay_rent(payer, payee, cash):
    """Takes a sum of money from one player and gives it to another as rent payment.

    Args:
        payer: Player
        payee: Player
        cash: int, cash > 0
    """
    take_money(payer, cash)
    give_money(payee, cash)


def go_to_jail(player):
    """Sends a player to jail for 3 turns.

    Args:
        player: Player
    """
    player.square = Square.objects.get(game=player.game, position=10) # Hardcoded jail position, probably shouldn't be like that
    player.in_jail_for = 3 # In jail for 3 turns
    player.save()


def handle_jail(player, dice):
    """Determines what to do with a player when he's in jail.

    If in jail for 2 or 3 more turns, to get out he either pays 50 or rolls doubles.
    If in jail for 1 more turn, always pay 50.

    Args:
        player: Player, player.is_in_jail() is True
        dice: (int, int)
    """
    assert player.is_in_jail(), "A player is not in jail, yet handle_jail() was called."
    if player.in_jail_for == 2 or player.in_jail_for == 3:
        if dice[0] == dice[1]:
            liberate(player) # Player rolled doubles, he's free.
            return
    if player.in_jail_for == 1:
        pay_bailout(player)
        return
    player.in_jail_for -= 1
    player.save()


def liberate(player):
    """Sets a player free (not in jail anymore).

    Args:
        player: Player
    """
    player.in_jail_for = 0
    player.save()


def pay_bailout(player):
    """Pays bailout on behalf of a player.

    Pays 50 to the bank and sets him free.

    Args:
        player: Player, player.is_in_jail() is True
    """
    assert player.is_in_jail(), "A player is not in jail, yet pay_bailout() was called."
    take_money(player, 50)
    liberate(player)


def can_draw_card(player):
    """Determines whether a player can draw a card.

    Only if he's on a community chest or chance square.

    Args:
        player: Player

    Returns:
        True if possible, False otherwise.
    """
    identity = identify_square(player.square)
    if not isinstance(identity, Special):
        return False

    if identity.effect.type != "community_chest" and identity.effect.type != "chance":
        return False

    if not player.rolled_this_turn:
        return False

    if player.drew_card_this_turn:
        return False

    return True
def can_build_house(square,player):
    identity = None
    type = squares[square.position]['type']
    if type == 'property':
        property = square.property
    else:
        return False
    for p in property.street.property_set.all():
        if p.owned_by != player:
            return False
    if player.money >= property.house_price:
        return True
    return False

    #if (len(street.property_set) == Property.objects.filter(street.own=street).count() and player.money > property.house_price and ):
    #    return True
    #else:
    #    return False

def identify_square(square):
    """Determines a square's identity.

    Args:
        square: Square

    Returns:
        identity: Property, Utility or Special
    """
    identity = None
    
    type = squares[square.position]['type']
    if type == 'property':
        identity = square.property
    elif type == 'special':
        identity = square.special
    elif type == 'utility':
        identity = square.utility

    '''
    try:
        identity = square.special
    except ObjectDoesNotExist:
        pass
    try:
        identity = square.property
    except ObjectDoesNotExist:
        pass
    try:
        identity = square.utility
    except ObjectDoesNotExist:
        pass
    '''
    assert identity is not None, "Couldn't determine square identity."
    return identity
