from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = 'store'

# '/store' will call the method "index" in viewws.py
urlpatterns = [
    url(r'^$', views.listing, name='listing'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^boss/', admin.site.urls)
]
