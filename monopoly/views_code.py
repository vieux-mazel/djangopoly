# -*- encoding: UTF-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

import json#, random, string

from monopoly.models import Player, UserProfile
from jchat.models import Room
import rules
from board import squares
FAILURE = json.dumps({'success': False})
SUCCESS = json.dumps({'success': True})


def send_message(message,user):
    groupe = user.profile.groupe
    r =  Room.objects.get(groupe=groupe)
    r.say(user, message)
def validate(request):
    return JsonResponse(SUCCESS)
#### Property views
