from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'allstars.views.home', name='home'),
    #home page

    url(r'^player/(?P<player_name>[\S\w ]+)/$', 'allstars.views.player_detail'),
    #player detail page, gives player stats

    url(r'^team/(?P<team_name>[\S\w ]+)/$', 'allstars.views.team_detail'),
    #team detail page, gives list of players

    url(r'^players/$', 'allstars.views.players'),
    #list of all players, can sort by position

    url(r'^filter_players/$', 'allstars.views.filter_players'),

    url(r'^leagues/$', 'allstars.views.leagues'),
#league detail view plz

    url(r'^schedule/$', 'allstars.views.schedule'),

    url(r'^set_roster/$', 'allstars.views.set_roster'),
    #list index out of range

    url(r'^play_game/$', 'allstars.views.play_game'),

    url(r'^create/$', 'allstars.views.create'),

    url(r'^validate_user/$', 'allstars.views.validate_user'),

    url(r'^draft/$', 'allstars.views.draft'),

    url(r'^draft_player/$', 'allstars.views.draft_player'),

    url(r'^admin/', include(admin.site.urls)),

)