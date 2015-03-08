from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from monopoly.models import Game, Square, Property, Utility, Special, Player
from board import board

# Placeholder index page
def index(request):
    return HttpResponse('Hello')

# Displays the game
def game(request, id):
    game = Game.objects.get(id=id)
    
    request.session['has_session'] = True # To ensure there is a session key
    session_id = request.session.session_key
    if session_id is None:
        return redirect('index') # There's no session. Incognito mode?
    
    # Try to find the player with this Session ID
    # If there isn't one, create her.
    try:
        player = Player.objects.get(session_id=session_id)
    except Player.DoesNotExist:
        player = Player(session_id=session_id, game=game, square=Square.objects.get(game=game, position=0))
        # If there are other players that have already joined, adjust plays_in_turns
        if len(Player.objects.filter(game=game)) > 0:
            player.plays_in_turns = Player.objects.filter(game=game).order_by('-plays_in_turns')[0].plays_in_turns + 1
        player.save()

    # This player exists, but she's playing another game.
    if player.game != game:
        return redirect('index')
    
    print player
    return HttpResponse(str(game.id) + ' ' + str(game.private))

# Create a new game
# Can be private or public, depends on URL invocation
def new_game(request, private):
    newGame = Game()
    newGame.private = True if private == "private" else False
    newGame.save()

    # Create game board
    # 40 squares that are either properties, utilities, or "specials"
    # Listed in board.py
    squares = []
    for x in sorted(board, key=lambda k: k['position']):
        square = Square(position=x['position'], game=newGame)
        identity = None # Identity of the square (property/utility/special)
        if x['type'] == 'property':
            identity = Property()
        elif x['type'] == 'utility':
            identity = Utility()
        elif x['type'] == 'special':
            identity = Special()
        square.title = x['title']
        square.save()
        identity.square = square
        identity.save()
        squares.append(square)

    # After creating the game, redirect to game view
    return redirect(game, id=newGame.id)

### API
# All requests return an empty string upon failure.
# On success, they return "ok" for content-empty responses
# or the requested contents otherwise.

FAILURE = json.dumps({'success': False})
SUCCESS = json.dumps({'success': True})

# Start a new game
def start_game(request, id):
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return HttpResponse(FAILURE)

    if game.in_progress is True:
        return HttpResponse(FAILURE)
    
    game.in_progress = True
    game.save()
    return HttpResponse(SUCCESS)

def roll_dice(request):
    try:
        player = Player.objects.get(session_id=request.session.session_key)
    except Player.DoesNotExist:
        return HttpResponse(FAILURE)

    # Roll two dice - will be random at some point
    dice1 = 2;
    dice2 = 4;

    # Calculate new player position
    new_position = (player.square.position + dice1 + dice2) % 40
    player.square = Square.objects.get(game=player.game, position=new_position)

    player.save()
    return HttpResponse(json.dumps(
        {
            'success': True,
            'dice1': dice1,
            'dice2': dice2,
            'square': player.square.position
        }))

