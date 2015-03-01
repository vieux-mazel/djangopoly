from django.shortcuts import render, redirect
from django.http import HttpResponse

from monopoly.models import Game

# Create your views here.
def index(request):
	return HttpResponse('Hello')

def new_game(request, private):
	#private = request.GET['private'] or False
	print private

	game = Game()
	game.private = True if private == "private" else False
	game.save()
	print game

	return redirect(index)