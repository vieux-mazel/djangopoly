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
from django.utils import timezone
import datetime

from jchat.models import Room, Message, Spy_code
from .forms import SpyForm, SpyTeamSelector

@login_required
def spy(request,hash=False):
    now = timezone.now() - datetime.timedelta(hours=12)
    codes = Spy_code.objects.filter(used_by=request.user.profile.groupe, first_used__gt=now)
    if not hash:
        if request.method == 'POST':
            p = request.POST
            form = SpyForm(p)
            hash = p['spycode']
            try:
                spy = Spy_code.objects.get(spy_hash = hash)
            except Spy_code.DoesNotExist:
                message = 'ce code n\'est pas valide - En cas de besoin n\'hésite pas à contacter cg@vieux-mazel.ch'
                return render(request, 'spy.html' , {'message': message, 'form':form, 'codes':codes})
            if (spy.is_active()):
                try:
                    if(p['spyteam']):
                        spy.linked_room = Room.objects.get(pk=int(p['spyteam']))
                        spy.save()
                except:
                    pass
                print spy.is_allowed(request.user.profile.groupe)
                if (not spy.is_allowed(request.user.profile.groupe)):
                    message = 'ce code est déjà utilisé par une autre équipe ! Soit tu essaies de tricher... c\'est bien essayé mais triche mieux la prochaine fois ;-) soit tu t\'es fait piqué ton code d\'accès SHAME ON YOU :-)'
                    return render(request, 'spy.html' , {'message': message, 'form':form, 'codes':codes})
                if (spy.is_set()):
                    return render(request, 'spy.html', {'hash': spy, 'codes':codes})
                else:
                    form_team = SpyTeamSelector()
                    return render(request, 'spy.html', {'hash':spy, 'form': form, 'form_teamselector':form_team, 'codes':codes})
            else:
                message = 'ce code a expiré, il n\'est plus valable. Pour rappel les codes d\'espionnage ne sont utilisables que 12h.'
                return render(request, 'spy.html' , {'message': message, 'form':form, 'codes':codes})
        else:
            form = SpyForm()
            return render(request, 'spy.html', {'form':form, 'codes':codes})
    else:
        spy = Spy_code.objects.get(spy_hash = hash)
        return render(request, 'spy.html', {'hash': spy, 'codes':codes})

@login_required
def send(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    player = request.user.profile.groupe
    if p['is_commun'] == unicode('true'):
        r = Room.objects.get(is_commun=True)
    else :
        r =  Room.objects.get(groupe=player)
    r.say(request.user, p['message'])
    return HttpResponse('')

@login_required
def sync(request):
    '''Return last message id

    EXPECTS the following POST parameters:
    id
    '''
    p = request.POST
    player = request.user.profile.groupe
    if p['is_commun'] == unicode('true'):
        r = Room.objects.get(is_commun=True)
    else :
        r =  Room.objects.get(groupe=player)
    lmid = r.last_message_id()

    return HttpResponse(jsonify({'last_message_id':lmid}))

@login_required
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
    if post['is_commun'] == unicode('true'):
        r = Room.objects.get(is_commun=True)
    else :
        r =  Room.objects.get(groupe=player)
    m = r.messages(offset)
    return HttpResponse(jsonify(m, ['id','author','message','type','timestamp']))

@login_required
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
def join(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    player = request.user.profile.groupe
    r =  Room.objects.get(groupe=player)
    r.join(request.user)
    return HttpResponse('')

@login_required
def leave(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    player = request.user.profile.groupe
    r =  Room.objects.get(groupe=player)
    r.leave(request.user)
    return HttpResponse('')

@login_required
def test(request):
    '''Test the chat application'''

    u = request.user.profile.groupe # always attach to first user id
    r = Room.objects.get_or_create(u)
    #return render(request, 'simple.html')
    return render_to_response('simple.html', {'js': ['/media/js/mg/chat.js'], 'chat_id':r.pk, 'is_com':'true'})

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
