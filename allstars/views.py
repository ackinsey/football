from django.db.models import Q
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.utils import simplejson

from allstars.models import Player, Team, Game

def home(request):
    return render(request, 'allstars/home.html', {
    })

def player_detail(request, player_name):
	p = Player.objects.all()
	return render(request, 'allstars/player_detail.html', {
		'player':p,
		})

def players(request):
	p = Player.objects.all()

	return render(request, 'allstars/players.html', {
		'players':p
	})

def schedule(request):
	g=None
	if request.user.is_authenticated():
		g=Game.objects.filter(Q(team_1 = Team.objects.filter(user=request.user)) | Q(team_2 = Team.objects.filter(user=request.user))).order_by('week')
	return render(request, 'allstars/schedule.html', {
		'games':g
	})
