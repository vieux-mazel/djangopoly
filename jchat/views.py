# -*- encoding: UTF-8 -*-
'''
Chat application views, some are tests... some are not
@author: Federico Cáceres <fede.caceres@gmail.com>
'''
import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from jchat.models import Room, Message, Spy_code
from .forms import SpyForm, SpyTeamSelector

@login_required
def spy(request):
    if request.method == 'POST':
        p = request.POST
        form = SpyForm(p)
        hash = p['spycode']
        print hash
        try:
            spy = Spy_code.objects.get(spy_hash = hash)
        except Spy_code.DoesNotExist:
            message = 'ce code n\'est pas valide - En cas de besoin n\'hésite pas à contacter cg@vieux-mazel.ch'
            return render(request, 'spy.html' , {'message': message, 'form':form})
        if (spy.is_active()):
            try:
                if(p['spyteam']):
                    spy.linked_room = Room.objects.get(id=p['spyteam'])
                    spy.save()
            except:
                pass
            print spy.is_allowed(request.user.profile.groupe)
            if (not spy.is_allowed(request.user.profile.groupe)):
                message = 'ce code est déjà utilisé par une autre équipe ! Soit tu essaies de tricher... c\'est bien essayé mais triche mieux la prochaine fois ;-) soit tu t\'es fait piqué ton code d\'accès SHAME ON YOU :-)'
                return render(request, 'spy.html' , {'message': message, 'form':form})
            if (spy.is_set()):
                return render(request, 'spy.html', {'hash': hash})
            else:
                form_team = SpyTeamSelector()
                return render(request, 'spy.html', {'hash':hash, 'form': form, 'form_teamselector':form_team})
        else:
            message = 'ce code a expiré, il n\'est plus valable. Pour rappel les codes d\'espionnage ne sont utilisables que 12h.'
            return render(request, 'spy.html' , {'message': message, 'form':form})
    else:
        form = SpyForm()
        return render(request, 'spy.html',{'form': form})

@login_required
@csrf_exempt
def send(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    player = request.user.profile.groupe
    r = Room.objects.get(id=player.id)
    r.say(request.user, p['message'])
    return HttpResponse('')

@login_required
@csrf_exempt
def sync(request):
    '''Return last message id

    EXPECTS the following POST parameters:
    id
    '''

    player = request.user.profile.groupe
    r = Room.objects.get(id=player.id)

    lmid = r.last_message_id()

    return HttpResponse(jsonify({'last_message_id':lmid}))

@login_required
@csrf_exempt
def receive(request):
    '''
    Returned serialized data

    EXPECTS the following POST parameters:
    id
    offset

    This could be useful:
    @see: http://www.djangosnippets.org/snippets/622/
    '''

    post = request.POST

    try:
        offset = int(post['offset'])
    except:
        offset = 0
    player = request.user.profile.groupe
    r = Room.objects.get(id=player.id)

    m = r.messages(offset)
    return HttpResponse(jsonify(m, ['id','author','message','type','timestamp']))

@login_required
@csrf_exempt
def receive_spy(request):
    '''
    Returned serialized data

    EXPECTS the following POST parameters:
    id
    offset

    This could be useful:
    @see: http://www.djangosnippets.org/snippets/622/
    '''

    post = request.POST
    spy_hash = post['spycode']
    try:
        spy = Spy_code.objects.get(spy_hash = spy_hash)
    except Spy_code.DoesNotExist:
        return HttpResponse(jsonify(["error"]))
    try:
        offset = int(post['offset'])
    except:
        offset = 0

    r = spy.linked_room
    m = r.messages(offset)
    return HttpResponse(jsonify(m, ['id','author','message','type','timestamp']))

@login_required
@csrf_exempt
def join(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    player = request.user.profile.groupe
    r = Room.objects.get(id=player.id)
    r.join(request.user)
    return HttpResponse('')

@login_required
@csrf_exempt
def leave(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    player = request.user.profile.groupe
    r = Room.objects.get(id=player.id)
    r.leave(request.user)
    return HttpResponse('')

@login_required
def test(request):
    '''Test the chat application'''

    u = request.user.profile.groupe # always attach to first user id
    r = Room.objects.get_or_create(u)
    #return render(request, 'simple.html')
    return render_to_response('simple.html', {'js': ['/media/js/mg/chat.js'], 'chat_id':r.pk})

def jsonify(object, fields=None, to_dict=False):
    '''Funcion utilitaria para convertir un query set a formato JSON'''
    try:
        import json
    except ImportError:
        import django.utils.simplejson as json

    out = []

    if type(object) not in [dict,list,tuple] :
        for i in object:
            tmp = {}
            if fields:
                for field in fields:
                    try:
                        tmp[field] = unicode(i.__getattribute__(field).strftime('%d %b - %Hh%M'))
                    except:
                        tmp[field] = unicode(i.__getattribute__(field))
            else:
                for attr, value in i.__dict__.iteritems():
                    tmp[attr] = value
            out.append(tmp)
    else:
        out = object
    if to_dict:
        return out
    else:
        return json.dumps(out)
