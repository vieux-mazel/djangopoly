from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
import json

from monopoly.models import Game, Square, Property, Utility, Special, Player, Street, Effect

import board
import rules

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
    return render(request, 'board.html')

# Create a new game
# Can be private or public, depends on URL invocation
def new_game(request, private):
    newGame = Game()
    newGame.private = True if private == "private" else False
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
            identity.street = Street.objects.get(color=x['street']) 
            identity.tax_site = x['tax_site']
        elif x['type'] == 'utility':
            identity = Utility()
        elif x['type'] == 'special':
            identity = Special()
            identity.effect, created = Effect.objects.get_or_create(type=x['effect']['type'], param=x['effect']['param'])
        assert identity is not None, "A square MUST have an identity that is Property, Utility or Special."

        square.title = x['title']
        square.save()
        identity.square = square
        identity.save()

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

    # Check that it is this player's turn
    if player.plays_in_turns != 0:
        return HttpResponse(FAILURE)

    # Roll two dice - will be random at some point
    (dice1, dice2) = rules.roll_dice();

    # Handle player movement
    rules.move_player(player, (dice1, dice2))

    player.save()
    return HttpResponse(json.dumps(
        {
            'success': True,
            'dice1': dice1,
            'dice2': dice2,
            'square': player.square.position
        }))

# End a turn, and adjust plays_in_turns for every player
def end_turn(request):
    try:
        player = Player.objects.get(session_id=request.session.session_key)
    except Player.DoesNotExist:
        return HttpResponse(FAILURE)

    # Check that it is this player's turn
    if player.plays_in_turns != 0:
        return HttpResponse(FAILURE)

    # Get all players in this game, subtract one from plays_in_turns
    # (when it gets negative it resets to the maximum)
    players = player.game.player_set.all()
    for p in players:
        p.plays_in_turns = (p.plays_in_turns - 1) % len(players)
        p.save()

    return HttpResponse(SUCCESS)

# Return JSON containing all of the game's state
def game_state(request, id):
    # Find the game for which the state is requested
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return HttpResponse(FAILURE)

    # Use Django's serializer
    state = serializers.serialize("json",
        list(Game.objects.filter(id=id)) +
        list(Player.objects.filter(game=game)) +
        list(Square.objects.filter(game=game)) +
        list(Property.objects.filter(square__game=game)) +
        list(Utility.objects.filter(square__game=game)) +
        list(Special.objects.filter(square__game=game))

    )

    # Echo the JSON as the response's body
    return HttpResponse(state)
