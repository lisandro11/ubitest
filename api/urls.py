from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from occurrences.models import Occurrence
from . import views

app_name = 'api'

urlpatterns = [
    url(r'^occurrences/$', views.occurrence_list, name='list'),
    url(r'^occurrences/(?P<id>[0-9]+)/$', views.occurrence_details, name='details'),
    url(r'^occurrences/create/$', views.occurrence_create, name='create'),
    url(r'^occurrences/validate/(?P<id>[0-9]+)/$', views.occurrence_update, name='retreive-update'),
    url(r'^occurrences/author/(?P<author>[0-9]+)/$', views.occurrence_by_author, name='occurrence-by-author'),
    url(r'^occurrences/category/(?P<category>[\w]+)/$', views.occurrence_by_category, name='occurrence-by-category'),
    url(r'^occurrences/inrange/$', views.occurrence_in_range, name='occurrence-in-range'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
