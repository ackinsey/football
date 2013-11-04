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

def home(request):
    return render(request, 'allstars/home.html', {
    })
draft_dict={}
draft_log=[]
def draft(request):
	#for player in Player.objects.all():
		#player.team=None
		#player.save()
	#lge=League.objects.all()[0]
	#lge.draft_index=0
	#lge.save()
	p = Player.objects.filter(team__isnull=True)
	drafted_p = Player.objects.filter(team=Team.objects.filter(user=request.user))
	return render(request, 'allstars/draft.html', {
		'draft_dict':draft_dict,
		'players':p,
		'drafted_players':drafted_p,
		'usr':request.user,
	})

def draft_player(request):
	if 'selection' in request.POST:
		if Team.objects.filter(league=League.objects.all()[0])[League.objects.all()[0].draft_index]==Team.objects.get(user=request.user) and Player.objects.get(name=request.POST['selection']).team==None:
			print "draft"
			selected_player=Player.objects.get(name=request.POST['selection'])
			selected_player.team=Team.objects.get(user=request.user)
			selected_player.save()
			draft_log.append("The "+selected_player.team.team_name+" draft "+selected_player.name)

			undrafted=serializers.serialize('python', Player.objects.filter(team=None))
			team=serializers.serialize('python', Player.objects.filter(team=selected_player.team))

			json = simplejson.dumps([undrafted,team])
			lge=League.objects.all()[0]
			lge.draft_index=1+lge.draft_index if int(lge.draft_index) < len(Team.objects.filter(league=lge))-1 else 0
			lge.save()
			
			return HttpResponse(json, mimetype='text/json')
		return HttpResponse()
	elif not 'selection' in request.POST:
		#print "update"
		#response = HttpResponse(content_type="application/json")
		#serializers.serialize("json", [Team.objects.filter(league=League.objects.all()[0])[League.objects.all()[0].draft_index]], stream=response)
		#return response
		undrafted=serializers.serialize('python', Player.objects.filter(team=None))
		team=serializers.serialize('python', Player.objects.filter(team=Team.objects.get(user=request.user)))
		current=serializers.serialize('python', [Team.objects.filter(league=League.objects.all()[0])[League.objects.all()[0].draft_index]])
		json = simplejson.dumps([undrafted,team,current,draft_log])
		return HttpResponse(json, mimetype='text/json')

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
			usr = User.objects.create_user(username=request.POST['username'], email=request.POST['email_address'],password=request.POST['password'])
			usr.save()
			team = Team()#team_name=request.POST['team_name'], user=usr)
			team.team_name=request.POST['team_name']
			team.league=League.objects.all()[0]
			team.email_address=usr.email
			team.user=usr;
			team.save()
			#team=Team.objects.create_user(team_name=form.team_name, email_address=form.email_address, password=form.password)
			return HttpResponseRedirect('/')
	else:
		form = RegisterForm()
	return render_to_response('forms/create.html', {
        'form': form,
    },RequestContext(request))

def validate_user(request):
		#'team_error':'There is already a team with that name',
		#'team_confirm':'that team name is available',
		#'password_error':'no errors',
		#'password_confirm':'the passwords are the same',
	#response=HttpResponse()

	#	undrafted=serializers.serialize('python', Player.objects.filter(team=None))
	#	team=serializers.serialize('python', Player.objects.filter(team=Team.objects.get(user=request.user)))
	#	current=serializers.serialize('python', [Team.objects.filter(league=League.objects.all()[0])[League.objects.all()[0].draft_index]])
	#	json = simplejson.dumps([undrafted,team,current,draft_log])

	#response = HttpResponse(content_type="application/json")
	#serializers.serialize("json", '')
	#current=serializers.serialize('json', 'aa'))
	#json = simplejson.dumps([current,current])
	#return HttpResponse(json, mimetype='text/json')`
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
	p = Player.objects.filter(team=Team.objects.filter(team_name=request.user)[0])
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