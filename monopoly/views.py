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

# Establishes a Session ID if one hasn't been established
#
# Because Django is magic, it doesn't create a session until AFTER
# a view has returned. If the 'game' view doesn't discover a session id
# it will redirect to 'join_game'. 'join_game' should discover the session id
# created by returning from 'game' and continue on rendering the game.
# If it doesn't discover anything, then the browser doesn't support sessions.
def join_game(request, id):
    session_id = request.session.session_key

    if session_id is None:
        return redirect('index') # There's no session. Incognito mode?

    return redirect('game', id)

# Displays the game
def game(request, id):
    game = Game.objects.get(id=id)
    
    session_id = request.session.session_key

    if session_id is None:
        return redirect('join_game', id)
    
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

    # After creating the game, redirect to game view
    return redirect(game, id=newGame.id)

### API
# All requests return an empty string upon failure.
# On success, they return "ok" for content-empty responses
# or the requested contents otherwise.

FAILURE = json.dumps({'success': False})
SUCCESS = json.dumps({'success': True})

# Player exists and can play decorator
def player_can_play(f):
    def wrap(request, *args, **kwargs):
        # Check that the player exists
        try:
            player = Player.objects.get(session_id=request.session.session_key)
        except Player.DoesNotExist:
            return HttpResponse(FAILURE)
        # Check that it is this player's turn
        if player.plays_in_turns != 0:
            return HttpResponse(FAILURE)
        return f(request, *args, **kwargs)

    # Black magic
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

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

@player_can_play
def roll_dice(request):
    player = Player.objects.get(session_id=request.session.session_key)

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
@player_can_play
def end_turn(request):
    player = Player.objects.get(session_id=request.session.session_key)

    # Get all players in this game, subtract one from plays_in_turns
    # (when it gets negative it resets to the maximum)
    players = player.game.player_set.all()
    for p in players:
        p.plays_in_turns = (p.plays_in_turns - 1) % len(players)
        p.save()

    return HttpResponse(SUCCESS)

# Buying a property or utility
@player_can_play
def buy(request, position):
    player = Player.objects.get(session_id=request.session.session_key)

    # Find the square at that position
    try:
        square = Square.objects.get(game=player.game, position=position)
    except Square.DoesNotExist:
        return HttpResponse(FAILURE)

    # Check if the square can be bought
    if not rules.buy(player, square):
        return HttpResponse(FAILURE)

    # Buying has succeeded
    return HttpResponse(SUCCESS)

# Pay a bailout when the player is in jail
# in order to become free.
@player_can_play
def pay_bailout(request):
    player = Player.objects.get(session_id=request.session.session_key)

    try:
        rules.pay_bailout(player)
    except AssertionError:
        return HttpResponse(FAILURE)

    return HttpResponse(SUCCESS)

# Return JSON containing all of the game's state
def game_state(request, id):
    # Find the game for which the state is requested
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return HttpResponse(FAILURE)

    players = game.player_set.all()
    for player in players:
        print player

    ss = []
    squares = game.square_set.all()
    for square in squares:
        s = {
            'id': square.id,
            'title': square.title,
            'type': rules.identify_square(square).__class__.__name__.lower()
        }

        t = rules.identify_square(square)
        print s['type']
        if s['type'] == 'property':
            s['owned_by'] = square.property.owned_by
            s['price'] = square.property.price

            s['tax_site'] = square.property.tax_site
            s['tax_1house'] = square.property.tax_1house
            s['tax_2house'] = square.property.tax_2house
            s['tax_3house'] = square.property.tax_3house
            s['tax_4house'] = square.property.tax_4house
            s['tax_hotel'] = square.property.tax_hotel

            s['mortgage_price'] = square.property.mortgage_price
            s['is_mortgaged'] = square.property.is_mortgaged
        
        elif s['type'] == 'utility':
            s['owned_by'] = square.utility.owned_by
            s['price'] = square.utility.price

            s['tax_site'] = square.utility.tax_site

            s['mortgage_price'] = square.utility.mortgage_price
            s['is_mortgaged'] = square.utility.is_mortgaged

        #print square.__dict__
        ss.append(s)
        
    state = json.dumps(ss, indent=4)

    # Use Django's serializer
    #state = serializers.serialize("dictionary",
    #    list(Game.objects.filter(id=id)) +
    #    list(Player.objects.filter(game=game)) +
    #    list(Square.objects.filter(game=game)) +
    #    list(Property.objects.filter(square__game=game)) +
    #    list(Utility.objects.filter(square__game=game)) +
    #    list(Special.objects.filter(square__game=game))
    #)

    # Echo the JSON as the response's body
    return HttpResponse(state)

