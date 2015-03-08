from django.conf.urls import patterns, url
from monopoly import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^new_game/(?P<private>[\w\-]+)/$', views.new_game, name='new_game'),
        url(r'^game/roll/$', views.roll_dice, name='roll_dice'),
        url(r'^game/(?P<id>[\w\-]+)/$', views.game, name='game'),
        url(r'^game/(?P<id>[\w\-]+)/start/$', views.start_game, name='start_game'),
)
