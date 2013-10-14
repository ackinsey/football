from django.db.models import Q
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from allstars.models import Player, Team, Game
from allstars.forms import RosterForm

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
@csrf_protect
def set_roster(request):
	p = Player.objects.filter(team=Team.objects.filter(user=request.user)[0])
	form = None
	if request.method == 'POST':
		form = RosterForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/')
	else:
		form = RosterForm()
	return render_to_response('allstars/set_roster.html', {
        'form': form,
    },RequestContext(request))
