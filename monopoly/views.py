from django.shortcuts import render, redirect
from django.http import HttpResponse

from monopoly.models import Game

# Create your views here.
def index(request):
    return HttpResponse('Hello')

def game(request, id):
    game = Game.objects.get(id=id)
    print game
    return HttpResponse(str(game.id) + ' ' + str(game.private))

def new_game(request, private):
    newGame = Game()
    newGame.private = True if private == "private" else False
    newGame.save()

    return redirect(game, id=newGame.id)
