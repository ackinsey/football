from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'allstars.views.home', name='home'),

    url(r'^player/(?P<player_name>[\S\w ]+)/$', 'allstars.views.player_detail'),

    url(r'^players/$', 'allstars.views.players'),
    
    url(r'^schedule/$', 'allstars.views.schedule'),

    url(r'^set_roster/$', 'allstars.views.set_roster'),

    url(r'^admin/', include(admin.site.urls)),
)