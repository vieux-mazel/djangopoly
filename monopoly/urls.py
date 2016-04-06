from django.conf.urls import patterns, url
from monopoly import views, views_property

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^new_game/(?P<private>[\w\-]+)/$', views.new_game, name='new_game'),
        url(r'^join_random/$', views.join_random_game, name='join_random_game'),
        url(r'^leave/$', views.leave, name='leave'),
        url(r'^help/$', views.help, name='help'),
        url(r'^game/roll/$', views.roll_dice, name='roll_dice'),
        url(r'^game/end_turn/$', views.end_turn, name='end_turn'),
        url(r'^game/buy/$', views.buy, name='buy'),
        url(r'^game/mortgage/$', views.mortgage, name='mortgage'),
        url(r'^game/pay_bailout/$', views.pay_bailout, name='pay_bailout'),
        url(r'^game/draw_card/$', views.draw_card, name='draw_card'),
        url(r'^game/(?P<id>[\w\-]+)/$', views.game, name='game'),
        url(r'^game/(?P<id>[\w\-]+)/start/$', views.start_game, name='start_game'),
        url(r'^game/(?P<id>[\w\-]+)/join/$', views.join_game, name='join_game'),
        url(r'^game/(?P<id>[\w\-]+)/state/$', views.game_state, name='game_state'),
        url(r'^super_reset/$', views.super_reset, name="super_reset"),
        url(r'^game/property/info', views_property.property_info, name='info_property'),
)
