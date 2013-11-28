from django.db.models import Q, Sum
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.utils import simplejson
from django.contrib.auth.models import User
from allstars.models import Player, Team, Game, League, Statistic
from allstars.forms import RosterForm, RegisterForm
from django.core import serializers
from django.contrib.auth.decorators import login_required
from datetime import datetime

def home(request):
	#Just rendering a template for the home page.
    return render(request, 'allstars/home.html', {
    })

def leagues(request):
	l = League.objects.all()

	t = Team.objects.filter(league=l)

	return render(request, 'allstars/leagues.html', {
		'leagues':l,
		'teams': t,	
	})

def team_detail(request, team_name):
	try:
		t = Team.objects.get(team_name=team_name)
	except:
		raise Http404

	players = Player.objects.filter(team=t)
	
	return render(request, 'allstars/team_detail.html', {
		'players':players,
		'team': t,
		})

def players(request):
	p = Player.objects.all()

	return render(request, 'allstars/players.html', {
		'players':p,
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


def filter_players(request):
	if 'selection' in request.POST:
		response = HttpResponse(content_type="application/json")
		serializers.serialize("json", Player.objects.filter(position=request.POST['selection']), stream=response)
		return response

@csrf_protect
def set_roster(request):
	form = None

	if request.method == 'POST':
		form = RosterForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/')
	else:
		form = RosterForm(request.user)
	return render_to_response('forms/set_roster.html', {
        'form': form,
    },RequestContext(request))


draft_dict={}
draft_log=[]

@login_required
def draft(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/login')

	p = Player.objects.filter(team__isnull=True)
	drafted_p = Player.objects.filter(team=Team.objects.filter(user=request.user))
	return render(request, 'allstars/draft.html', {
		'players':p,
		'drafted_players':drafted_p,
	})

def draft_player(request):
	if 'selection' in request.POST:
		if Team.objects.filter(league=League.objects.all()[0])[League.objects.all()[0].draft_index]==Team.objects.get(user=request.user) and Player.objects.get(name=request.POST['selection']).team==None:
			selected_player=Player.objects.get(name=request.POST['selection'])
			selected_player.team=Team.objects.get(user=request.user)
			selected_player.save()
			#draft_log.append("The "+selected_player.team.team_name+" draft "+selected_player.name) maybe later

			undrafted=serializers.serialize('python', Player.objects.filter(team__isnull=True))
			team=serializers.serialize('python', Player.objects.filter(team=selected_player.team))

			json = simplejson.dumps([undrafted,team])
			lge=League.objects.all()[0]
			lge.draft_index=1+lge.draft_index if int(lge.draft_index) < len(Team.objects.filter(league=lge))-1 else 0
			lge.save()
			
			return HttpResponse(json, mimetype='text/json')
		return HttpResponse()
	elif not 'selection' in request.POST:
		undrafted=serializers.serialize('python', Player.objects.filter(team=None))
		team=serializers.serialize('python', Player.objects.filter(team=Team.objects.get(user=request.user)))
		current=serializers.serialize('python', [Team.objects.filter(league=League.objects.all()[0])[League.objects.all()[0].draft_index]])
		json = simplejson.dumps([undrafted,team,current,draft_log])
		return HttpResponse(json, mimetype='text/json')

def create(request):
	form = None

	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			usr = User.objects.create_user(username=request.POST['username'], email=request.POST['email_address'],password=request.POST['password'])
			usr.save()
			team = Team()#team_name=request.POST['team_name'], user=usr)
			team.team_name=request.POST['team_name']
			team.league=League.objects.all()[0]
			team.email_address=usr.email
			team.user=usr;
			team.save()
			return HttpResponseRedirect('/')
	else:
		form = RegisterForm()
	return render_to_response('forms/create.html', {
        'form': form,
    },RequestContext(request))

def validate_user(request):
	if 'username' in request.POST:
		user_confirm=''
		user_error=''
		if len(User.objects.filter(username=request.POST['username']))==0:
			user_confirm='That username is available.'
		else:
			user_error='That username is taken.'
		return HttpResponse(simplejson.dumps({
				'user_error':user_error,
				'user_confirm':user_confirm,
				}))
	if 'team_name' in request.POST:
		team_error=''
		team_confirm=''
		if len(Team.objects.filter(team_name=request.POST['team_name']))==0:
			team_confirm='That team name is available.'
		else:
			team_error='That team name is taken.'
		return HttpResponse(simplejson.dumps({
				'team_confirm':team_confirm,
				'team_error':team_error,
				}))
	if 'password' in request.POST:
		password_confirm=''
		password_error=''
		if request.POST['password']==request.POST['password_retype']:
			password_confirm='Passwords match.'
		else:
			password_error='The passwords don\'t match'
		return HttpResponse(simplejson.dumps({
		'password_error':password_error,
		'password_confirm':password_confirm,
		}))

	return HttpResponse(simplejson.dumps({
		'user_error':'',
		'user_confirm':user_confirm,
		'team_error':team_error,
		'team_confirm':team_confirm,
		'password_error':'',
		'password_confirm':'Passwords match.',
		}))


def play_game(request, team1):
	t1 = Team.objects.get(team_name=team1)
	t2 = Team.objects.get(user=request.user)

	g = Game(team_1=t1, team_2=t2, week=0)
	g.save()
	g.generate_result()
	
	
	#s = Statistic.objects.all()

	return render(request, 'allstars/play_game.html', {
		'game': g,
		#'stats': s,
	})

@login_required
def lobby(request):
	t = Team.objects.get(user=request.user)

	t.play_ready = True
	t.save()

	teams = Team.objects.filter(play_ready = True)
	hosts = Team.objects.filter(hosting_game = True)

	return render(request, 'allstars/lobby.html', {
		'teams':teams,
		'hosts':hosts,
	})

def lobbyupdate(request):
	if "hosting" in request.POST:
		t = Team.objects.get(user=request.user)

		t.hosting_game = True
		t.play_ready = False
		t.save()

	teams=serializers.serialize('python', Team.objects.filter(play_ready=True))
	hosts=serializers.serialize('python', Team.objects.filter(hosting_game=True))
	json = simplejson.dumps([teams,hosts])
	return HttpResponse(json, mimetype='text/json')

def lobbyexit(request):
	t = Team.objects.get(user=request.user)

	t.play_ready = False
	t.hosting_game = False
	t.save()

	return render(request, 'allstars/lobby.html', {
	})