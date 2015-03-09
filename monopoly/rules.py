# Game rules
from monopoly.models import Game, Player, Square, Property, Utility, Special

from board import squares, streets

# Rolling dice by Monopoly rules
def roll_dice():
    return (2, 4)

# Handle moving a player to a new square
def move_player(player, dice):
    new_position = (player.square.position + dice[0] + dice[1]) % len(squares)
    player.square = Square.objects.get(game=player.game, position=new_position)

