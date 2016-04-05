from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
import json
import random, string


from monopoly.models import Game, Square, Property, Utility, Special, Player, Street, Effect, UserProfile

import board
import rules

def my_random_key():
    return ''.join(random.choice(string.digits) for _ in range(4))

# Placeholder index page
@login_required
def index(request):
    game = Game.objects.first()
    if (game is None):
        game = Game.create()
        game.save()
    try:
        user = request.user.profile.groupe
    except UserProfile.DoesNotExist:
        g = Player.objects.annotate(num_players=Count('userprofile')).order_by('num_players') # get the smalest group (monopoly player)
        u = request.user # get django user
        profil = UserProfile()
        profil.django_user = u
        profil.groupe = g[0] # assign new user to the smallest team
        profil.save()
        u.username = '%s_%s' % (g[0].name[6:], my_random_key())
        u.save()
    return render(request, 'index.html', {'game_id':game.pk})

def help(request):
    return render(request, 'help.html')

# Establishes a Session ID if one hasn't been established
#
# Because Django is magic, it doesn't create a session until AFTER
# a view has returned. If the 'game' view doesn't discover a session id
# it will redirect to 'join_game'. 'join_game' should discover the session id
# created by returning from 'game' and continue on rendering the game.
# If it doesn't discover anything, then the browser doesn't support sessions.
@login_required
def join_game(request, id):
    return redirect('game', id)

# Displays the game
@login_required
def game(request, id):
    game = Game.objects.get(id=id)

    # Try to find the player with this Session ID
    # If there isn't one, create her.
    try:
        player = request.user.profile.groupe
    except UserProfile.DoesNotExist:
        return redirect('index') # Disallow joining games in progress

    # This player exists, but she's playing another game.
    if player.game != game:
        return redirect('index')

    return render(request, 'board.html',{'groupe':player,'player':request.user})

# Create a new game
# Can be private or public, depends on URL invocation
@staff_member_required
def new_game(request, private):
    newGame = Game.create()
    newGame.save()
    return redirect(game, id=newGame.id)

# Make someone join a random public game that's not started
# This is called from the home page
@staff_member_required
def join_random_game(request):
    if Game.objects.filter(private=False, in_progress=False).count() == 0:
        return redirect(new_game, private="no") # Create a new public game if there are none

    random_game = random.choice(list(Game.objects.filter(private=False, in_progress=False)))
    return redirect(game, id=random_game.id)

# Leave a game
@staff_member_required
def leave(request):
    try:
        player = Player.objects.filter(session_id=request.session.session_key)
        player.delete()
    except:
        pass
    return redirect(index)

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
            player = request.user.profile.groupe
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
    player = request.user.profile.groupe

    # Lock the game - shouldn't be like that
    game = player.game
    game.in_progress = True
    game.save()

    # Roll two dice - will be random at some point
    (dice1, dice2) = rules.roll_dice();

    # Can't roll more than once (except when it's a double)
    if player.rolled_this_turn:
        return HttpResponse(FAILURE)

    # If it's a double, the player can roll twice.
    if dice1 != dice2:
        player.rolled_this_turn = True
        player.save()

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
    player = request.user.profile.groupe

    # Make sure the player can roll the next turn
    player.rolled_this_turn = False
    player.save()

    # Make sure the player can draw a card next turn
    player.drew_card_this_turn = False
    player.save()

    # Get all players in this game, subtract one from plays_in_turns
    # (when it gets negative it resets to the maximum)
    players = player.game.player_set.all()
    for p in players:
        p.plays_in_turns = (p.plays_in_turns - 1) % len(players)
        p.save()

    return HttpResponse(SUCCESS)

# Buying a property or utility
@player_can_play
def buy(request):
    player = request.user.profile.groupe
    square = player.square

    # Check if the square can be bought
    if not rules.buy(player, square):
        return HttpResponse(FAILURE)

    # Buying has succeeded
    return HttpResponse(SUCCESS)

# Pay a bailout when the player is in jail
# in order to become free.
@player_can_play
def pay_bailout(request):
    player = request.user.profile.groupe

    try:
        rules.pay_bailout(player)
    except AssertionError:
        return HttpResponse(FAILURE)

    return HttpResponse(SUCCESS)

