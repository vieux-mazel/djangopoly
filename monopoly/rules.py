# Game rules
from django.core.exceptions import ObjectDoesNotExist

from monopoly.models import Game, Player, Square, Property, Utility, Special

from board import squares, streets

# Rolling dice by Monopoly rules
def roll_dice():
    return (2, 4)

# Handle moving a player to a new square
def move_player(player, dice):
    assert len(dice) == 2, "Unexpected number of dice rolls. Should be exactly two." 
    new_position = (player.square.position + dice[0] + dice[1]) % len(squares)
    player.square = Square.objects.get(game=player.game, position=new_position)
    player.save()

    identity = identify_square(player.square)

    # Handle different types of squares
    if isinstance(identity, Special):
        assert identity.effect is not None, "A special square doesn't have an effect"
        apply_effect(player, identity.effect)

    elif isinstance(identity, Property) or isinstance(identity, Utility):
        # At this point, the property is certainly owned by someone
        assert identity.owned_by is None or isinstance(identity.owned_by, Player), "The property/utility is owned by a non-Player object?"
        assert identity.owned_by is None or Player.objects.filter(session_id=identity.owned_by.session_id, game=player.game).exists(), "The property/utility is owned by an invalid player or someone from another game."

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

# Buys a square on behalf of player
# Returns True upon success and False upon failure
def buy(player, square):

    identity = identify_square(square)

    if isinstance(identity, Special): # The square is special, so it can't be bought
        return False
    
    if identity.owned_by != None: # The square is owned by someone else
        return False

    if player.money < identity.price: # The player doesn't have enough money to buy the square
        return False

    # Do the transaction
    take_money(player, identity.price)
    identity.owned_by = player
    identity.save()
    # It has succeeded
    return True

# Apply an effect to a player
def apply_effect(player, effect):
    # Give money to a player
    print effect.type
    if effect.type == "give_money":
        give_money(player, effect.param)
    elif effect.type == "income_tax":
        take_money(player, 200) # Pay a flat rate of 200
    elif effect.type == "supertax":
        take_money(player, 100) # Pay a flat rate of 100
    elif effect.type == "go_to_jail":
        go_to_jail(player)

def give_money(player, cash):
    assert isinstance(cash, int), "Cash is not an integer."
    assert cash > 0, "Can't give non-positive cash to a player."
    player.money = player.money + cash
    player.save()

def take_money(player, cash):
    assert isinstance(cash, int), "Cash is not an integer."
    assert cash > 0, "Can't take non-positive cash from a player."
    player.money = (player.money - cash) if (player.money - cash > 0) else 0
    player.save()

def pay_rent(payer, payee, cash):
    take_money(payer, cash)
    give_money(payee, cash)

def go_to_jail(player):
    player.square = Square.objects.get(game=player.game, position=10) # Hardcoded jail position, probably shouldn't be like that
    # Should also prevent the player from moving subsequent turns
    player.save()

# Determine identity of square
def identify_square(square):
    identity = None
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
    assert identity is not None, "Couldn't determine square identity."
    return identity

# Determine how much rent is to be payed on a property/utility
def get_rent(identity):
    if isinstance(identity, Property):
        return identity.tax_site
    elif isinstance(identity, Utility):
        if identity.owned_by is None:
            return identity.tax_site
        else:
            return identity.tax_site * identity.owned_by.utility_set.all().count()
    else:
        assert False, "Tried to determine rent on a special square"

