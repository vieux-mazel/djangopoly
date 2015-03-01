from django.shortcuts import render, redirect
from django.http import HttpResponse

from monopoly.models import Game, Square, Property, Utility, Special
from board import properties, utilities, specials

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
    for x in range(40):
        square = Square(position=x, game=newGame, title='Square ' + str(x))
        square.save()
        squares.append(square)

    for prop in properties:
        property = Property()
        property.square = squares[prop['position']]
        property.square.title = prop['title']
        property.square.save()
        property.save()

    for util in utilities:
        utility = Utility()
        utility.square = squares[util['position']]
        utility.square.title = util['title']
        utility.square.save()
        utility.save()

    for spec in specials:
        special = Special()
        special.square = squares[spec['position']]
        special.square.title = spec['title']
        special.square.save()
        special.save()

    for square in squares:
        print square.title

    return redirect(game, id=newGame.id)
