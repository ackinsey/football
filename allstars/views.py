from django.db.models import Q, Sum
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from allstars.models import Player, Team, Game, League, Statistic
from allstars.forms import RosterForm

def home(request):
    return render(request, 'allstars/home.html', {
    })

def player_detail(request, player_name):
	p = Player.objects.get(name=player_name)
	s = Statistic.objects.filter(player=p).order_by('week')
	totals=[]
	totals.append(s.aggregate(Sum('passing_yards')).get('passing_yards__sum'))
	totals.append(s.aggregate(Sum('passing_touchdowns')).get('passing_touchdowns__sum'))
	totals.append(s.aggregate(Sum('rushing_yards')).get('rushing_yards__sum'))
	totals.append(s.aggregate(Sum('rushing_touchdowns')).get('rushing_touchdowns__sum'))
	totals.append(s.aggregate(Sum('receiving_yards')).get('receiving_yards__sum'))
	totals.append(s.aggregate(Sum('receiving_touchdowns')).get('receiving_touchdowns__sum'))
	return render(request, 'allstars/player_detail.html', {
		'player':p,
		'statistics':s,
		'total_statistics':totals
		})

def players(request):
	p = Player.objects.all()
	#for pi in p:
		#pi.is_active=False
		#pi.generate_ratings()
		#pi.save()
	return render(request, 'allstars/players.html', {
		'players':p,
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
	#for pi in p:
	#	pi.is_active=False
	#	pi.save()
	if request.method == 'POST':
		form = RosterForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/')
	else:
		form = RosterForm()
	return render_to_response('allstars/set_roster.html', {
        'form': form,
    },RequestContext(request))

def play_game(request):
	g = Game.objects.get(week=League.objects.get().week)
	g.generate_result()
	return render(request, 'allstars/play_game.html', {
		'game': g,
	})