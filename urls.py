from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template

from django_restapi.model_resource import Collection
from django_restapi.responder import JSONResponder
from project.models import Project

from settings import WORKSPACE_DIR

from django.contrib import admin
admin.autodiscover()

project_resource = Collection(
    queryset = Project.objects.all(),
    responder = JSONResponder(),
)

urlpatterns = patterns('',
                       (r'^$', direct_to_template, {'template': 'about.html'}),
                       (r'^about/$', direct_to_template, {'template': 'about.html'}),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^projects/', include('project.urls')),
                       (r'^forum/', include('forum.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': WORKSPACE_DIR + 'step2/site_media/'}),
                       #REST interface
                       (r'^json/project/(.*?)/?$', project_resource))
