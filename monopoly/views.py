from django.shortcuts import render, redirect
from django.http import HttpResponse

from monopoly.models import Game, Square, Property, Utility, Special
from board import board

# Create your views here.
def index(request):
    return HttpResponse('Hello')

def game(request, id):
    game = Game.objects.get(id=id)

    return HttpResponse(str(game.id) + ' ' + str(game.private))

def new_game(request, private):
    newGame = Game()
    newGame.private = True if private == "private" else False
    newGame.save()

    squares = []
    for x in sorted(board, key=lambda k: k['position']):
        square = Square(position=x['position'], game=newGame)
        identity = None
        if x['type'] == 'property':
            identity = Property()
        elif x['type'] == 'utility':
            identity = Utility()
        elif x['type'] == 'special':
            identity = Special()
        square.title = x['title']
        square.save()
        identity.square = square
        identity.save()
        squares.append(square)

    for square in squares:
        print square.title

    return redirect(game, id=newGame.id)
