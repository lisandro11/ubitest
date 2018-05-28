from django.urls import path, include
from django.conf.urls import url

from . import views

app_name = 'occurrences'

urlpatterns = [
    url(r'^$', views.occurrences_list, name="list"),
    url(r'^map/$', views.occurrences_map, name="map"),
    url(r'^create/$', views.occurrence_create, name="create"),
    url(r'^(?P<id>[\d]+)/$', views.occurrence_details, name="detail"),
]
