from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout, login

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'allstars.views.home', name='home'),
    #home page

    url(r'^leagues/$', 'allstars.views.leagues'),
    #show all the leagues for the game and what teams reside in those leagues

    url(r'^team/(?P<team_name>[\S\w ]+)/$', 'allstars.views.team_detail'),
    #team detail page, gives list of players

    url(r'^players/$', 'allstars.views.players'),
    #list of all players, can sort by position

    url(r'^player/(?P<player_name>[\S\w ]+)/$', 'allstars.views.player_detail'),
    #player detail page, gives player stats

    url(r'^filter_players/$', 'allstars.views.filter_players'),
    #ajax view for players
    
    url(r'^set_roster/$', 'allstars.views.set_roster'),
    #set your roster so you can play the game

    url(r'^lobby/$', 'allstars.views.lobby'),
    #going into the lobby

    url(r'^lobbyupdate/$', 'allstars.views.lobbyupdate'),
    #ajax for updating lobby

    url(r'^lobbyexit/$', 'allstars.views.lobbyexit'),
    #ajax view for exiting the lobby

    url(r'^play_game/$', 'allstars.views.play_game'),
    #play the game todo make accept two teams

    url(r'^create/$', 'allstars.views.create'),
    #create user

    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    #logout

    (r'^login/$', 'django.contrib.auth.views.login'),
    #login

    url(r'^validate_user/$', 'allstars.views.validate_user'),

    url(r'^draft/$', 'allstars.views.draft'),
    #drafting your team

    url(r'^draft_player/$', 'allstars.views.draft_player'),
    #ajax

    url(r'^admin/', include(admin.site.urls)),
    #builtin admin
)