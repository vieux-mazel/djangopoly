from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.db.models import Count
import json, random, string

from monopoly.models import Game, Square, Property, Utility, Special, Player, Street, Effect, UserProfile
from jchat.models import Message, Room
import rules
from board import squares

#### Property views
@login_required
def property_info(request):
    post = request.POST
    player = request.user.profile.groupe
    sid = int(post['square_id'])

    square = Square.objects.filter(position=sid,game=player.game).get()
    if squares[square.position]['type'] == 'special':
        return HttpResponse(FAILURE)
    clicked_object = rules.identify_square(square)
    forms = []

    rendered = render_to_string('property_info.html', { 'clicked_object': clicked_object })
    return JsonResponse({'html' : rendered})

def reste_de_code(request):
    post = request.POST
    try:
        player = request.user.profile.groupe
    except UserProfile.DoesNotExist:
        return redirect('index') # Disallow joining games in progress
    player = request.user.profile.groupe
    game = player.game
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
