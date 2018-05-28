from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from occurrences import views as occurrence_views
from accounts import views as accounts_views




urlpatterns = [
    url(r'^$', accounts_views.login_view, name='homepage'), #homepage, list of occurrences
    url(r'^admin/', admin.site.urls, name='admin'), #Administration
    url(r'^api/', include('api.urls'), name='api'), #Rest API
    url(r'^accounts/', include('accounts.urls'), name='accounts'), #Users Management
    url(r'^occurrences/', include('occurrences.urls'), name='occurences'), #Occurrences Management
    url(r'^about/$', views.about, name='about'), #About Page
]


urlpatterns += staticfiles_urlpatterns()
