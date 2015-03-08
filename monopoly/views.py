from django.shortcuts import render, redirect
from django.http import HttpResponse

from monopoly.models import Game, Square, Property, Utility, Special, Player
from board import board

# Placeholder index page
def index(request):
    return HttpResponse('Hello')

# Displays the game
def game(request, id):
    game = Game.objects.get(id=id)
    
    request.session['has_session'] = True
    session_id = request.session.session_key
    
    try:
        player = Player.objects.get(session_id=session_id)
    except Player.DoesNotExist:
        player = Player(session_id=session_id, game=game, square=Square.objects.get(game=game, position=0))
        player.save()

    if player.game != game:
        return redirect('index')
    
    print player
    return HttpResponse(str(game.id) + ' ' + str(game.private))

# Create a new game
# Can be private or public, depends on URL invocation
def new_game(request, private):
    newGame = Game()
    newGame.private = True if private == "private" else False
    newGame.save()

    # Create game board
    # 40 squares that are either properties, utilities, or "specials"
    # Listed in board.py
    squares = []
    for x in sorted(board, key=lambda k: k['position']):
        square = Square(position=x['position'], game=newGame)
        identity = None # Identity of the square (property/utility/special)
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

    # After creating the game, redirect to game view
    return redirect(game, id=newGame.id)
