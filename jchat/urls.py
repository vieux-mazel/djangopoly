from django.conf.urls import patterns, url
from jchat import views

urlpatterns = patterns('',
        #url(r'^request/$', 'jchat.views.forum'),
        url(r'^$', views.test, name="test"),
        url(r'^send/$', views.send, name="send"),
        url(r'^receive/$', views.receive, name="receive"),
        url(r'^receive_spy/$', views.receive_spy, name="receive_spy"),
        url(r'^sync/$', views.sync, name="sync"),
        url(r'^spy/$', views.spy, name="spy_index"),
        url(r'^spy/(?P<hash>[\w\-]+)/$', views.spy, name="spy"),
        url(r'^join/$', views.join, name="join"),
        url(r'^leave/$', views.leave, name="leave"),
)
