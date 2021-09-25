from django.conf.urls import url

from . import views

# '/store' will call the method "index" in viewws.py
urlpatterns = [
    url(r'^$', views.listing),
]
