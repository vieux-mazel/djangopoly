from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('monopoly.urls')),
)