# Mortgage a property belonging to the player
@player_can_play
def mortgage(request):
    player = request.user.profile.groupe
    square = player.square
    
    if not rules.mortgage(player, square):
        return HttpResponse(FAILURE)

    return HttpResponse(SUCCESS)

# Draw a card
@player_can_play
def draw_card(request):
    player = request.user.profile.groupe

    if not rules.can_draw_card(player):
        return HttpResponse(FAILURE)
    
    card = random.choice(board.cards)
    player.drew_card_this_turn = True
    player.save()

    rules.apply_effect(player, Effect(type=card["effect"]["type"], param=card["effect"]["param"]))

    return HttpResponse(json.dumps({
        'success': True,
        'name': card["name"],
        'description': card["description"],
        }))

# Return JSON containing all of the game's state
@login_required
def game_state(request, id):
    try:
        current_player = request.user.profile.groupe
    except UserProfile.DoesNotExist:
        return HttpResponse(FAILURE)

    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return HttpResponse(FAILURE)

    # Players list of Python dictionaries
    # instead of a list of Django objects
    pp = []
    players = game.player_set.all()
    for player in players:
        p = {
            'name': player.name,
            'money': player.money,
            'plays_in_turns': player.plays_in_turns,
            'in_jail_for': player.in_jail_for,
            'is_in_jail': player.is_in_jail(),
            'joined': player.joined
        }
        pp.append(p)
    pp = sorted(pp, key=lambda p: p['joined']) 

    # Squares list of Python dictionaries
    # instead of a list with Django objects
    ss = []
    squares = game.square_set.all()
    for square in squares:
        s = {
            'position': square.position,
            'title': square.title,
            'type': board.squares[square.position]['type'],
            'players': []
        }

        # Players who are currently on the square
        s_players = square.player_set.all()
        if len(s_players):
            for player in s_players:
                s['players'].append({
                    'player_id': player.pk,
                    'player_name': player.name,
                    'joined': player.joined
                })

        # Reflect the square's type
        if s['type'] == 'property':
            s['is_mortgaged'] = square.property.is_mortgaged
            if square.property.owned_by is not None:
                s['owned_by'] = {
                    'name': square.property.owned_by.name,
                    'joined': square.property.owned_by.joined
                }
            else:
                s['owned_by'] = None

        elif s['type'] == 'utility':
            s['is_mortgaged'] = square.utility.is_mortgaged
            if square.utility.owned_by is not None:
                s['owned_by'] = {
                    'name': square.utility.owned_by.name,
                    'joined': square.utility.owned_by.joined
                }
            else:
                s['owned_by'] = None
        
        ss.append(s)

    state = {
        'players': pp,
        'squares': ss,
        'is_your_turn': not current_player.plays_in_turns,
        'rolled_this_turn': current_player.rolled_this_turn,
        'can_be_bought': current_player.rolled_this_turn and rules.can_be_bought(current_player, current_player.square),
        'can_be_mortgaged': rules.can_be_mortgaged(current_player, current_player.square),
        'can_draw_card': rules.can_draw_card(player),
        'can_pay_jail': current_player.is_in_jail() and current_player.plays_in_turns == 0
    }
        
    state = json.dumps(state, indent=4, sort_keys=True)

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


#### Property views
@login_required
@csrf_exempt
def property_check(request):
    post = request.POST
    try:
        player = request.user.profile.groupe
    except UserProfile.DoesNotExist:
        return redirect('index') # Disallow joining games in progress
    player = request.user.profile.groupe
    game = Game.objects.get(id=1)
    square = Square.objects.filter(game=game).get(position=post['property_id'])
    game_property = False

    try:
        game_property = Property.objects.get(square=square)
    except:
        try:
            game_property = Utility.objects.get(square=square)
        except:
            return JsonResponse({'owned' : False})
    if (game_property.owned_by == player):
        return JsonResponse({'owned' : True})
    else:
        return JsonResponse({'owned' : False})
