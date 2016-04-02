from django.conf.urls import patterns, url
from jchat import views

urlpatterns = patterns('',
        #url(r'^request/$', 'jchat.views.forum'),
        url(r'^$', views.test, name="test"),
        url(r'^send/$', views.send, name="send"),
        url(r'^receive/$', views.receive, name="receive"),
        url(r'^sync/$', views.sync, name="sync"),

        url(r'^join/$', views.join, name="join"),
        url(r'^leave/$', views.leave, name="leave"),
)
