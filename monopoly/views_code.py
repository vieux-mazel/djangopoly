# -*- encoding: UTF-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import CheatCodeForm
import json#, random, string

from monopoly.models import Player, UserProfile, Code
from jchat.models import Room, Spy_code
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

def code(request):
    form = CheatCodeForm()
    hash = ''
    try:
        p = request.POST
        hash = Code.objects.get(hash=p['cheatcode'])
    except:
        try:
            hash = Spy_code.objects.get(spy_hash=p['cheatcode'])
            if hash:
                return render(request,'code.html', {'form':form, 'message':'Ce code semble être un code d\'espionnage, merci de te rendre sur la page d\'espionnage !'})
        except:
            return render(request, 'code.html', {'form':form,'message':'Ce code n\'existe pas, merci de le vérifier ou de contacter cg@vieux-mazel.ch'})
    else:
        if hash.is_used:
            return render(request, 'code.html', {'form':form,'message':'Code déjà utilisé'})
        form = CheatCodeForm(p)
        u = request.user
        g = u.profile.groupe
        if (hash.effect == 'g'): #give money
            effet = 'de gagner 1000$'
            rules.give_money(u,1000)
        elif (hash.effect == 'a'): # adddice
            effect = 'd\'ajouter un jet de dé gratuitement'
            g.dice_left += 1
            g.save()
        elif (hash.effect == 'm'): #moveanywhere
            effect = 'de se déplacer n\'importe où sur la carte'
            g.free_move += 1
            g.save()
        elif (hash.effect == 's'): # shield
            effect = 'de se protéger des 2 prochaines taxes de passage'
            g.is_protected += 2
            g.save()
        elif (hash.effect == 'f'): # freebuy
            effect = 'd\'acheter une propriété gratuitement'
            g.free_buy +=1
            g.save()
        message = '{user} a activé un code permettant {effect}'.format(user=u,effect=effect)
        send_message(message,u)
        hash.is_used = True
        hash.save()
        return render(request, 'code.html', {'message':message})
#### Property views
