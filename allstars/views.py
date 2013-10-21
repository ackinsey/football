from django.db.models import Q, Sum
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.utils import simplejson

from allstars.models import Player, Team, Game, League, Statistic
from allstars.forms import RosterForm, RegisterForm
from django.core import serializers

def home(request):
    return render(request, 'allstars/home.html', {
    })

def player_detail(request, player_name):
	try:
		p = Player.objects.get(name=player_name)
	except:
		raise Http404

	stats = Statistic.objects.filter(player=p).order_by('week')
	totals=[]

	for field in Statistic._meta.fields[4:]:
		totals.append(stats.aggregate(Sum(field.name)).get('%s__sum' %field.name))
	
	return render(request, 'allstars/player_detail.html', {
		'player':p,
		'statistics':stats,
		'total_statistics':totals
		})

def players(request):
	p = Player.objects.all()

	return render(request, 'allstars/players.html', {
		'players':p,
	})

def create(request):
	form = None

	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			team=Team.objects.create_user(team_name=form.team_name, email_address=form.email_address, password=form.password)
			return HttpResponseRedirect('/')
	else:
		form = RegisterForm()
	return render_to_response('forms/create.html', {
        'form': form,
    },RequestContext(request))

def filter_players(request):
	if 'selection' in request.POST:
		response = HttpResponse(content_type="application/json")
		serializers.serialize("json", Player.objects.filter(position=request.POST['selection']), stream=response)
		return response

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
	return render_to_response('forms/set_roster.html', {
        'form': form,
    },RequestContext(request))

def play_game(request):
	g = Game.objects.get(week=League.objects.get().week)
	g.generate_result()
	return render(request, 'allstars/play_game.html', {
		'game': g,
	})