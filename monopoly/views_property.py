# -*- encoding: UTF-8 -*-
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
FAILURE = json.dumps({'success': False})
SUCCESS = json.dumps({'success': True})


def send_message(message,user):
    groupe = user.profile.groupe
    r =  Room.objects.get(groupe=groupe)
    r.say(user, message)

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

def property_action(request):
    p = request.POST
    groupe = request.user.profile.groupe
    user = request.user
    house = Property.objects.get(pk=int(p['property_id']))
    if (p['action_type'] == 'buy-house'):
        if (house.owned_by == groupe):
            if (rules.can_build_house(house.square, groupe)):
                if (not house.build_house == 5):
                    house.build_house += 1 # ajoute une maison a la property
                    house.save()
                    message = "--> Nouvelle maison sur <b style='color:{color};'> {name} </b> - fait par {player}".format(
                              color = house.street.color,
                              name = house.square.title,
                              player = request.user.username)
                    send_message(message, user)
                    return HttpResponse(SUCCESS)
        return HttpResponse(FAILURE)

    elif(p['action_type'] == 'mortage-house'):
        if(rules.mortgage(groupe, house.square)):
            message = "--> La propriete <b style='color:{color};'> {name} </b> a été hypothèquéee - fait par {player}".format(
                      color=house.street.color,
                      name=house.square.title,
                      player = request.user.username)
            send_message(message, user)
            return HttpResponse(SUCCESS)
        return HttpResponse(FAILURE)

    elif(p['action_type'] == 'unmortgage-house'):
        if(rules.unmortgage(groupe, house.square)):
            message = "--> La propriete <b style='color:{color};'> {name} </b> est dé-hypothèquéee - fait par {player}".format(
                      color=house.street.color,
                      name=house.square.title,
                      player = request.user.username)
            send_message(message,user)
            return HttpResponse(SUCCESS)
        return HttpResponse(FAILURE)

    elif(p['action_type'] == 'sell-house'):
        if (house.owned_by == groupe):
            if (house.build_house > 0):
                house.build_house -= 1 # ajoute une maison a la property
                house.save()
                rules.give_money(groupe, house.house_sell_price)
                message = "--> Maison vendue sur <b style='color:{color};'> {name} </b> - fait par {player}".format(
                          color = house.street.color,
                          name = house.square.title,
                          player = request.user.username)
                send_message(message, user)
                return HttpResponse(SUCCESS)
    return HttpResponse(FAILURE)

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
