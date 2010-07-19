from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template

from project.models import Project

from settings import WORKSPACE_DIR

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       (r'^$', direct_to_template, {'template': 'about.html'}),
                       (r'^about/$', direct_to_template, {'template': 'about.html'}),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^projects/', include('project.urls')),
                       (r'^forum/', include('forum.urls')),
                       #REST interface
                       (r'^api/', include('api.urls')))
